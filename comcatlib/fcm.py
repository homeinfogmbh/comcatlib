"""Firebase Cloud Messaging."""

from logging import getLogger
from typing import Iterable, Sequence, Union

from firebase_admin import App, initialize_app
from firebase_admin.credentials import Certificate
from firebase_admin.messaging import AndroidConfig
from firebase_admin.messaging import AndroidNotification
from firebase_admin.messaging import APNSConfig
from firebase_admin.messaging import APNSPayload
from firebase_admin.messaging import Aps
from firebase_admin.messaging import MulticastMessage
from firebase_admin.messaging import Notification
from firebase_admin.messaging import WebpushConfig
from firebase_admin.messaging import WebpushNotification
from firebase_admin.messaging import WebpushNotificationAction
from firebase_admin.messaging import send
from peewee import ModelSelect

from comcatlib.orm import FCMToken, User


__all__ = [
    'delete_tokens',
    'get_tokens',
    'init',
    'multicast_message'
]


CERT_FILE = '/usr/local/etc/comcat.d/fcm.json'
LOGGER = getLogger(__file__)


def delete_tokens(user: Union[User, int], *tokens: str) -> None:
    """Deletes and existing FCM token."""

    condition = FCMToken.user == user

    if tokens:
        condition &= FCMToken.token << tokens

    for fcm_token in FCMToken.select().where(condition):
        fcm_token.delete_instance()


def get_tokens(users: Sequence[Union[User, int]]) -> ModelSelect:
    """Select all tokens of the given users."""

    return FCMToken.select().where(FCMToken.user << users)


def init() -> App:
    """Initialize the firebase app."""

    return initialize_app(Certificate(CERT_FILE))


def multicast_message(
        tokens: Iterable[str],
        *,
        urlcode: str,
        title: str,
        body: str
) -> str:
    """Multicast messages to the given tokens."""

    return send(
        MulticastMessage(
            tokens=list(tokens),
            data={'urlcode': urlcode},
            notification=Notification(title=title, body=body),
            android=AndroidConfig(
                notification=AndroidNotification(
                    click_action='FCM_PLUGIN_ACTIVITY'
                )
            )
        )
    )
