# llm/chat_completion.py

import os
from dotenv import load_dotenv
from typing import Any, Dict, List, Optional
from httpcore import URL
from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI
import logging


logging.getLogger("httpx").setLevel(logging.WARNING) 


class ChatCompletionHandler:
    """
    Handles chat completion requests to OpenAI.
    """

    def __init__(self, base_url: str = 'https://api.openai.com/v1/', api_key: str = None, model: str = "gpt-3.5-turbo"):
        if not api_key:
            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")
        
        self.client = OpenAI(api_key = api_key, base_url = base_url)
        self.model = model

    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def chat_completion_request(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Any] = None,
    ) -> Any:
        """
        Make a chat completion request to OpenAI.

        :param messages: List of messages in the conversation.
        :param tools: List of tools to provide to the assistant.
        :param tool_choice: Specific tool choice if needed.
        :return: OpenAI API response.
        """
        try:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,
            )
            return response
        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            raise e  # Let tenacity handle the retry