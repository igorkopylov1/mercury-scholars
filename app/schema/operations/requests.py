import typing as tp
from datetime import datetime

import fastapi

import pydantic


class Chat(pydantic.BaseModel):
    id: int = pydantic.Field(description="Unique identifier for this chat. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.")
    type: str = pydantic.Field(description="Type of the chat, can be either 'private', 'group', 'supergroup' or 'channel'.")
    title: tp.Optional[str] = pydantic.Field(None, description="Optional. Title, for supergroups, channels and group chats.")
    username: tp.Optional[str] = pydantic.Field(None, description="Optional. Username, for private chats, supergroups and channels if available.")
    first_name: tp.Optional[str] = pydantic.Field(None, description="Optional. First name of the other party in a private chat.")
    last_name: tp.Optional[str] = pydantic.Field(None, description="Optional. Last name of the other party in a private chat.")
    is_forum: tp.Optional[bool] = pydantic.Field(None, description="True, if the supergroup chat is a forum (has topics enabled).")



class User(pydantic.BaseModel):
    id: int = pydantic.Field(description="Unique identifier for this user or bot.")
    is_bot: bool = pydantic.Field(description="True, if this user is a bot.")
    first_name: str = pydantic.Field(description="User's or bot's first name.")
    last_name: tp.Optional[str] = pydantic.Field(None, description="User's or bot's last name.")
    username: tp.Optional[str] = pydantic.Field(None, description="User's or bot's username.")
    language_code: tp.Optional[str] = pydantic.Field(None, description="IETF language tag of the user's language.")
    is_premium: tp.Optional[bool] = pydantic.Field(None, description="True, if this user is a Telegram Premium user.")
    added_to_attachment_menu: tp.Optional[bool] = pydantic.Field(None, description="True, if this user added the bot to the attachment menu.")
    can_join_groups: tp.Optional[bool] = pydantic.Field(None, description="True, if the bot can be invited to groups. Returned only in getMe.")
    can_read_all_group_messages: tp.Optional[bool] = pydantic.Field(None, description="True, if privacy mode is disabled for the bot. Returned only in getMe.")
    supports_inline_queries: tp.Optional[bool] = pydantic.Field(None, description="True, if the bot supports inline queries. Returned only in getMe.")
    can_connect_to_business: tp.Optional[bool] = pydantic.Field(None, description="True, if the bot can be connected to a Telegram Business account to receive its messages. Returned only in getMe.")
    has_main_web_app: tp.Optional[bool] = pydantic.Field(None, description="True, if the bot has a main Web App. Returned only in getMe.")


class Message(pydantic.BaseModel):
    message_id: int = fastapi.Path(description="Message identifier")
    from_user: User = fastapi.Body(description="User information")


class BaseRequest(pydantic.BaseModel):
    update_id: int = pydantic.Field(description="Идентификатор обновлений")
    message: Message = fastapi.Body()
    chat: Chat = fastapi.Body()
    date: datetime = pydantic.Field(description="Дата обновления в формате Unix timestamp")
    text: str = pydantic.Field(description="Текст")

class TestRequest(pydantic.BaseModel):
    user_id: int = pydantic.Field(description="Идентификатор пользователя")
