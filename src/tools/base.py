from abc import ABC, abstractmethod
from typing import Tuple, Any, Dict

class BaseTool(ABC):
    """
    Базовый интерфейс для всех tools.
    """
    name: str

    @abstractmethod
    async def run(self, text: str, metadata: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        ...