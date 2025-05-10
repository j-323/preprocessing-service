import spacy
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

nlp_temp = spacy.load("en_core_web_sm", disable=["parser","tagger"])

class TemporalEntityExtractor(BaseTool):
    name = "temporal_entity_extractor"
    async def run(self, text: str, metadata: dict):
        try:
            ents=[]
            for ent in nlp_temp(text).ents:
                if ent.label_ in {"DATE","TIME"}:
                    ents.append({"text":ent.text,"label":ent.label_,"span":(ent.start_char,ent.end_char)})
            metadata["temporal_entities"]=ents
            return text, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")