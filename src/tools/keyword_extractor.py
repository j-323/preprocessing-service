from rake_nltk import Rake
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

class KeywordExtractor(BaseTool):
    name = "keyword_extractor"
    def __init__(self, max_terms=10):
        self.rake = Rake(); self.max_terms = max_terms
    async def run(self, text: str, metadata: dict):
        try:
            self.rake.extract_keywords_from_text(text)
            metadata["keywords"] = self.rake.get_ranked_phrases()[:self.max_terms]
            return text, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")