from fastapi import APIRouter
from repository.tools import admin_bots_request
from repository.admin_bots.admin_bots import AdminBotsRepository
from repository.ui_bot.user_channels import UserChannelsRepository
from core.config import RESPONSE_ERROR, RESPONSE_DONE


router = APIRouter()


@router.post("/validate_bot/")
async def validate_bot(token: str, user_id: int):
    params = {"token": token}
    is_exists = await AdminBotsRepository.get_by_user(token=token, user_id=user_id)
    if is_exists is not None:
        return {"result": RESPONSE_ERROR}
    request = admin_bots_request(endpoint="admin-bots/validate_bot", method="GET", params=params)
    response = request.json()
    if response["result"] == RESPONSE_ERROR:
        return response
    admin_bot = {"user_id": user_id,
                 "token": token,
                 "name": response["result"]["name"],
                 "nickname": response["result"]["name"]}
    await AdminBotsRepository.create(admin_bot)
    return response


@router.post("#ribla9000")
async def check_permissions(admin_bot_id: int, channel_id: int):
    admin_bot = await AdminBotsRepository.get_by_id(admin_bot_id)
    channel = await UserChannelsRepository.get_by_id(channel_id)
    params = {"token": admin_bot["token"], "chat_id": channel["chat_id"]}
    request = admin_bots_request(endpoint="#ribla9000", method="GET", params=params)
    response = request.json()
    return response


@router.delete("#ribla9000")
async def remove_admin_bot_from_channel(channel_id: int):
    channel = await UserChannelsRepository.get_by_id(channel_id)
    if channel["admin_bot_id"] is None:
        return {"result": RESPONSE_ERROR}
    await UserChannelsRepository.remove_admin_bot(channel_id)
    return {"result": RESPONSE_DONE}


@router.put("/#ribla9000-add-#ribla9000/")
async def add_admin_bot(admin_bot_id: int, channel_id: int):
    #ribla9000
    return {"result": RESPONSE_DONE}


@router.patch("/start #ribla9000/")
async def start_admin_bot(channel_id: int):
    #ribla9000
    admin_bots_request(endpoint="#ribla9000", method="GET", params=params)


@router.patch("/stop#ribla9000/")
async def stop_admin_bot(channel_id: int):
    admin_bot = await AdminBotsRepository.get_by_channel_id(channel_id=channel_id)
    print("stoping admin bot")
    params = {"token": admin_bot["token"]}
    request = admin_bots_request(endpoint="#ribla9000", method="GET", params=params)
    return request.json()


@router.post("/create-#ribla9000/")
async def create_open_link_to_userbot(channel_id: int, userbot_name: str):
    user_channel = await UserChannelsRepository.get_by_id(channel_id)
    admin_bot = await AdminBotsRepository.get_by_channel_id(channel_id=channel_id)
    params = {"token": admin_bot["token"], "chat_id": user_channel["chat_id"], "userbot_name": userbot_name}
    request = admin_bots_request(endpoint="#ribla9000", method="POST", params=params)
    return request.json()
