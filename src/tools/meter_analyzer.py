import pronouncing
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

class MeterAnalyzer(BaseTool):
    name = "meter_analyzer"
    async def run(self, text: str, metadata: dict):
        try:
            patterns = []
            for ln in text.splitlines():
                tokens = pronouncing.tokenize(ln)
                st = [pronouncing.stresses(w)[0] for w in tokens if pronouncing.stresses(w)]
                patterns.append("".join(st))
            metadata["meter_patterns"] = patterns
            return text, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")