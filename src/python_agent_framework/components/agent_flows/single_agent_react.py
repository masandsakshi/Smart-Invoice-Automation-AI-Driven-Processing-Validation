
# agent_flows/react.py

from core.agent_flow import AgentFlow
from core.agent import Agent
from core.memory import Memory
from core.tool_manager import ToolManager
from llm.chat_completion import ChatCompletionHandler
from utilities.pretty_print_conversation import pretty_print_conversation
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import asyncio


@dataclass
class SingleAgentReAct(AgentFlow):    
    max_iterations: int = 5
    
    
    async def execute(self, agent: Agent) -> str:
        chat_handler = ChatCompletionHandler(base_url=self.connection.base_url,
                                             api_key=self.connection.api_key,
                                             model=self.connection.model)
        assistant_message = None
        
        for user_input in agent.user_inputs:
            # Add the user prompt to memory
            agent.memory.add_message(user_input)

            # Make chat completion request
            chat_response = chat_handler.chat_completion_request(
                messages=agent.memory.get_messages(),
                tools=ToolManager.selected_tools(agent.tools),
            )
            assistant_message = chat_response.choices[0].message
            
            # Add the assistant's content to memory
            agent.memory.add_message(assistant_message)

            # Check for tool calls and invoke tools if necessary
            if assistant_message.tool_calls:
                iterations = 0
                while assistant_message.tool_calls and (iterations := iterations + 1) <= self.max_iterations:
                    tool_messages = await ToolManager.invoke_tools(assistant_message.tool_calls)
                    for tool_message in tool_messages:
                        # Add each tool message to memory
                        agent.memory.add_message(tool_message)
                    
                    chat_response = chat_handler.chat_completion_request(
                        messages=agent.memory.get_messages(),
                        tools=ToolManager.selected_tools(agent.tools),
                    )
                    assistant_message = chat_response.choices[0].message        
                    
                    # Directly add the assistant's content to memory without conversion
                    agent.memory.add_message(assistant_message)   
              
            pretty_print_conversation(agent.memory.get_messages())  
            return assistant_message.content


agent_flow = SingleAgentReAct(description =
                    """
                    ReAct pattern (Reason + Act)
                        Think - LLM
                        Action - Invoke tool
                        Observe - Tool response
                        Repeat - Repeat until finished
                    """,
                    connection_name = "openai_gpt4o",
                    guidelines = [
                        """
                        Strictly follow all guidleines. It is mandatory that you reflect on all guidleines before returning a response.
                        Guidelines
                            1. You should follow the ReAct agent pattern (Reason + Act) when generating a response.
                                Pattern:
                                    Think - using your interanl reasoning.
                                    Action - Invoke tools to get information, including additional human input.
                                    Observe - Process tool response using your internal reasoning.
                                    Repeat - Repeat until finished.
                            2. Do not guess or infer tool arguments except for the following reasons:
                                You are given specific guidance on infering a tool argunent.
                                You have previous context to make a reasonable assumption.
                        """
                    ]
                )