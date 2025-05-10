from transformers import pipeline as hf_pipeline
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

class SarcasmDetector(BaseTool):
    name = "sarcasm_detector"
    def __init__(self, model_name="mohammadmahmor/sarcasm-detection"):
        self.clf = hf_pipeline("text-classification", model=model_name)
    async def run(self, text: str, metadata: dict):
        try:
            out = self.clf(text)[0]
            metadata["sarcasm"]={"label":out["label"],"score":float(out["score"])}
            return text, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")