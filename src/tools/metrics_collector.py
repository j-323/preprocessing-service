import time
from prometheus_client import Counter, Histogram
from src.tools.base import BaseTool

_TOOL_DURATION = Histogram("tool_duration_seconds", "Time per tool", ["tool"])
_TOOL_ERRORS   = Counter("tool_errors_total",    "Errors per tool", ["tool"])

class MetricsCollector(BaseTool):
    name = "metrics_collector"
    async def run(self, text: str, metadata: dict):
        # метрики собираются обёрткой pipeline, здесь заглушка
        return text, metadata