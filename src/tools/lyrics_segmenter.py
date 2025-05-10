import re
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

class LyricsSegmenter(BaseTool):
    name = "lyrics_segmenter"
    async def run(self, text: str, metadata: dict):
        try:
            parts = re.split(r'\n{2,}', text.strip())
            metadata["segments"] = [
                {"id": i+1, "lines": [l.strip() for l in p.splitlines() if l.strip()]}
                for i,p in enumerate(parts)
            ]
            return text, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")