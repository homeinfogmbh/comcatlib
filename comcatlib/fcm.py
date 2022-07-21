"""Firebase Cloud Messaging."""

from logging import getLogger
from typing import Union

from firebase_admin import App, initialize_app
from firebase_admin.credentials import Certificate
from firebase_admin.messaging import AndroidConfig
from firebase_admin.messaging import AndroidNotification
from firebase_admin.messaging import APNSConfig
from firebase_admin.messaging import APNSPayload
from firebase_admin.messaging import Aps
from firebase_admin.messaging import Message
from firebase_admin.messaging import Notification
from firebase_admin.messaging import WebpushConfig
from firebase_admin.messaging import WebpushNotification
from firebase_admin.messaging import WebpushNotificationAction
from firebase_admin.messaging import send

from comcatlib.orm import FCMToken, User


__all__ = [
    'add_token',
    'delete_tokens',
    'init',
    'message_user',
    'send_message'
]


CERT_FILE = '/usr/local/etc/comcat.d/fcm.json'
LOGGER = getLogger(__file__)


def add_token(user: Union[User, int]) -> str:
    """Generates a new FCM token."""

    fcm_token = FCMToken(user=user)
    fcm_token.save()
    return fcm_token.token


def delete_tokens(user: Union[User, int], *tokens: str) -> None:
    """Deletes and existing FCM token."""

    condition = FCMToken.user == user

    if tokens:
        condition &= FCMToken.token << tokens

    for fcm_token in FCMToken.select().where(condition):
        fcm_token.delete_instance()


def init() -> App:
    """Initialize the firebase app."""

    return initialize_app(Certificate(CERT_FILE))


def message_user(
        user: Union[User, int],
        *,
        urlcode: str,
        title: str,
        body: str
) -> dict[str, str]:
    """Message a user."""

    results = {}

    for token in FCMToken.select().where(FCMToken.user == user):
        results[token] = send_message(
            token := token.token, urlcode=urlcode, title=title, body=body
        )

    return results


def send_message(
        token: str,
        *,
        urlcode: str,
        title: str,
        body: str
) -> str:
    """Sends a message."""

    return send(
        Message(
            notification=Notification(title=title, body=body),
            android=AndroidConfig(
                notification=AndroidNotification(click_action=urlcode)
            ),
            apns=APNSConfig(
                payload=APNSPayload(
                    aps=Aps(custom_data={'urlcode': urlcode})
                )
            ),
            webpush=WebpushConfig(
                notification=WebpushNotification(
                    actions=[WebpushNotificationAction(urlcode, 'öffnen')]
                )
            ),
            token=token
        )
    )
