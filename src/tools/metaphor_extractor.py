# src/tools/metaphor_extractor.py

import re
import spacy
from typing import Tuple, Dict, Any, List
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

# Загружаем модель SpaCy один раз
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])  # включаем парсер для зависимостей

class MetaphorExtractor(BaseTool):
    """
    Улучшенный экстрактор метафор:
      - синтаксический анализ через SpaCy для обнаружения конструкций "X is a Y" и "X feels like Y"
      - доп. regex-рейдбэк для нестандартных форм
    """

    name = "metaphor_extractor"

    # Паттерны для regex-анализа
    _regex_patterns = [
        re.compile(r"\b([A-Z][a-z]+)\s+is\s+a[n]?\s+([a-z]+)", re.IGNORECASE),
        re.compile(r"\b([A-Z][a-z]+)\s+feels?\s+like\s+([a-z]+)", re.IGNORECASE),
    ]

    async def run(self, text: str, metadata: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        try:
            metaphors: List[Dict[str, Any]] = []

            # 1) Синтаксический парсинг через SpaCy:
            doc = nlp(text)
            for sent in doc.sents:
                # ищем nsubj → cop → attr/acomp
                for token in sent:
                    if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
                        cop = token.head
                        if cop.lemma_ in {"be", "feel"}:
                            for child in cop.children:
                                if child.dep_ in {"attr", "acomp", "oprd"}:
                                    metaphors.append({
                                        "subject": token.text,
                                        "predicate": cop.text,
                                        "metaphor": child.text,
                                        "method": "dependency",
                                        "span": (token.idx, child.idx + len(child.text))
                                    })

            # 2) Regex fallback для простых случаев
            for pattern in self._regex_patterns:
                for m in pattern.finditer(text):
                    metaphors.append({
                        "subject": m.group(1),
                        "metaphor": m.group(2),
                        "method": "regex",
                        "span": m.span()
                    })

            # Убираем дубликаты
            seen = set()
            unique = []
            for obj in metaphors:
                key = (obj["subject"], obj["metaphor"], obj["method"], obj["span"])
                if key not in seen:
                    seen.add(key)
                    unique.append(obj)

            metadata["metaphors"] = unique
            return text, metadata

        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")
