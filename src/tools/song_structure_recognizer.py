import hashlib
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

class SongStructureRecognizer(BaseTool):
    name = "song_structure_recognizer"
    async def run(self, text: str, metadata: dict):
        try:
            segs = metadata.get("segments", [])
            counts = {}
            for s in segs:
                h = hashlib.md5("\n".join(s["lines"]).encode()).hexdigest()
                s["hash"] = h
                counts[h] = counts.get(h, 0) + 1
            metadata["structure"] = [
                {"id": s["id"], "type": "chorus" if counts[s["hash"]]>1 else "verse"}
                for s in segs
            ]
            return text, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")