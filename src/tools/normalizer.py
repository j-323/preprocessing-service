import spacy
from src.tools.base import BaseTool

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

class Normalizer(BaseTool):
    name = "normalizer"

    async def run(self, text: str, metadata: dict) -> tuple[str, dict]:
        doc = nlp(text)
        lemmas = [token.lemma_.lower() for token in doc if not token.is_punct]
        return " ".join(lemmas), metadata