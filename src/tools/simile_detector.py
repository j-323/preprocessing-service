import re
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

class SimileDetector(BaseTool):
    name = "simile_detector"
    patterns = [r"\blike a[n]?\s+([a-z]+)", r"\bas\s+([a-z]+)\s+as\s+([a-z]+)"]
    async def run(self, text: str, metadata: dict):
        try:
            found=[]
            for p in self.patterns:
                for m in re.finditer(p, text, flags=re.IGNORECASE):
                    found.append({"pattern":p, "matches":m.groups(), "span":m.span()})
            metadata["similes"]=found
            return text, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")