# core/connection.py

from dataclasses import dataclass, field
from typing import Optional, Dict
import os
from dotenv import load_dotenv


@dataclass
class Connection:
    name: Optional[str] = field(default="")
    base_url: str = None
    model: str = None
    api_key: str = None
    
    
    def __post_init__(self):
            """Replace placeholder API key with the actual value from the environment."""
            load_dotenv()
            if self.api_key in os.environ:
                self.api_key = os.getenv(self.api_key)  # Get the actual key value    