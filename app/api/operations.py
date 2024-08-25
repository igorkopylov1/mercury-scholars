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
async def clone_model(
    request: Request,
    data: schema.operations.TestRequest = Body(),
) -> JSONResponse:
    print(data.user_id)
    app: Application = request.app.state.application 
    app.operation_controller.first_try() # Test func
    return JSONResponse(
        dict(status="ok")
    )
