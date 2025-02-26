# core/memory.py

from typing import Any, Dict, List, Optional


class Memory:
    """
    Manages the conversation history.
    """

    def __init__(self, initial_messages: Optional[List[Dict[str, Any]]] = None):
        self.messages: List[Dict[str, Any]] = initial_messages if initial_messages else []

    def add_role_content_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        
    def add_message(self, message: str):
        self.messages.append(message)


    def add_tool_message(self, tool_call_id: str, name: str, content: str):
        self.messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": name,
            "content": content
        })


    def get_messages(self) -> List[Dict[str, Any]]:
        return self.messages


    def clear(self):
        self.messages = []