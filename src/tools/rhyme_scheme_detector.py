import re, pronouncing
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

class RhymeSchemeDetector(BaseTool):
    name = "rhyme_scheme_detector"
    async def run(self, text: str, metadata: dict):
        try:
            lines = [l for l in text.splitlines() if l.strip()]
            ends = []
            for ln in lines:
                w = re.findall(r"\b\w+\b", ln.lower())
                last = w[-1] if w else ""
                phones = pronouncing.phones_for_word(last)
                rp = pronouncing.rhyming_part(phones[0]) if phones else last
                ends.append(rp)
            scheme, m, lbl = [], {}, ord('A')
            for p in ends:
                if p not in m:
                    m[p] = chr(lbl); lbl+=1
                scheme.append(m[p])
            metadata["rhyme_scheme"] = "".join(scheme)
            return text, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")