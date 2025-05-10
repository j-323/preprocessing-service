from bs4 import BeautifulSoup
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

class TextCleaner(BaseTool):
    name = "text_cleaner"

    async def run(self, text: str, metadata: dict) -> tuple[str, dict]:
        try:
            clean = BeautifulSoup(text, "lxml").get_text(separator=" ")
            clean = " ".join(clean.split())
            return clean, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")