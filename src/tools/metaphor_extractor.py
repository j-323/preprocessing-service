# src/tools/metaphor_extractor.py

import re
import spacy
import logging
from typing import Tuple, Dict, Any, List
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

logger = logging.getLogger(__name__)

# Загружаем SpaCy однажды, отключаем только ner
nlp = spacy.load("en_core_web_sm", disable=["ner"])

class MetaphorExtractor(BaseTool):
    """
    Улучшенный экстрактор метафор:
      • синтаксический анализ через SpaCy
      • два этапа: dependency-парсинг и regex-фоллбек
      • рефакторинг на приватные методы для удобства тестирования
    """

    name = "metaphor_extractor"

    # прекомпилированные regex-паттерны
    _regex_patterns = [
        re.compile(r"\b([A-Z][a-z]+)\s+is\s+a[n]?\s+([a-z]+)", re.IGNORECASE),
        re.compile(r"\b([A-Z][a-z]+)\s+feels?\s+like\s+([a-z]+)", re.IGNORECASE),
    ]

    # глаголы-связки и зависимости-атрибуты
    _COPULAS = {"be", "feel"}
    _ATTR_DEPS = {"attr", "acomp", "oprd"}

    async def run(self, text: str, metadata: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        try:
            deps = self._extract_via_dependency(text)
            regs = self._extract_via_regex(text)
            all_metaphors = deps + regs
            metadata["metaphors"] = self._dedupe(all_metaphors)
            return text, metadata

        except Exception as e:
            logger.exception("MetaphorExtractor failed")
            raise ToolError(f"{self.name} failed: {e}")

    def _extract_via_dependency(self, text: str) -> List[Dict[str, Any]]:
        metaphors: List[Dict[str, Any]] = []
        doc = nlp(text)
        for sent in doc.sents:
            for token in sent:
                # находим субъект + связку-copula
                if token.dep_ == "nsubj" and token.head.lemma_ in self._COPULAS:
                    cop = token.head
                    for child in cop.children:
                        if child.dep_ in self._ATTR_DEPS:
                            metaphors.append({
                                "subject": token.text,
                                "predicate": cop.text,
                                "metaphor": child.text,
                                "method": "dependency",
                                "span": (token.idx, child.idx + len(child.text))
                            })
        return metaphors

    def _extract_via_regex(self, text: str) -> List[Dict[str, Any]]:
        metaphors: List[Dict[str, Any]] = []
        for pattern in self._regex_patterns:
            for m in pattern.finditer(text):
                metaphors.append({
                    "subject": m.group(1),
                    "metaphor": m.group(2),
                    "method": "regex",
                    "span": m.span()
                })
        return metaphors

    def _dedupe(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        unique = []
        for obj in items:
            key = (obj["subject"], obj["metaphor"], obj["method"], obj["span"])
            if key not in seen:
                seen.add(key)
                unique.append(obj)
        return unique