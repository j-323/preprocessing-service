import spacy
from src.tools.base import BaseTool
from src.models.domain import Entity

ner_nlp = spacy.load("en_core_web_sm", disable=["parser"])

class NER(BaseTool):
    name = "ner"

    async def run(self, text: str, metadata: dict) -> tuple[str, dict]:
        doc = ner_nlp(text)
        metadata["entities"] = [
            Entity(text=ent.text, label=ent.label_, start=ent.start_char, end=ent.end_char).dict()
            for ent in doc.ents
        ]
        return text, metadata