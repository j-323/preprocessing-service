from transformers import pipeline as hf_pipeline
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

class EmotionClassifier(BaseTool):
    name = "emotion_classifier"
    def __init__(self, model_name="j-hartmann/emotion-english-distilroberta-base"):
        self.clf = hf_pipeline("text-classification", model=model_name, return_all_scores=True)
    async def run(self, text: str, metadata: dict):
        try:
            scores = self.clf(text)[0]
            metadata["emotions"] = sorted(scores, key=lambda x: x["score"], reverse=True)[:3]
            return text, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")