import typing as tp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from ...config import Config


class BaseTgClient:

    def __init__(self):
        self.application = ApplicationBuilder().token(Config.TG_BOT_TOKEN).build()
        # TODO: refactoring
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("new", self.clear_history_for_chat))


    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! . Спроси меня что-нибудь!")


    async def new(update: Update, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError("Implemented in the nearest future")
        # TODO: очистить контент чата
    
    async def clear_history_for_chat(chat_id):  #TODO: add functionality when add Redis storage
        raise NotImplementedError("Implemented in the nearest future")





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


    # def process_text_message(text, chat_id) -> str:
    #     model = "gpt-3.5-turbo"

    #     # Чтение текущей истории чата
    #     history = []


    #     history.append({"role": "user", "content": text})

    #     try:
    #         chat_completion = client.chat.completions.create(
    #             model=model, messages=history
    #         )
    #     except Exception as e:
    #         raise e

    #     ai_response = chat_completion.choices[0].message.content

    #     return ai_response