import asyncio
from typing import List, Dict, Any, Tuple
from src.tools.loader import discover_tools
from src.core.exceptions import PipelineError
from src.logger import logger

class Pipeline:
    def __init__(self, tools: List = None):
        import src.tools as pkg
        self.tools = tools or discover_tools(pkg)
        logger.info("Pipeline init", tools=[t.name for t in self.tools])

    async def run(self, text: str, metadata: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        try:
            for tool in self.tools:
                logger.debug("Tool run", tool=tool.name)
                text, metadata = await tool.run(text, metadata)
            return text, metadata
        except Exception as e:
            logger.error("Pipeline error", error=str(e))
            raise PipelineError(e)