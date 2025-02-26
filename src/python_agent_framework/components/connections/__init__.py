# connections/__init__.py

import importlib
import pkgutil
from typing import Dict, Any, List
from core.connection import Connection


# Dictionary to hold registered connections
CONNECTIONS: Dict[str, Connection] = {}

def load_connections():
    """
    Dynamically finds and registers all predefined Connection instances.
    """
    package_name = __name__

    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{package_name}.{module_name}")

        # Look for pre-instantiated Connection objects in the module
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, Connection):
                if not attr.name:  
                    attr.name = module_name  # Assign module name as default name if missing
                CONNECTIONS[attr.name.lower().replace(" ", "_")] = attr  # Normalize name

# Load connections when the package is imported
load_connections()