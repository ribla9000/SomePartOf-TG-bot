import time
import requests
from core.config import API_BASE_URL, redis_db
from db.users import ROLES



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


def api_request(endpoint: str, method: str, params: dict):
    return requests.request(method=method, url=API_BASE_URL + endpoint, params=params)


def check_permissions(cur_role, chsn_role):
    roles = list(ROLES.values())
    return roles.index(cur_role) > roles.index(chsn_role)


def redis_set_data(key, value):
    redis_db.set(key, value)


def redis_hset_data(key, value):
    redis_db.hset(key, mapping=value)


def redis_get_data(key):
    return redis_db.get(key)


def redis_hget_data(key):
    return redis_db.hgetall(key)


def redis_delete_data(key):
    redis_db.delete(key)


class redis_client:

    redis_set_data: callable = redis_set_data
    redis_hset_data: callable = redis_hset_data
    redis_hget_data: callable = redis_hget_data
    redis_delete_data: callable = redis_delete_data


