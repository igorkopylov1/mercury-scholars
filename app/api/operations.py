import logging
import typing as tp

from fastapi import Depends, Request, Body
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi.exceptions import RequestValidationError

from telegram import Update

from .. import schema as schema

if tp.TYPE_CHECKING:
    from tg_project.app import Application

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/operations", tags=["Operations"])


@router.post("/query")
async def query(
    request: Request,
    # data: schema.operations.BaseRequest = Body()  # TODO: work with schema
) -> JSONResponse:
    app: Application = request.app.state.application
    data = await request.json()
    logger.info(f"Received data: {data}")

    if not data.get("message", None) or not data["message"].get("text", None):
        logger.info(f"Bad request: {data}")
        if data.get("my_chat_member", None):
            chat_id = data["my_chat_member"]["chat"]["id"]
            user_name = data["my_chat_member"]["chat"]["first_name"]
        elif data.get("message", None):
            chat_id = data["message"]["chat"]["id"]
            user_name = data["message"]["from"]["first_name"]
        else:
            logger.error("BAD SCHEMA!")
            return JSONResponse(content={"status": "ok"})
        error_status = await app.operation_controller.bad_response(chat_id=chat_id, user_name=user_name)
        return JSONResponse(content={"status": error_status})

    status = await app.operation_controller.create_response(chat_id=data["message"]["chat"]["id"], message_text=data["message"]["text"], user_name=data["message"]["from"]["first_name"])
    return JSONResponse(content={"status": status})
