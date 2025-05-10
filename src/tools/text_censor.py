from aho_corasick import Automaton
from src.tools.base import BaseTool
from src.core.exceptions import ToolError

class TextCensor(BaseTool):
    name = "text_censor"
    BAD_WORDS = ["fuck", "shit", "bitch"]

    def __init__(self):
        self.automaton = Automaton()
        for w in self.BAD_WORDS:
            self.automaton.add_word(w, w)
        self.automaton.make_automaton()

    async def run(self, text: str, metadata: dict) -> tuple[str, dict]:
        try:
            result, last = [], 0
            for end, word in self.automaton.iter(text.lower()):
                start = end - len(word) + 1
                result.append(text[last:start])
                result.append("*" * len(word))
                last = end + 1
            result.append(text[last:])
            return "".join(result), metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")