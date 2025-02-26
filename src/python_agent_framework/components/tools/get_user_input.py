# tools/get_user_input.py

from core.tool import Tool, Parameter
from typing import Dict, Any


def get_user_input(user_prompt: str) -> str:
    """
    Prompt user for information.

    :param user_prompt: The information needed from the user.'
    :return: User response.
    """
    user_input = input(f'{user_prompt}: ')
    
    # Return the user input
    #return [{"role": "user", "content": user_input}]
    return user_input


tool = Tool(
    description="Get user input to gain clarity and eliminate ambiguity.",
    function=get_user_input,
    parameters=[
        Parameter(
            name="user_prompt",
            type="string",
            description="The information needed from the user.",
            required=True
        )
    ],
    metadata={
        "author": "Nathan Angstadt",
        "version": "1.0",
        "category": "Maps",
    }
)