# core/agent_flow.py

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any, Callable, Union
import asyncio
from core.agent import Agent
from components.connections import Connection, CONNECTIONS


@dataclass
class AgentFlow(ABC):
    """
    Base class for all agent flows.
    Represents a structured flow executed by an agent.
    """
    name: Optional[str] = field(default="")
    description: str = None
    connection_name: str = None  # Name of the connection to be used
    connection: Optional[Connection] = field(init=False, default=None)  # This will be set dynamically
    guidelines: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=lambda: {
        "author": "",
        "version": "1.0",
        "category": "",
    })
    
    
    def __post_init__(self):
        if self.connection_name:
            """Set the connection attribute based on connection_name."""
            self.connection = CONNECTIONS.get(self.connection_name)
            if self.connection is None:
                raise ValueError(f"Model connection '{self.connection_name}' not found in registered connections.")

    
    
    @abstractmethod
    async def execute(self, agent: Agent) -> Any:
        """Abstract method to be implemented by concrete agent flows."""
        pass