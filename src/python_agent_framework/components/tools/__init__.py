# tools/__init__.py

import importlib
import pkgutil
from typing import Dict, Any, List
from core.tool import Tool

# Dictionary to hold registered tools
TOOLS: Dict[str, Tool] = {}


def load_tools():
    """
    Dynamically discovers and registers all pre-instantiated Tool instances.
    """
    package_name = __name__

    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{package_name}.{module_name}")

        # Look for pre-instantiated Tool objects in the module
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, Tool):  # Registers all instances found
                if not attr.name:  
                    attr.name = module_name  # Assign module name as default name if missing
                TOOLS[attr.name.lower().replace(" ", "_")] = attr  # Normalize key name


# Load tools when the package is imported
load_tools()