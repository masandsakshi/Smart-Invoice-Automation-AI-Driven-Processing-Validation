# utilities/pretty_print_conversation.py

import inspect
from typing import Any, Dict, List

from termcolor import colored
from pydantic import BaseModel


def object_to_dict(obj: Any) -> Dict[str, Any]:
    """
    Convert various objects to a dictionary.

    :param obj: The object to convert.
    :return: Dictionary representation of the object.
    """
    obj_dict = {}

    if isinstance(obj, dict):
        obj_dict = obj
    elif isinstance(obj, BaseModel):
        obj_dict = obj.model_dump()
    else:
        # Handle objects with __dict__
        if hasattr(obj, "__dict__"):
            obj_dict.update(obj.__dict__)

        # Handle objects with __slots__
        if hasattr(obj, "__slots__"):
            for slot in obj.__slots__:
                obj_dict[slot] = getattr(obj, slot)

        # Use inspect to get all properties and other attributes
        for name, value in inspect.getmembers(obj):
            if (
                not name.startswith("_")  # Exclude private and special attributes
                and not inspect.isroutine(value)  # Exclude methods
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.ismethod(value)
            ):
                obj_dict[name] = value

    return obj_dict


def pretty_print_conversation(messages: List[Dict[str, Any]]):
    """
    Print the conversation with colored roles.

    :param messages: List of message dictionaries.
    """
    role_to_color = {
        "system": "cyan",
        "user": "green",
        "assistant": "blue",
        "tool": "magenta",
        "unknown": "red",
    }
    
    for message in messages:
        message = object_to_dict(message)
        
        role = message.get("role", "unknown")
        color = role_to_color.get(role, "red")
        content = ""

        if role in ["system", "user"]:
            content = message.get("content", "")
            print(colored(f"{role}: {content}\n", color))
        elif role == "assistant" and message.get("tool_calls"):
            for tool_message in message.get("tool_calls"):            
                id = tool_message['id']
                name = tool_message['function']['name']
                arguments = tool_message['function']['arguments']
                print(colored(f"{role}: {id}\n{name} {arguments}\n", color))            
        elif role == "assistant":
            content = message.get("content", "")
            print(colored(f"{role}: {content}\n", color))            
        elif role == "tool":
            tool_call_id = message.get("tool_call_id", "")
            name = message.get("name", "")
            tool_content = message.get("content", "")
            content = f"{tool_call_id}\n{name}: {tool_content}"
            print(colored(f"{role}: {content}\n", color))
        else:
            content = message.get("content", "")
            print(colored(f"{role}: {content}\n", role_to_color["unknown"]))