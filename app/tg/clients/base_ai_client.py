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
        self.model = "gpt-3.5-turbo"

    async def process_text_message(self, text: str, model: tp.Optional[str] = None) -> str:
        # TODO: Чтение текущей истории чата
        history = []
        history.append({"role": "user", "content": text})  # TODO: add roles
        
        try:
            if not model:
                model = self.model
            chat_completion = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=model,
                messages=history
            )

        except Exception as e:
            raise e

        return chat_completion.choices[0].message.content
