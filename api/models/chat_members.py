from models.users import UsersModel
from pydantic import BaseModel, field_validator
from typing import Union


class _ChatMember(BaseModel):
    chat_id: str
    date_joined: Union[None, str] = None
    date_leaved: Union[None, str] = None
    is_member: bool


class ChatMembersModel(BaseModel):
    user: UsersModel
    chat: _ChatMember
