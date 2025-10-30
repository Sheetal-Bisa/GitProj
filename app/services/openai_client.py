import os
from openai import OpenAI


class ChatGPTClient:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set in environment variables.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[CHATGPT ERROR] {e}"


# Module-level singleton for reuse across the app
_client: ChatGPTClient | None = None


def get_client(model: str = "gpt-3.5-turbo") -> ChatGPTClient:
    """Return a singleton ChatGPTClient instance.

    This function mirrors the former `get_client` that used to live in the
    `gemini` module so `app.main` can call it on startup.
    """
    global _client
    if _client is None:
        _client = ChatGPTClient(model=model)
    return _client
