import logging
import typing as tp

from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from telegram import Update

# TODO: relocate to controllers
from ..tg.clients import BaseTgClient
from ..config import Config

# import brewuser.projects.tg.tg_project.app.schema as schema  # TODO: make relative path
from .. import schema as schema # TODO: make relative path

if tp.TYPE_CHECKING:
    from tg_project.app import Application # ?

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/operations", tags=["Operations"])

# TODO: add schema, such like that:
# @router.post(
#     "/clone/{model_key}",
#     summary="Клонирует модель в storage с новым ключом",
#     description="Клонирует модель | Чтобы воспользоваться этой функции, необходимо делегировать секрет сервису Sandbox: https://docs.yandex-team.ru/sandbox/dev/secret#delegate-secret",
#     response_model=schema.operations.CloneResponse,
# )
# async def clone_model(
#     request: Request,
#     data: schema.operations.CloneModelRequest = Depends(),
# )

@router.on_event("startup")
async def startup_event():
    await BaseTgClient.application.initialize()


@router.post("/query")
async def webhook(request: Request):
    try:
        update = Update.de_json(await request.json(), BaseTgClient.application.bot)
    except Exception as e:
        logging.error(f"Error parsing update: {e}")
        return JSONResponse(content={"status": "505"})
    
    logging.info(update)
    if update.message is not None and update.message.from_user.username.lower() in Config.TG_BOT_CHATS:
        await BaseTgClient.application.process_update(update)

    return JSONResponse(content={"status": "ok"})
