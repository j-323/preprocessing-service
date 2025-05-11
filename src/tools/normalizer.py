# src/tools/advanced_normalizer.py
import unicodedata
import contractions
import langdetect
import spacy
from spacy.lang.en.stop_words import STOP_WORDS as EN_STOP
from spacy.lang.ru.stop_words import STOP_WORDS as RU_STOP
from typing import Tuple, Dict, Any
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

# Предзагружаем модели SpaCy для English и Russian
nlp_en = spacy.load("en_core_web_sm", disable=["parser", "ner"])
nlp_ru = spacy.load("ru_core_news_sm", disable=["parser", "ner"])

class Normalizer(BaseTool):
    name = "normalizer"

    async def run(self, text: str, metadata: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        try:
            # 1) Unicode нормализация
            text_norm = unicodedata.normalize("NFKC", text)

            # 2) Детект языка
            lang = langdetect.detect(text_norm)
            metadata["language"] = lang

            # 3) Развёртка сокращений для английского
            if lang.startswith("en"):
                text_norm = contractions.fix(text_norm)
                nlp = nlp_en
                stop_words = EN_STOP
            elif lang.startswith("ru"):
                nlp = nlp_ru
                stop_words = RU_STOP
            else:
                # для прочих языков просто ставим English-модель без стоп-слов
                nlp = nlp_en
                stop_words = set()

            # 4) Лемматизация и фильтрация
            doc = nlp(text_norm)
            tokens: list[str] = []
            for token in doc:
                lemma = token.lemma_.lower().strip()
                if (
                    lemma
                    and lemma not in stop_words
                    and not token.is_punct
                    and not token.is_space
                    and not token.like_num
                    and len(lemma) > 1
                ):
                    tokens.append(lemma)

            # 5) Сохраняем в metadata и возвращаем новую строчку
            metadata["normalized_tokens"] = tokens
            normalized_text = " ".join(tokens)
            return normalized_text, metadata

        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")