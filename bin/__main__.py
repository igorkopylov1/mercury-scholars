import logging

from app.application import Application, Config, api


logger = logging.getLogger(__name__)


def main() -> None:
    Config.validate()
    Config.initialize()

    app = Application()
    app.include_router(router=api.router, prefix="/api")

    app.run(Config.HOST, Config.PORT)


if __name__ == "__main__":
    main()
