# core/tool_manager.py

from openai.types.chat.chat_completion_message import ChatCompletionMessage
import asyncio
import json
import logging
from typing import List, Dict, Any
from components.tools import TOOLS  # Import the registered tools dictionary


# Configure logging
logger = logging.getLogger(__name__)


class ToolManager:
    @staticmethod
    async def invoke_tools(tool_calls: List[ChatCompletionMessage]) -> List[Dict[str, Any]]:
        """
        Asynchronously invokes tool functions based on tool call messages.

        :param tool_calls: List of tool call messages from assistant.
        :return: List of tool response messages.
        """
        

        async def invoke_tool(tool_call: ChatCompletionMessage) -> Dict[str, Any]:
            tool_name = tool_call.function.name.lower().replace(" ", "_")  # Normalize tool name
            arguments = tool_call.function.arguments  # Expected to be a dict or JSON string

            logger.info(f"Invoking tool: {tool_name} with arguments: {arguments}")

            tool = TOOLS.get(tool_name)
            if not tool:
                error_msg = f"Tool '{tool_name}' not found."
                logger.error(error_msg)
                return {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": error_msg,
                }

            # Parse JSON arguments if necessary
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                    logger.debug(f"Parsed arguments for tool '{tool_name}': {arguments}")
                except json.JSONDecodeError:
                    error_msg = f"Invalid JSON format for tool '{tool_name}': {arguments}"
                    logger.error(error_msg)
                    return {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": error_msg,
                    }

            # Validate arguments format
            if not isinstance(arguments, dict):
                error_msg = f"Invalid arguments type for tool '{tool_name}'. Expected dict, got {type(arguments).__name__}"
                logger.error(error_msg)
                return {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": error_msg,
                }

            try:
                # Call the tool function dynamically
                tool_function = tool.function
                if asyncio.iscoroutinefunction(tool_function):
                    result = await tool_function(**arguments)
                else:
                    result = tool_function(**arguments)

                logger.debug(f"Tool '{tool_name}' executed successfully.")
            except Exception as e:
                result = f"Error executing tool '{tool_name}': {str(e)}"
                logger.error(result, exc_info=True)

            # Ensure response is a valid string
            formatted_result = ToolManager._format_tool_response(result)
            
            return {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": formatted_result,
            }

        # Execute all tool calls concurrently
        return await asyncio.gather(*(invoke_tool(tool_call) for tool_call in tool_calls))
    
    
    @staticmethod
    def _format_tool_response(response: Any) -> str:
        """
        Ensures that tool responses are always a valid string.
        - If it's a dictionary or list, converts it to a compact JSON string.
        - If it's already a string, returns it as-is.
        - Otherwise, converts the response to a string.
        """
        if isinstance(response, (dict, list)):
            return json.dumps(response, separators=(',', ':'))  # Compact JSON format
        
        return str(response)  # Convert everything else to string
    
    
    @staticmethod
    def tools() -> List[Dict[str, Any]]:
        """
        Generates a list of tool definitions in the correct format.

        :return: A list of tool definitions.
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.get_parameters_schema(),
                }
            }
            for tool in TOOLS.values()
        ]
        
        
    @staticmethod
    def selected_tools(tool_names: List[str]) -> List[Dict[str, Any]]:
        """
        Generates a list of only the selected tool definitions.

        :param tool_names: A list of tool names to filter.
        :return: A list of selected tool definitions.
        """
        selected_tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.get_parameters_schema(),
                }
            }
            for name, tool in TOOLS.items() if name in tool_names
        ]
        return selected_tools