"""ORM models based on MySQL Alchemy."""

from peewee import ForeignKeyField

from peeweeplus.authlib import OAuth2ClientMixin
from peeweeplus.authlib import OAuth2TokenMixin
from peeweeplus.authlib import OAuth2AuthorizationCodeMixin

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['Client', 'Token', 'AuthorizationCode']


class Client(ComCatModel, OAuth2ClientMixin):
    """An OAuth client."""

    user = ForeignKeyField(User, column_name='user', ondelete='CASCADE')


class Token(ComCatModel, OAuth2TokenMixin):
    """An OAuth bearer token."""

    user = ForeignKeyField(User, column_name='user', ondelete='CASCADE')


class AuthorizationCode(ComCatModel, OAuth2AuthorizationCodeMixin):
    """An OAuth authorization code."""

    user = ForeignKeyField(User, column_name='user', ondelete='CASCADE')
