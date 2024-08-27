import logging
import typing as tp

from fastapi import Depends, Request, Body
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from telegram import Update


from .. import schema as schema

if tp.TYPE_CHECKING:
    from tg_project.app import Application

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/operations", tags=["Operations"])


@router.post("/query")
async def query(
    request: Request,
    data: schema.operations.BaseRequest = Body(),
) -> JSONResponse:
    app: Application = request.app.state.application

    status = await app.operation_controller.create_response(chat_id=data.message.chat.id, message_text=data.message.text, user_name=data.message.from_.first_name)
    return JSONResponse(content={"status": status})
