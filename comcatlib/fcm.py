"""Firebase Cloud Messaging."""

from enum import Enum
from logging import getLogger
from typing import Iterable, Iterator, Union

from firebase_admin import App, initialize_app
from firebase_admin.credentials import Certificate
from firebase_admin.messaging import AndroidConfig
from firebase_admin.messaging import AndroidNotification
from firebase_admin.messaging import BatchResponse
from firebase_admin.messaging import MulticastMessage
from firebase_admin.messaging import Notification
from firebase_admin.messaging import send_multicast
from peewee import ModelSelect

from cmslib import BaseChart, Group, GroupBaseChart

from comcatlib.orm import FCMToken, GroupMemberUser, User, UserBaseChart


__all__ = [
    'APP_NAME',
    'CAPTIONS',
    'URLCode',
    'delete_tokens',
    'expand_groups',
    'get_tokens',
    'groups_users',
    'init',
    'multicast_base_chart',
    'multicast_message'
]


APP_NAME = 'MieterApp'
CERT_FILE = '/usr/local/etc/comcat.d/fcm.json'
LOGGER = getLogger(__file__)


class URLCode(str, Enum):
    """Available URL codes."""

    NEWS = 'news'
    DOWNLOAD = DOCUMENTS = 'download'
    EVENTS = 'events'
    CONTACT = TENANT_TO_LANDLORD = 'contact'


CAPTIONS = {
    URLCode.NEWS: 'Neue News',
    URLCode.DOWNLOAD: 'Neuer Download'
}


def delete_tokens(user: Union[User, int], *tokens: str) -> None:
    """Deletes and existing FCM token."""

    condition = FCMToken.user == user

    if tokens:
        condition &= FCMToken.token << tokens

    for fcm_token in FCMToken.select().where(condition):
        fcm_token.delete_instance()


def expand_groups(
        groups: Iterable[Union[Group, int]]
) -> set[Union[Group, int]]:
    """Expand the group into its children."""

    groups = children = set(groups)

    while children := set(Group.select().where(Group.parent << children)):
        groups |= children

    LOGGER.info('Expanded groups: %s', groups)
    return groups


def get_tokens(users: Iterable[Union[User, int]]) -> ModelSelect:
    """Select all tokens of the given users."""

    return FCMToken.select().where(FCMToken.user << users)


def groups_users(
        groups: Iterable[Union[Group, int]]
) -> Iterator[Union[User, int]]:
    """Yield users that are members of the respective groups."""

    for member in GroupMemberUser.select().where(
            GroupMemberUser.group << groups
    ):
        LOGGER.info('Group user: %s', member.user)
        yield member.user


def init() -> App:
    """Initialize the firebase app."""

    return initialize_app(Certificate(CERT_FILE))


def multicast_base_chart(
        base_chart: BaseChart,
        url_code: URLCode
) -> BatchResponse:
    """Multicast base chart to users."""

    return multicast_message(
        [
            token.token for token in
            get_tokens(set(affected_users_by_base_chart(base_chart)))
        ],
        url_code=url_code,
        title=f'{APP_NAME}: {CAPTIONS[url_code]}',
        body=base_chart.title
    )


def multicast_message(
        tokens: Iterable[str],
        *,
        url_code: URLCode,
        title: str,
        body: str
) -> BatchResponse:
    """Multicast messages to the given tokens."""

    LOGGER.info('Sending multicast message.')
    LOGGER.info('Title: "%s"', title)
    LOGGER.info('Body: "%s"', body)
    LOGGER.info('URL Code: "%s"', url_code)
    LOGGER.info('Tokens: %s', tokens)
    return send_multicast(
        MulticastMessage(
            tokens=list(tokens),
            data={'urlcode': url_code},
            notification=Notification(title=title, body=body),
            android=AndroidConfig(
                notification=AndroidNotification(
                    click_action='FCM_PLUGIN_ACTIVITY'
                )
            )
        )
    )


def affected_users_by_base_chart(
        base_chart: Union[BaseChart, int]
) -> Iterator[Union[User, int]]:
    """Return a set of users affected by the
    change to the respective chart mapping.
    """

    for user_base_chart in UserBaseChart.select().where(
            UserBaseChart.base_chart == base_chart
    ):
        LOGGER.info('Base chart user: %s', user_base_chart.user)
        yield user_base_chart.user

    yield from groups_users(expand_groups({
        group_base_chart.group for
        group_base_chart in GroupBaseChart.select().where(
            GroupBaseChart.base_chart == base_chart
        )
    }))
