import json
import logging
from urllib.parse import urlencode

import pydantic
from django.core import signing
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from kenar.app import Scope, SendChatMessageResourceIdParams
from kenar.models.oauth import OauthResourceType
from rest_framework.decorators import api_view

from addon.models import Post
from boilerplate import settings
from boilerplate.clients import get_divar_kenar_client
from chat.handler import ChatNotificationHandler, Notification, StartChatSessionRequest
from chat.models import Chat
from oauth.models import OAuth
from oauth.schemas import OAuthSession, OAuthSessionType

logger = logging.getLogger(__name__)
signer = signing.Signer()


@api_view(["POST"])
def start_chat_session(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or auth_header != settings.DIVAR_IDENTIFICATION_KEY:
        return HttpResponseForbidden("Unauthorized access")

    req_data = StartChatSessionRequest(**json.loads(request.body))

    post_token = req_data.post_token
    user_id = req_data.user_id
    peer_id = req_data.peer_id
    supplier_id = req_data.supplier.id
    callback_url = req_data.callback_url

    # Needed for CHAT_POST_CONVERSATIONS_READ oauth scope
    if user_id != supplier_id:
        return HttpResponseForbidden("You must be post owner")

    post, _ = Post.objects.get_or_create(token=post_token)
    chat, _ = Chat.objects.get_or_create(
        post=post,
        user_id=user_id,
        peer_id=peer_id,
    )

    oauth_session = OAuthSession(
        callback_url=callback_url,
        type=OAuthSessionType.CHAT,
        post_token=post.token,
        chat_id=chat.id,
    )
    signed_oauth_session = signer.sign_object(oauth_session.model_dump(exclude_none=True))

    chat_oauth_url = settings.APP_BASE_URL + reverse("chat_oauth")
    query_string = urlencode({"oauth_session": signed_oauth_session})
    chat_oauth_url = f"{chat_oauth_url}?{query_string}"

    return JsonResponse({"status": "200", "message": "success", "url": chat_oauth_url})


@api_view(["GET"])
def chat_oauth(request):
    signed_oauth_session = request.query_params.get("oauth_session")
    if not signed_oauth_session:
        return HttpResponseForbidden("permission denied")

    try:
        unsigned_oauth_session = signer.unsign_object(signed_oauth_session)
    except signing.BadSignature:
        return HttpResponseForbidden("permission denied")

    try:
        oauth_session = OAuthSession(**unsigned_oauth_session)
    except pydantic.ValidationError:
        return HttpResponseForbidden("permission denied")

    try:
        chat = Chat.objects.get(id=oauth_session.chat_id)
    except Chat.DoesNotExist:
        return HttpResponseForbidden("permission denied")

    request.session[settings.OAUTH_SESSION_KEY] = oauth_session.model_dump(exclude_none=True)

    kenar_client = get_divar_kenar_client()

    oauth_scopes = [
        Scope(
            resource_type=OauthResourceType.CHAT_MESSAGE_SEND,
            resource_id=kenar_client.oauth.get_send_message_resource_id(
                SendChatMessageResourceIdParams(user_id=chat.user_id, peer_id=chat.peer_id, post_token=chat.post.token)
            ),
        ),
        Scope(resource_type=OauthResourceType.CHAT_POST_CONVERSATIONS_READ, resource_id=chat.post.token),
    ]

    oauth_url = kenar_client.oauth.get_oauth_redirect(
        scopes=oauth_scopes,
        state=oauth_session.get_state(),
    )

    return redirect(oauth_url)


@api_view(["GET"])
def chat_app(request):
    try:
        oauth_session = OAuthSession(**request.session.get(settings.OAUTH_SESSION_KEY))
    except pydantic.ValidationError as e:
        logger.error(e)
        return HttpResponseForbidden("permission denied")

    req_state = request.query_params.get("state")
    if not req_state or req_state != oauth_session.get_state():
        return HttpResponseForbidden("permission denied")

    try:
        oauth = OAuth.objects.get(session_id=request.session.session_key)
        chat = oauth.chat
    except OAuth.DoesNotExist:
        return HttpResponseForbidden("permission denied")

    # TODO: Implement logic for after opening your application in chat
    # Example: Sending message in chat

    # After processing the chat logic, redirect to the callback URL
    callback_url = oauth_session.get_callback_url()
    return redirect(callback_url)


@api_view(["POST"])
def receive_notify(request):
    signed_authorization = request.headers.get("Authorization")
    if not signed_authorization:
        return JsonResponse(
            {
                "status": "403",
            }
        )

    try:
        chat_id = signer.unsign(signed_authorization)
    except signing.BadSignature:
        return JsonResponse(
            {
                "status": "403",
            }
        )

    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        return JsonResponse(
            {
                "status": "404",
            }
        )

    try:
        notification = Notification(**json.loads(request.body))
        handler = ChatNotificationHandler(chat=chat)
        handler.handle(notification)
    except Exception as e:
        logger.error(e)
        return JsonResponse(
            {
                "status": "500",
            }
        )

    return JsonResponse(
        {
            "status": "200",
        }
    )
