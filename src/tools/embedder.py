from transformers import AutoTokenizer, AutoModel
import torch
from src.tools.base import BaseTool

class Embedder(BaseTool):
    name = "embedder"

    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    async def run(self, text: str, metadata: dict) -> tuple[str, dict]:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            out = self.model(**inputs, return_dict=True)
            emb = out.last_hidden_state.mean(dim=1).squeeze().tolist()
        metadata["embedding"] = emb
        return text, metadata