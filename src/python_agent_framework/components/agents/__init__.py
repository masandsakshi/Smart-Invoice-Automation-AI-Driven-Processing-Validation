# agents/__init__.py

import importlib
import pkgutil
from typing import Dict, Any, List
from core.agent import Agent

# Dictionary to hold registered agents
AGENTS: Dict[str, Agent] = {}


def load_agents():
    """
    Dynamically finds and registers all predefined Agent instances.
    """
    package_name = __name__

    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{package_name}.{module_name}")

        # Look for pre-instantiated Agent objects in the module
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, Agent):
                if not attr.name:
                    attr.name = module_name  # Assign module name as default name if missing
                AGENTS[attr.name.lower().replace(" ", "_")] = attr  # Normalize name


# Load agents when the package is imported
load_agents()