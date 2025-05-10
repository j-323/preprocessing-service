import re
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

class MetaphorExtractor(BaseTool):
    name = "metaphor_extractor"
    pat = r"\b([A-Z][a-z]+)\s+is\s+a[n]?\s+([a-z]+)"
    async def run(self, text: str, metadata: dict):
        try:
            mets=[]
            for m in re.finditer(self.pat, text):
                mets.append({"subject":m.group(1),"metaphor":m.group(2),"span":m.span()})
            metadata["metaphors"]=mets
            return text, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")