import logging

from app.application import Application, Config, api


logger = logging.getLogger(__name__)


def main() -> None:
    Config.validate()
    Config.initialize()

    app = Application(ssl_certfile=Config.SSL_CERTFILE_PATH, ssl_keyfile=Config.SSL_CERTFILE_KEY)
    app.include_router(router=api.router, prefix="/api")

    app.run(Config.HOST, Config.PORT)


if __name__ == "__main__":
    main()
