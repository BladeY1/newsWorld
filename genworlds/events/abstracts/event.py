from abc import ABC

import json
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class AbstractEvent(ABC, BaseModel):
    event_type: str
    description: str
    #summary: Optional[str]
    created_at: datetime = Field(default_factory=datetime.now)
    sender_id: str
    target_id: Optional[str]

class NewsEvent(AbstractEvent):
    news_id: Optional[str]
    news_content: Optional[str]
    comment_content: Optional[str]

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_dict(cls, event_data):
        return cls(**event_data)

