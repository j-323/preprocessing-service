from pymilvus import connections, Collection
from src.models.domain import SearchRequest, SearchResponse, SearchResult
from src.config import settings
from src.core.exceptions import ServiceError

class SearchService:
    def __init__(self, collection_name: str = "songs"):
        connections.connect(host=settings.milvus_host, port=str(settings.milvus_port))
        self.collection = Collection(collection_name)

    def search(self, req: SearchRequest) -> SearchResponse:
        try:
            # здесь предполагаем, что req.metadata.get("embedding") есть
            query_vec = req.metadata.get("embedding", [0.0]*384)
            hits = self.collection.search(
                data=[query_vec],
                anns_field="embedding",
                param={"metric_type": "IP", "params": {"nprobe": 10}},
                limit=req.top_k,
                output_fields=["metadata"],
            )
            results = [
                SearchResult(
                    milvus_id=h.id,
                    score=h.score,
                    metadata=h.entity.get("metadata", {}),
                    blob_url=h.entity.get("metadata", {}).get("blob_url", "")
                ) for h in hits[0]
            ]
            return SearchResponse(results=results)
        except Exception as e:
            raise ServiceError(f"SearchService failed: {e}")