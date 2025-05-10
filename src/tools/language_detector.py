from langdetect import detect
from src.tools.base import BaseTool

class LanguageDetector(BaseTool):
    name = "language_detector"

    async def run(self, text: str, metadata: dict) -> tuple[str, dict]:
        metadata["language"] = detect(text)
        return text, metadata