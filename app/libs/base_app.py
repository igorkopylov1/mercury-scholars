import logging
import typing as tp
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter


logger = logging.getLogger(__name__)


class BaseApplication:
    SSL_CERTFILE = "/etc/letsencrypt/live/mercury-scholars.ru/fullchain.pem"
    SSL_KEYFILE = "/etc/letsencrypt/live/mercury-scholars.ru/privkey.pem"

    def __init__(self):
        self.app = FastAPI()
        self.api_router = APIRouter()

    def include_router(self, router: APIRouter, prefix: str):
    # Добавление маршрута из переданного роутера
        for route in router.routes:
            print(f"server api path: {prefix}{route.path}")
            self.api_router.add_api_route(
                path=f"{prefix}{route.path}",
                endpoint=route.endpoint,
                methods=route.methods,
                name=route.name,
                response_model=route.response_model,
                status_code=route.status_code,
                tags=route.tags,
                summary=route.summary,
                description=route.description,
                responses=route.responses,
            )


    def run(self, host: str = "194.87.248.10", port: int = 8443):
        self.app.state.application = self
        self.app.include_router(self.api_router)
        uvicorn.run(self.app, host=host, port=port, ssl_keyfile=self.SSL_KEYFILE, ssl_certfile=self.SSL_CERTFILE)
