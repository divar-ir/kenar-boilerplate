import abc

from pydantic import BaseModel

from chat.models import Chat


class StartChatSessionUser(BaseModel):
    id: str


class StartChatSessionRequest(BaseModel):
    post_token: str
    user_id: str
    peer_id: str
    callback_url: str
    supplier: StartChatSessionUser
    demand: StartChatSessionUser


class ChatMessagePayloadUser(BaseModel):
    id: str
    is_supply: bool


class ChatMessagePayloadMetadata(BaseModel):
    title: str
    category: str
    post_token: str


class ChatMessageTextData(BaseModel):
    text: str


class ChatMessagePayload(BaseModel):
    id: str
    type: str
    data: ChatMessageTextData
    sender: ChatMessagePayloadUser
    receiver: ChatMessagePayloadUser
    metadata: ChatMessagePayloadMetadata
    sent_at: int


class Notification(BaseModel):
    type: str
    timestamp: int
    payload: ChatMessagePayload


class Handler(abc.ABC):
    @abc.abstractmethod
    def handle(self, notification: Notification):
        raise NotImplemented


class ChatNotificationHandler(Handler):
    def __init__(self, chat: Chat):
        self.chat = chat

    def handle(self, notification: Notification):
        match notification.type:
            case "CHAT_MESSAGE":
                if not notification.payload.sender.is_supply:
                    self.handle_chat_message(notification.timestamp, notification.payload)

    @abc.abstractmethod
    def handle_chat_message(self, timestamp: int, payload: ChatMessagePayload):
        raise NotImplemented
