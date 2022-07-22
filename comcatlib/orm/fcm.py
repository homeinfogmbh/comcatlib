"""Firebase Cloud Messaging models."""

from __future__ import annotations
from peewee import CharField, ForeignKeyField

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['FCMToken']


class FCMToken(ComCatModel):
    """An FCM token."""

    class Meta:
        table_name = 'fcm_token'

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    token = CharField(163, unique=True)
