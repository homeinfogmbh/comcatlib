"""Firebase Cloud Messaging tokens."""

from __future__ import annotations
from firebase_admin.auth import create_custom_token
from peewee import CharField, ForeignKeyField

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['FCMToken']


class FCMToken(ComCatModel):
    """An FCM token."""

    class Meta:
        table_name = 'fcm_token'

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    token = CharField(162, unique=True)

    @classmethod
    def for_user(cls, user: User) -> FCMToken:
        """Creates a new FCM token for the given user."""
        return cls(user=user, token=create_custom_token(user.email).decode())
