import pydantic
import typing as tp


class GetModelsABCResponse(pydantic.BaseModel):
    data: tp.Optional[str]
