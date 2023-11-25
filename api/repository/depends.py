from pydantic import BaseModel
from typing import Dict, Any


class CustomModel(BaseModel):
    pass


def parse_model(model: BaseModel, values: dict):
    return values.items()
