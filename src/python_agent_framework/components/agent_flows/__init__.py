# agent_flows/__init__.py

import importlib
import pkgutil
from typing import Dict, Any, List
from core.agent_flow import AgentFlow

# Dictionary to hold registered agent_flows
AGENT_FLOWS: Dict[str, AgentFlow] = {}


def register_agent_flows():
    """
    Dynamically finds and registers all predefined Agent_Flow instances.
    """
    package_name = __name__

    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{package_name}.{module_name}")

        # Look for pre-instantiated Agent_Flow objects in the module
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, AgentFlow):
                if not attr.name:  # Assign module name as default name if missing
                    attr.name = module_name
                AGENT_FLOWS[attr.name.lower().replace(" ", "_")] = attr  # Normalize name


# Load agent flows when the package is imported
register_agent_flows()