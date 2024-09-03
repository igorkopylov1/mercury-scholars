from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class AccessLevel(Enum):
    GRANTED = "GRANTED"
    DENIED = "DENIED"
    EXPIRED = "EXPIRED"


class BasePattern:
    def to_dict(self, **kwargs):
        data = self.dict(**kwargs)
        if "access" in data:
            data["access"] = data["access"].value
        return data


class RedisSession(BaseModel, BasePattern):
    chat_id: str
    first_name: str
    access: AccessLevel
    last_session: int 


class RedisAuthorize(BaseModel, BasePattern):
    chat_id: str
    first_name: str
    pay: int
    date_end: str
    date_start: str
