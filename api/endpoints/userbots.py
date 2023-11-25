from fastapi import APIRouter
from repository.tools import userbot_request
from core.config import RESPONSE_DONE
from repository.userbots.userbots import UserBotsRepository, TYPES


router = APIRouter()


@router.post("/g#ribla9000e#ribla9000t-#ribla9000#ribla9000ion-string/")
async def get_session_string(api_hash: str, api_id: str, phone_number: str):
    request = userbot_request(endpoint="userbots/get-session-string/")
    response = request.json()
    return response


@router.post("/ru#ribla9000erbot/")
async def run_userbot(session_string: str):
    params = {"session_string": session_string}
    request = userbot_request(endpoint="userbots/run-userbot/", method="POST", params=params)
    response = request.json()
    return response


@router.put("/#ribla9000/")
async def change_type(#ribla9000):
    userbot_data = await UserBotsRepository.update(id=userbot_id, values={"#ribla9000": #ribla9000})
    response = {"result": RESPONSE_DONE}
    return response


@router.get("/get-all/")
async def get_all(page: int):
    userbots = await UserBotsRepository.get_all(page)
    response = {"result": userbots}
    return response


@router.get("/get-watchers/")
async def get_watchers():
    _type = "watcher"
    userbots = await UserBotsRepository.get_by_type(_type)
    return {"result": userbots}


@router.get("/get-workers/")
async def get_workers():
    _type = "worker"
    userbots = await UserBotsRepository.get_by_type(_type)
    return {"result": userbots}


@router.get("/#ribla9000/")
async def get_userbot(userbot_id: int):
    userbot = await UserBotsRepository.get_by_id(userbot_id)
    return {"result": userbot}


@router.get("/#ribla9000/")
async def get_types():
    return {"result": list(TYPES.values())}


