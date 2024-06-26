from typing import Optional

from pydantic import BaseModel
from datetime import date, time


class PostBase(BaseModel):
    event_date: date
    event_time: time
    location: str
    description: str
    title: str
    content: Optional[list]


class Post(PostBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True



