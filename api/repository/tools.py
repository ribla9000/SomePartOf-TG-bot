import time
from core.config import USERBOT_BASE_URL, ADMIN_BOTS_BASE_URL
import requests
from typing import Union, Any


def to_seconds(day: int = 0, hour: int = 0, minutes: int = 0):
    current_time = time.time()
    expire_date = current_time + day * 24 * 60 * 60 + hour * 60 * 60 + minutes * 60
    return expire_date


def keyboard_cols(buttons, cols):
    menu = [buttons[i:i + cols] for i in range(0, len(buttons), cols)]
    return menu


def get_values(values):
    if values is None:
        return None
    return [dict(value) for value in values] if isinstance(values, list) else dict(values)


def userbot_request(endpoint: str, method: str, params: dict):
    return requests.request(method=method, url=USERBOT_BASE_URL + endpoint, params=params)


def admin_bots_request(endpoint: str, method: str, params: dict):
    return requests.request(method=method, url=ADMIN_BOTS_BASE_URL + endpoint, params=params)


def create_response(data: Union[Any, dict] = None, code: int = None, description: str = None, message: str = None):
    _response = {"code": 200 if code is None else code,
                 "description": description,
                 "data": data,
                 "message": message}
    return _response





