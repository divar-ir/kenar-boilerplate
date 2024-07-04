from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_serializer, model_validator
from pydantic.networks import AnyUrl


class OAuthSessionType(Enum):
    CHAT = "CHAT"
    POST = "POST"


class OAuthSession(BaseModel):
    state: UUID = Field(default_factory=uuid4)
    type: OAuthSessionType
    callback_url: Optional[AnyUrl] = None
    post_token: str
    chat_id: Optional[UUID] = None

    def get_state(self) -> str:
        return str(self.state)

    def get_callback_url(self) -> str:
        return str(self.callback_url)

    @field_serializer("state")
    def serialize_state(self, state: UUID, _info):
        return str(state)

    @field_serializer("chat_id")
    def serialize_chat_id(self, chat_id: UUID, _info):
        return str(chat_id)

    @field_serializer("callback_url")
    def serialize_callback_url(self, callback_url: AnyUrl, _info):
        return str(callback_url)

    @model_validator(mode="after")
    def validate_chat_id(self):
        if self.type == OAuthSessionType.CHAT.value and not self.chat_id:
            raise ValueError(f"OAuthSession with {OAuthSessionType.CHAT.value} type must has chat_id")
        return self

    class Config:
        use_enum_values = True
