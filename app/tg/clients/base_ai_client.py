import typing as tp
import openai
import asyncio



class OpenAiClient:
    BASE_URL = "https://api.proxyapi.ru/openai/v1"

    def __init__(self, proxy_token: str) -> None:
        self.client = openai.Client(
            api_key=proxy_token,
            base_url=self.BASE_URL,
        )
        self.model = "gpt-4o-mini"
        self.max_tokens = 400

    async def process_text_message(self, history: list[dict], model: tp.Optional[str] = None) -> str:        
        try:
            if not model:
                model = self.model
            chat_completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=model,
                messages=history,
                max_tokens=self.max_tokens
            )

        except Exception as e:
            raise e

        return chat_completion.choices[0].message.content
