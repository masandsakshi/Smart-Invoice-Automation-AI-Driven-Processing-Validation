# connections/openai_gpt35turbo.py

from core.connection import Connection


openai_gpt4o = Connection(
    base_url = "https://api.openai.com/v1/chat/completions",
    model = "gpt-3.5-turbo",
    api_key = "OPENAI_API_KEY"
)