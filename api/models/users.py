from pydantic import BaseModel


class UsersModel(BaseModel):
    nickname: str
    name: str
    chat_id: str
