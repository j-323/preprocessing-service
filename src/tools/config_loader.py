import yaml
from pathlib import Path
from src.core.exceptions import ToolError

def load_pipeline_config(path: str) -> list[str]:
    try:
        cfg = yaml.safe_load(Path(path).read_text())
        tools = cfg.get("tools")
        if not isinstance(tools, list):
            raise ToolError("`tools` must be list")
        return tools
    except Exception as e:
        raise ToolError(f"ConfigLoader failed: {e}")