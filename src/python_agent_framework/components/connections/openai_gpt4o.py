# connections/openai_gpt4o.py

from core.connection import Connection


openai_gpt4o = Connection(
    base_url = "https://api.openai.com/v1/",
    model = "gpt-4o",
    api_key = "OPENAI_API_KEY"
)