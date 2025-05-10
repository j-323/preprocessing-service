import textstat
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

class ComplexityAnalyzer(BaseTool):
    name = "complexity_analyzer"
    async def run(self, text: str, metadata: dict):
        try:
            metadata["complexity"]={
                "dale_chall": textstat.dale_chall_readability_score(text),
                "gunning_fog": textstat.gunning_fog(text),
                "smog_index": textstat.smog_index(text),
                "coleman_liau": textstat.coleman_liau_index(text),
            }
            return text, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")