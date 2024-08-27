import typing as tp
from datetime import datetime

import fastapi

import pydantic


class Chat(pydantic.BaseModel):
    id: int = pydantic.Field(description="Unique identifier for this chat.")
    type: str = pydantic.Field(description="Type of the chat.")
    title: tp.Optional[str] = pydantic.Field(None, description="Optional. Title for supergroups, channels and group chats.")
    username: tp.Optional[str] = pydantic.Field(None, description="Optional. Username for private chats, supergroups and channels if available.")
    first_name: tp.Optional[str] = pydantic.Field(None, description="Optional. First name of the other party in a private chat.")
    last_name: tp.Optional[str] = pydantic.Field(None, description="Optional. Last name of the other party in a private chat.")
    is_forum: tp.Optional[bool] = pydantic.Field(None, description="True if the supergroup chat is a forum.")

class User(pydantic.BaseModel):
    id: int = pydantic.Field(description="Unique identifier for this user or bot.")
    is_bot: bool = pydantic.Field(description="True if this user is a bot.")
    first_name: str = pydantic.Field(description="User's or bot's first name.")
    last_name: tp.Optional[str] = pydantic.Field(None, description="User's or bot's last name.")
    username: tp.Optional[str] = pydantic.Field(None, description="User's or bot's username.")
    language_code: tp.Optional[str] = pydantic.Field(None, description="IETF language tag of the user's language.")

class Message(pydantic.BaseModel):
    message_id: int = pydantic.Field(description="Message identifier")
    from_: User = pydantic.Field(..., alias='from', description="User information")  # Используем alias для поля
    chat: Chat = pydantic.Field(description="Chat information")
    date: datetime = pydantic.Field(description="Date in Unix timestamp format")
    text: str = pydantic.Field(description="Text")

class BaseRequest(pydantic.BaseModel):
    update_id: int = pydantic.Field(description="Update identifier")
    message: Message
