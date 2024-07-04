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
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from addon.models import Post
from boilerplate import settings
from boilerplate.clients import get_divar_kenar_client
from chat.models import Chat
from oauth.models import OAuth
from oauth.schemas import OAuthSession, OAuthSessionType
from kenar import CreatePostAddonRequest

from kenar import (
    CreatePostAddonRequest,
    GetUserAddonsRequest,
    DeleteUserAddonRequest,
    GetPostAddonsRequest,
    DeletePostAddonRequest,
    CreateUserAddonRequest,
    IconName,
    Icon,
    TitleRow,
    SubtitleRow,
    SelectorRow,
    ScoreRow,
    LegendTitleRow,
    GroupInfo,
    EventRow,
    EvaluationRow,
    DescriptionRow,
    Color,
    WideButtonBar,
)


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
            base_url = reverse("fake-view")
            query_string = urlencode({
                "state": oauth_session.state,
                "access_token": oauth.access_token,
                "post_token": post.token
                })
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
            ), )

            kenar_client.chat.set_notify_chat_post_conversations(
                access_token=access_token_response.access_token,
                data=SetNotifyChatPostConversationsRequest(
                    post_token=chat.post.token,
                    endpoint=settings.APP_BASE_URL + reverse("receive_notify"),
                    identification_key=signer.sign(str(chat.id)),
                ),
            )
            base_url = reverse("fake-view")
            query_string = urlencode({
                "state": oauth_session.state,
                "access_token": oauth.access_token
                })
            url = f"{base_url}?{query_string}"
            logger.info("sep01 else callback")
            return redirect(url)

    except httpx.HTTPStatusError as http_err:
        logger.error(f"HTTP error occurred: {http_err}: {http_err.response.text}")
        return HttpResponseServerError("Internal server error")
    except Exception as err:
        logger.error(f"An error occurred: {err}")
        return HttpResponseServerError("Internal server error")


class FakeView(APIView):
    def get(self, request):
        logger.info("in fake",request.GET["access_token"])
        title_row = TitleRow(
            text="این یک نمونه تایتل میباشد", text_color=Color.TEXT_SECONDARY
        )
        
        kenar_client = get_divar_kenar_client()
        #kenar_client.addon.upload_image("")
        
        subtitle_row = SubtitleRow(text="این یک سابتایتل میباشد")

        desc_row = DescriptionRow(
            text="سلام - این یک ویجت تستی میباشد.",
            has_divider=True,
            is_primary=True,
            expandable=False,
            padded=True,
        )

        eval_row = EvaluationRow(
            indicator_text="متن اندیکاتور",
            indicator_percentage=50,
            indicator_icon=Icon(icon_name=IconName.DOWNLOAD),
            indicator_color=Color.SUCCESS_PRIMARY,
            left=EvaluationRow.Section(
                text="سمت چپ",
                text_color=Color.TEXT_SECONDARY,
                section_color=Color.SUCCESS_PRIMARY,
            ),
            middle=EvaluationRow.Section(
                text="وسط",
                text_color=Color.TEXT_SECONDARY,
                section_color=Color.TEXT_PRIMARY,
            ),
            right=EvaluationRow.Section(
                text="سمت راستی",
                text_color=Color.TEXT_SECONDARY,
                section_color=Color.TEXT_SECONDARY,
            ),
        )

        event_row = EventRow(
            title="تایتل",
            subtitle="سابتایتل",
            has_indicator=False,
            #image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoY3USrSPdY4jq7pzu9nYNPWwuxEv0Dh_K_w&s",
            label="لیبل",
            has_divider=True,
            link="https://www.test.com",
            padded=True,
            icon=Icon(icon_name=IconName.ADD),
        )

        group_info = GroupInfo(
            has_divider=True,
            items=[
                GroupInfo.GroupInfoItem(title="تایتل ۱", value="مقدار ۱"),
                GroupInfo.GroupInfoItem(title="تایتل ۲", value="مقدار ۲"),
                GroupInfo.GroupInfoItem(title="تایتل ۳", value="مقدار ۳"),
            ],
        )

        legend_title_row = LegendTitleRow(
            title="ارائه خدمت با کنار دیوار",
            subtitle="",
            has_divider=True,
            image_url="logo",
            tags=[
                LegendTitleRow.Tag(
                    text="احراز",
                    icon=Icon(icon_name=IconName.VERIFIED),
                    bg_color=LegendTitleRow.Tag.BackgroundColor.GRAY,
                ),
                LegendTitleRow.Tag(
                    text="کارشناسی",
                    icon=Icon(icon_name=IconName.CAR_INSPECTED),
                    bg_color=LegendTitleRow.Tag.BackgroundColor.TRANSPARENT,
                ),
                LegendTitleRow.Tag(
                    text="پرداخت امن",
                    icon=Icon(icon_name=IconName.ADD),
                    bg_color=LegendTitleRow.Tag.BackgroundColor.RED,
                ),
            ],
        )

        score_row_1 = ScoreRow(
            title="مدل امتیاز کیفی",
            descriptive_score="بسیار عالی",
            score_color=Color.TEXT_SECONDARY,
            link="",
            has_divider=True,
            icon=Icon(icon_name=IconName.ADD),
        )

        score_row_2 = ScoreRow(
            title="مدل امتیاز درصدی",
            percentage_score=100,
            score_color=Color.TEXT_SECONDARY,
            link="",
            has_divider=True,
            icon=Icon(icon_name=IconName.ADD),
        )

        selector_row = SelectorRow(
            title="این یک ویجت سلکتور میباشد",
            has_divider=True,
            has_arrow=True,
            icon=Icon(icon_name=IconName.INFO),
            link="https://www.test.com",
        )

        wide_button_bar = WideButtonBar(
            button=WideButtonBar.Button(
                title="به سمت سایت شما", link="https://www.test.com"
            ),
        )
        resp = kenar_client.addon.create_post_addon(
            access_token=request.GET["access_token"],
            data=CreatePostAddonRequest(
                token=request.GET["post_token"],
                widgets=[
                    title_row,
                    subtitle_row,
                    desc_row,
                    eval_row,
                    event_row,
                    group_info,
                    selector_row,
                    wide_button_bar,
                ],
            ),
        )
        print(resp)

        return Response({"message": request.GET}, status=status.HTTP_200_OK)
        pass
