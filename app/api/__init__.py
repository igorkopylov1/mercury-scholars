from fastapi import APIRouter

from . import operations # noqa

router = APIRouter()  # api

router.include_router(operations.router)
