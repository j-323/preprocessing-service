import pkgutil
import importlib
from typing import List
from src.tools.base import BaseTool

def discover_tools(package) -> List[BaseTool]:
    tools: List[BaseTool] = []
    prefix = f"{package.__name__}."
    for _, modname, _ in pkgutil.iter_modules(package.__path__, prefix):
        module = importlib.import_module(modname)
        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, type) and issubclass(obj, BaseTool) and obj is not BaseTool:
                tools.append(obj())
    return tools