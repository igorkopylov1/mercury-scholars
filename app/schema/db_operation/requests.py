import typing as tp
from datetime import datetime

import fastapi

import pydantic


class InsertRequestBody(pydantic.BaseModel):
    chat_id: str = pydantic.Field(description="chat identifier")
    first_name: str = pydantic.Field(description="Telegram user name")
    start_date: datetime = pydantic.Field(description="Start date of bot using")
    end_date: datetime = pydantic.Field(description="End date of bot using")
    pay: int = pydantic.Field(description="Payment for using")

    class Config:
        arbitrary_types_allowed = True

class InsertRequest(pydantic.BaseModel):
    body: InsertRequestBody = fastapi.Body()

    @pydantic.validator('body')
    def validate_config(cls, body: InsertRequestBody) -> InsertRequestBody:
        assert body.start_date, "start_date field is a required parameter in the config"
        assert body.pay >= 0, "pay must be a positive value"
        return body


# class InsertRequest(pydantic.BaseModel):
#     class InsertRequestBody:
#         chat_id: str = pydantic.Field(description="chat indificator")
#         first_name: str = pydantic.Field(description="Telegram user name")
#         start_date: datetime = pydantic.Field(description="Start date of bot using")
#         end_date: datetime = pydantic.Field(description="End date of bot using")
#         pay: int = pydantic.Field(description="Payment for using")

#     body: InsertRequestBody = fastapi.Body()

#     @pydantic.field_validator("body")
#     def validate(cls, body: InsertRequestBody) -> InsertRequestBody:
#         assert body.start_date, "start_date field is a required parameter in the config"
#         assert body.pay >= 0, "pay must be a positive value"
#         return body
