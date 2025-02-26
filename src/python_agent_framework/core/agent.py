# core/agent.py

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
import asyncio
from core.memory import Memory

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from components.agent_flows import AgentFlow, AGENT_FLOWS


@dataclass
class Agent:
    name: Optional[str] = field(default="")
    role: List[str] = field(default_factory=list)
    guidelines: List[str] = field(default_factory=list)
    tools: List[str] =  field(default_factory=list)
    agent_flow_name: str = None  # Name of the agent flow to be used
    agent_flow: Optional["AgentFlow"] = field(init=False)  # This will be set dynamically
    
    
    def __post_init__(self):
        """Retrieve the agent flow."""
        from components.agent_flows import AGENT_FLOWS
        self.agent_flow = AGENT_FLOWS.get(self.agent_flow_name)
        if self.agent_flow is None:
            raise ValueError(f"Agent flow '{self.agent_flow_name}' not found in registered agent flows.")
        
        self.reset()
    
    
    def reset(self):
        """Resets the agent's state."""
        system_prompts = []
        system_prompts.extend([{"role": "system", "content": content} for content in self.role])
        system_prompts.extend([{"role": "system", "content": content} for content in self.agent_flow.guidelines])
        system_prompts.extend([{"role": "system", "content": content} for content in self.guidelines])
        self.memory = Memory(initial_messages=system_prompts)
    
    
    async def run_conversation(self, user_inputs: List[Dict[str, Any]]) -> str:
        """Asynchronously executes the assigned agent flow."""
        self.user_inputs = user_inputs
        if self.agent_flow:
            return await self.agent_flow.execute(self)
        raise ValueError("No agent flow assigned to this agent.")