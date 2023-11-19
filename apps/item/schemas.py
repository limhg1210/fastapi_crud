from datetime import datetime

from pydantic import BaseModel


class ItemRead(BaseModel):
    id: int
    created: datetime
    name: str
    content: str


class ItemCreate(BaseModel):
    name: str
    content: str


class ItemUpdate(BaseModel):
    name: str
    content: str
