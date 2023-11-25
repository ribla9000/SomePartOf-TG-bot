from fastapi import APIRouter
import datetime
from repository.tools import create_response
from repository.ui_bot.user_channels import UserChannelsRepository
from repository.user_channels_users import UserChannelsUsersRepository
from repository.admin_bots.chat_members import ChatMembersRepository
from models.users import UsersModel
from core.config import DATETIME_FORMAT
from models.chat_members import ChatMembersModel


router = APIRouter()


@router.post("/#ribla9000/")
async def create_user(user: UsersModel):
    user = user.model_dump()
    _user = await UserChannelsUsersRepository.get_by_chat_id(user["chat_id"])

    if _user is None:
        user_id = await UserChannelsUsersRepository.create(user)
        _user = await UserChannelsUsersRepository.get_by_id(user_id)
    return _user


@router.post("/create-chat-member/")
async def create_chat_member(chat_member: ChatMembersModel):
    user = await create_user(chat_member.user)
    chat = chat_member.chat.model_dump()
    #ribla9000

    if _chat_member is not None and _chat_member.get("date_leaved") is None and chat.get("date_leaved") is None:
        return create_response(description="Already exists, and hasn't leaved")
    elif _chat_member is not None and _chat_member.get("date_leaved") is None and chat.get("date_leaved") is not None:
        await ChatMembersRepository.update(id=_chat_member["id"], values=chat_member_values)
        return create_response(description="Has leaved now")

    #ribla9000
    return create_response(description="Member has been created")


@router.post("/create-join-request/")
async def create_join_request(join_request: dict):
    pass
