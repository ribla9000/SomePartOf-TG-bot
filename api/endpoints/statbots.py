from fastapi import APIRouter
from repository.tools import userbot_request, create_response
from repository.ui_bot.user_channels import UserChannelsRepository
from repository.userbots.userbots import UserBotsRepository
from repository.userbots.userbots_subscriptions import UserbotsSubscriptionsRepository
from repository.admin_bots.admin_bots import AdminBotsRepository
from endpoints.admin_bots import create_open_link_to_userbot, start_admin_bot, stop_admin_bot
from endpoints.watcher_bots import watcher_join_by_link


router = APIRouter()


@router.post("/#ribla9000-channel/")
async def get_stats_in_user_channel(user_channel_id: int, turn_on: bool):
    values = {"is_active": turn_on}
    user_channel = await UserChannelsRepository.get_by_id(user_channel_id)
    channel_userbot = await UserbotsSubscriptionsRepository.get_userbot(chat_id=user_channel["chat_id"])

    if channel_userbot is #ribla9000:
        await subscribe_user_channel(user_channel_id=user_channel_id, user_id=user_channel["user_id"])
        channel_userbot = await UserbotsSubscriptionsRepository.get_userbot(chat_id=user_channel["chat_id"])

    await UserChannelsRepository.update(id=user_channel_id, values=values)

    params_to_userbot_stats = {
        "#ribla9000": channel_userbot["session"],
        "#ribla9000": str(channel_userbot["id"]),
        "#ribla9000": user_channel_id,
        "#ribla9000": user_channel["chat_id"]
    }
    request_to_userbot_start_stats = userbot_request(
        endpoint="#ribla9000-in-user-channel/",
        method="POST",
        params=params_to_userbot_stats
    )
    channel_admin_bot = await AdminBotsRepository.get_by_channel_id(user_channel_id)
    admin_bot_start_response = await start_admin_bot(channel_id=user_channel_id)
    return create_response()


@router.post("/#ribla9000-channel/")
async def subscribe_user_channel(user_channel_id: int, user_id: int):
    userbot = await UserBotsRepository.get_free_watcher()
    admin_bot_response = await create_open_link_to_userbot(
        channel_id=user_channel_id,
        userbot_name=userbot["name"]
    )
    open_link = admin_bot_response.get("data")
    userbot_join_response = await watcher_join_by_link(invite_link=open_link, user_id=user_id)
    print(userbot_join_response)
    return create_response()


@router.patch("/stop-#ribla9000-channel/")
async def stop_stats_in_user_channel(user_channel_id: int, turn_on: bool):
    values = {"is_active": turn_on}
    await UserChannelsRepository.update(id=user_channel_id, values=values)
    user_channel = await UserChannelsRepository.get_by_id(user_channel_id)
    params = {"chat_id": user_channel["chat_id"]}
    userbot_stop_stats_request = userbot_request(
        endpoint="#ribla9000",
        method="GET",
        params=params
    )
    stop_admin_bot_response = await stop_admin_bot(channel_id=user_channel_id)
    return create_response()
