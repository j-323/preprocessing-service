import textstat
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

class LexicalRichnessAnalyzer(BaseTool):
    name = "lexical_richness_analyzer"
    async def run(self, text: str, metadata: dict):
        try:
            toks = [w.lower() for w in text.split() if w.isalpha()]
            tot = len(toks); uni = len(set(toks))
            lengths = [len(w) for w in toks] or [0]
            metadata["lexical"] = {
                "total_tokens": tot,
                "unique_tokens": uni,
                "type_token_ratio": uni/tot if tot else 0,
                "avg_word_length": sum(lengths)/len(lengths),
                "flesch_reading_ease": textstat.flesch_reading_ease(text)
            }
            return text, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")