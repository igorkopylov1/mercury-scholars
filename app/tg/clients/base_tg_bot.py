import typing as tp
from aiogram import Bot
import asyncio
from .base_ai_client import OpenAiClient

from ...config import Config


class BaseTgClient:
    def __init__(self, tg_bot_token: str, proxi_api_key: str,):
        self.bot = Bot(token=tg_bot_token)
        self.ai_client = OpenAiClient(proxi_api_key)
    
    async def send_chat_action(self, chat_id: int, action: str='typing')->None: # TODO: add enum
        await self.bot.send_chat_action(chat_id=chat_id, action=action)


    async def process_comand(self, chat_id: int, text: str) -> str:
        # TODO: ADD comands
        ai_response = await self.ai_client.process_text_message(text=text)
        await self.bot.send_message(chat_id, ai_response)





# async def get_s3_client():  # TODO: ADD CHAT HISTORY
#     session = aioboto3.Session(
#         aws_access_key_id=AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=AWS_SECRET_ACCESS_KEY
#     )
#     return session.client('s3')

# async def process_text_message(text, chat_id) -> str:
#     model = "gpt-3.5-turbo"

#     # Чтение текущей истории чата
#     s3client = await get_s3_client()
#     history = []
    
#     try:
#         history_object_response = await s3client.get_object(
#             Bucket=S3_BUCKET_NAME, Key=f"{chat_id}.json"
#         )
#         history = json.loads(await history_object_response["Body"].read())
#     except Exception:
#         pass

#     history.append({"role": "user", "content": text})

#     try:
#         chat_completion = await client.chat.completions.create(
#             model=model, messages=history
#         )
#     except Exception as e:
#         if type(e).__name__ == "BadRequestError":
#             clear_history_for_chat(chat_id)
#             return await process_text_message(text, chat_id)
#         else:
#             raise e

#     ai_response = chat_completion.choices[0].message.content
#     history.append({"role": "assistant", "content": ai_response})

#     # Save current chat history
#     try:
#         s3client = await get_s3_client()
#         async with s3client as client:
#             await client.put_object(
#                 Bucket=S3_BUCKET_NAME,
#                 Key=f"{chat_id}.json",
#                 Body=json.dumps(history),
#             )
#     except Exception:
#         pass

#     return ai_response
