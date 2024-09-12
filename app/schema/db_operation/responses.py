import pydantic
import typing as tp


class InserResponse(pydantic.BaseModel):
    status: str
    error: tp.Optional[str]
