from transformers import pipeline as hf_pipeline
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

class Summarizer(BaseTool):
    name = "summarizer"
    def __init__(self, model_name="sshleifer/distilbart-cnn-12-6"):
        self.pipe = hf_pipeline("summarization", model=model_name)
    async def run(self, text: str, metadata: dict):
        try:
            sm = self.pipe(text, max_length=60, min_length=20, do_sample=False)
            metadata["summary"] = sm[0]["summary_text"]
            return text, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")