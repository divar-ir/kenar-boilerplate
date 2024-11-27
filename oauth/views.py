import logging
from datetime import timedelta
from urllib.parse import urlencode

import httpx
import pydantic
from django.core import signing
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from kenar.chatmessage import SetNotifyChatPostConversationsRequest
from rest_framework.decorators import api_view

from addon.models import Post
from boilerplate import settings
from boilerplate.clients import get_divar_kenar_client
from chat.models import Chat
from oauth.models import OAuth
from oauth.schemas import OAuthSession, OAuthSessionType

logger = logging.getLogger(__name__)
signer = signing.Signer()


@api_view(["GET"])
def oauth_callback(request):
    req_state = request.query_params.get("state")
    authorization_code = request.query_params.get("code")

    if not authorization_code or not req_state:
        return HttpResponseBadRequest("missing state or authorization code")

    try:
        oauth_session = OAuthSession(**request.session.get(settings.OAUTH_SESSION_KEY))
    except pydantic.ValidationError as e:
        logger.error(e)
        return HttpResponseForbidden("permission denied")

    if req_state != oauth_session.get_state():
        return HttpResponseForbidden("permission denied")

    kenar_client = get_divar_kenar_client()
    session_key = request.session.session_key

    try:
        access_token_response = kenar_client.oauth.get_access_token(authorization_code)

        if OAuth.objects.filter(session_id=session_key).exists():
            OAuth.objects.get(session_id=session_key).delete()

        oauth = OAuth.objects.create(
            session_id=session_key,
            access_token=access_token_response.access_token,
            expires_in=timezone.now() + timedelta(seconds=access_token_response.expires_in),
        )
        post = Post.objects.get(token=oauth_session.post_token)
        oauth.post = post
        oauth.save()

        if oauth_session.type == OAuthSessionType.POST.value:
            oauth.save()
            base_url = reverse("addon_app")
            query_string = urlencode({"state": oauth_session.state})
            url = f"{base_url}?{query_string}"
            return redirect(url)

        elif oauth_session.type == OAuthSessionType.CHAT.value:
            chat = Chat.objects.get(id=oauth_session.chat_id)
            oauth.chat = chat
            oauth.save()

            logger.error(access_token_response.access_token)
            logger.error(SetNotifyChatPostConversationsRequest(
                    post_token=chat.post.token,
                    endpoint=settings.APP_BASE_URL + reverse("receive_notify"),
                    identification_key=signer.sign(str(chat.id)),
                ),)

            base_url = reverse("chat_app")
            query_string = urlencode({"state": oauth_session.state})
            url = f"{base_url}?{query_string}"
            return redirect(url)

    except httpx.HTTPStatusError as http_err:
        logger.error(f"HTTP error occurred: {http_err}: {http_err.response.text}")
        return HttpResponseServerError("Internal server error")
    except Exception as err:
        logger.error(f"An error occurred: {err}")
        return HttpResponseServerError("Internal server error")
