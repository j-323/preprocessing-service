class ToolError(Exception):
    """Ошибка внутри одного шага пайплайна."""

class PipelineError(Exception):
    """Ошибка в orchestration пайплайна."""

class ServiceError(Exception):
    """Ошибка сервисного слоя (embed/search)."""