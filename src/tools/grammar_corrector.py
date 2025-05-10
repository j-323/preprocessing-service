import language_tool_python
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

class GrammarCorrector(BaseTool):
    name = "grammar_corrector"
    def __init__(self, lang="en-US"):
        self.tool = language_tool_python.LanguageTool(lang)
    async def run(self, text: str, metadata: dict):
        try:
            corr = self.tool.correct(text)
            metadata["grammar_corrected"] = corr
            return corr, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")