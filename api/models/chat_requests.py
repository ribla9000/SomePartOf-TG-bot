from pydantic import BaseModel


class ChatRequestsModel(BaseModel):
    user_channel_user_id: int
    invite_link: str
