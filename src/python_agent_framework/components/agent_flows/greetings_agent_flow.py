
# agent_flows/geteeting_flow.py

from core.agent_flow import AgentFlow
from core.agent import Agent
from dataclasses import dataclass, field
import asyncio


@dataclass
class GreetingsAgentFlow(AgentFlow):
    async def execute(self, agent: Agent) -> str:
        await asyncio.sleep(1)  # Simulate async processing
        return f"Hello! I am {agent.name}, your AI assistant.\nI see your question: {agent.user_inputs}"


agent_flow = GreetingsAgentFlow(description="An agent flow that sends a greeting message.")