import asyncio
import openai
import logging
from typing import List, Dict, Any, Tuple

from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from sklearn.cluster import KMeans
import hdbscan
from transformers import (
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
)
from src.tools.base import BaseTool
from src.services.cache_service import CacheService
from src.core.exceptions import ToolError

logger = logging.getLogger(__name__)
cache = CacheService()

class MetadataSummarizerTool(BaseTool):
    name = "metadata_summarizer"

    def __init__(self, kmeans_clusters: int = 10, hdbscan_min_size: int = 10):
        self.kmeans_clusters = kmeans_clusters
        self.hdbscan_min_size = hdbscan_min_size

    @retry(
        retry=retry_if_exception_type(Exception),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        stop=stop_after_attempt(5),
        reraise=True,
    )
    async def _embed_batch(self, batch: List[str]) -> List[List[float]]:
        resp = openai.Embedding.create(model="text-embedding-ada-002", input=batch)
        return [item["embedding"] for item in resp["data"]]

    async def run(self, text_segments: List[str], metadata: Dict[str, Any]) -> Tuple[List[str], Dict[str, Any]]:
        try:
            cache_key = "|".join(text_segments)
            cached = await cache.get(self.name + ":embeddings", cache_key)
            if cached:
                embeddings = cached
                logger.debug("Используем кэшированные эмбеддинги")
            else:
                batch_size = 16
                batches = [text_segments[i : i + batch_size] for i in range(0, len(text_segments), batch_size)]
                tasks = [self._embed_batch(b) for b in batches]
                results = await asyncio.gather(*tasks)
                embeddings = [vec for batch in results for vec in batch]
                await cache.set(self.name + ":embeddings", cache_key, embeddings)
                logger.debug("Сгенерированы и закэшированы эмбеддинги")

            metadata["embeddings"] = embeddings

            km = KMeans(n_clusters=self.kmeans_clusters, random_state=42, n_init="auto")
            labels_km = km.fit_predict(embeddings)
            metadata["clusters_kmeans"] = labels_km.tolist()

            clusterer = hdbscan.HDBSCAN(
                min_cluster_size=self.hdbscan_min_size, metric="euclidean"
            )
            labels_hdb = clusterer.fit_predict(embeddings)
            metadata["clusters_hdbscan"] = labels_hdb.tolist()

            unique_labels = set(labels_hdb) - {-1}
            num_labels = len(unique_labels)
            model = AutoModelForSequenceClassification.from_pretrained(
                "roberta-base", num_labels=num_labels
            )

            training_args = TrainingArguments(
                output_dir="./checkpoints",
                per_device_train_batch_size=16,
                num_train_epochs=3,
                learning_rate=2e-5,
                weight_decay=0.01,
                logging_steps=50,
                evaluation_strategy="steps",
                save_total_limit=2,
            )
            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=metadata.get("train_ds"),
                eval_dataset=metadata.get("val_ds"),
            )
            trainer.train()
            metadata["classifier_checkpoint"] = "./checkpoints"

            return text_segments, metadata

        except Exception as e:
            logger.exception("MetadataSummarizerTool failed")
            raise ToolError(f"{self.name} failed: {e}")