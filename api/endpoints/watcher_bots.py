from fastapi import APIRouter
from core.config import RESPONSE_ERROR
from repository.tools import userbot_request, create_response
from repository.userbots.external_channels import ExternalChannelsRepository
from repository.userbots.competiter_channels import CompetitorChannelsRepository
from repository.userbots.userbots import UserBotsRepository
from repository.userbots.userbots_subscriptions import UserbotsSubscriptionsRepository
import datetime

router = APIRouter()
min_check_24_delta_hours = 6


async def get_competitor_channel(parsed_channel: dict, external_channel: dict):
    title = parsed_channel["title"]
    description = ""
    if parsed_channel.get("description_full") is None:
        _description = parsed_channel["description"]
    _description = parsed_channel["description_full"].split("\n")
    count = await CompetitorChannelsRepository.get_count(url=parsed_channel["link"])
    count = count[0]["count_1"]
    excepts = ["adsell", "https://t.me/+", "\n"]
    filtered_description = [item for item in _description if all(except_item not in item for except_item in excepts)]
    for i in filtered_description:
        if "@" in i or "t.me/" in i:
            ind = filtered_description.index(i)
            description = "\n".join(filtered_description[ind::])
            break
        else:
            description = "-"
    if title.replace("\n", "").strip() == external_channel["title"].replace("\n", "").strip():
        return None
    channel = {#ribla9000 parsed_channel.get("description_full")
                                                                         is not None else description,
               #ribla9000rsed_channel.get("message_id") is not None else "-"}
    return channel


async def get_competitor_info(parsed_channel: dict, external_channel: dict):
    title = parsed_channel["title"]
    existing_competitor_channel = await CompetitorChannelsRepository.get_by_user_channel(external_id=external_channel["id"], title=title)
    channel = await get_competitor_channel(parsed_channel=parsed_channel, external_channel=external_channel)
    if channel is None:
        return None
    if existing_competitor_channel is not None:
        return channel
    _channel = channel.copy()
    del _channel["count"]
    await CompetitorChannelsRepository.create(_channel)
    return channel


@router.post("/#ribla9000/")
async def watcher_join_by_link(invite_link: str, user_id: int):
    userbot = await UserBotsRepository.get_free_watcher()
    params = {#ribla9000}
    request = userbot_request(endpoint="#ribla9000", method="POST", params=params)
    response = request.json()

    if response.get("result") == RESPONSE_ERROR:
        return create_response(code=400, message="Invalid data given")

    channel = {"title": response.get("title"),
               "user_id": user_id,
               "open_link": invite_link,
               "chat_id": str(response.get("chat_id"))}

    if channel["chat_id"] is None or channel["chat_id"] == "":
        return create_response(code=400, message="Invalid data given")

    external_channel = await ExternalChannelsRepository.get_user_channel(user_id=user_id, chat_id=channel["chat_id"])
    ub_subscription = {"chat_id": channel["chat_id"], "userbot_id": userbot["id"]}

    if external_channel is not None:
        subscription = await UserbotsSubscriptionsRepository.get_userbot(channel["chat_id"])

        if subscription is None:
            await UserbotsSubscriptionsRepository.create(ub_subscription)
            return create_response(
                code=400,
                message="This channel already exists",
                description="Wasn't subscribed, now - subscribed"
            )

        return create_response(code=400, message="This channel already exists", description="Already subscribed")

    await UserbotsSubscriptionsRepository.create(ub_subscription)
    channel_id = await ExternalChannelsRepository.create(channel)
    return create_response(data=channel_id, message="Channel successfully added")


@router.post("/get-ads-in-external-channel/")
async def get_ads_in_external_channel(external_id: int):
    external_channel = await ExternalChannelsRepository.get_by_id(external_id)
    channel_userbot = await UserbotsSubscriptionsRepository.get_userbot(chat_id=external_channel["chat_id"])
    print("get_ads_in_external_channel function")
    print(f"ext channel {external_channel['title']} --> user bot: {channel_userbot['name']} {channel_userbot['id']}")
    print(f"last activity: {external_channel.get('last_activity')}")

    if (external_channel.get('last_activity') is not None and
        (datetime.datetime.now() - external_channel.get('last_activity')) <
            datetime.timedelta(hours=min_check_24_delta_hours)):
        print("event last activity is not None")
        channels = await CompetitorChannelsRepository.get_result_by_chat_id(chat_id=external_channel["chat_id"])
        channels_info = []
        print(f"channels to return by last activity event: {channels}")

        for parsed_channel in channels:
            result = await get_competitor_info(parsed_channel, external_channel)
            if result is None:
                continue
            if result not in channels:
                channels_info.append(result)
        print(f"data: {channels_info}\n\n")
        return create_response(data=channels_info)

    print("event last activity is None")
    params = {
        "session": channel_userbot["session"],
        "userbot_id": channel_userbot["id"],
        "external_channel_id": external_channel["id"]
    }
    request = userbot_request(endpoint="watchers/find-ads-in-external-channel", method="POST", params=params)
    response = request.json()
    print(f"response: {response}")

    if response.get("code") != 200:
        await ExternalChannelsRepository.update_last_activity(external_id)
        print(f"Some error from Userbots, response: {response}")
        return create_response(code=400, message="Error while parsing, text in support")

    channels = []
    if response.get("data") is None:
        return response
    for parsed_channel in response.get("data"):
        result = await get_competitor_info(parsed_channel, external_channel)
        if result is None:
            continue
        if result not in channels:
            channels.append(result)

    print(f"channels to return after parsing: {channels}")
    await ExternalChannelsRepository.update_last_activity(external_id)
    return create_response(data=channels)


@router.delete("/leave_channel/")
async def watcher_leave_channel(channel_id: int):
    external_channel = await ExternalChannelsRepository.get_by_id(channel_id)
    watcher = await UserbotsSubscriptionsRepository.get_userbot(chat_id=external_channel["chat_id"])
    params = {"external_id": channel_id, "session": watcher["session"], "userbot_id": watcher["id"]}
    request = userbot_request(endpoint="watchers/leave_channel/", method="DELETE", params=params)
    return create_response()

