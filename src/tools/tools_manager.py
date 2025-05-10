from src.tools.loader import discover_tools
from src.core.exceptions import ToolError

class ToolsManager:
    def __init__(self, enabled: list[str] = None):
        all_t = {t.name:t for t in discover_tools(__import__("src.tools", fromlist=["."]))}
        if enabled:
            missing=[n for n in enabled if n not in all_t]
            if missing: raise ToolError(f"Tools not found: {missing}")
            self.tools=[all_t[n] for n in enabled]
        else:
            self.tools=list(all_t.values())

    def list_tools(self) -> list[str]:
        return [t.name for t in self.tools]

    def get_pipeline_tools(self):
        return self.tools