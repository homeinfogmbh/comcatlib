"""ORM models based on MySQL Alchemy."""

from mdb import Customer
from peewee import CharField, ForeignKeyField, Model

from peeweeplus import Argon2Field, MySQLDatabase
from peeweeplus.authlib import OAuth2ClientMixin
from peeweeplus.authlib import OAuth2TokenMixin
from peeweeplus.authlib import OAuth2AuthorizationCodeMixin

from comcatlib.orm.user import ComCatModel, User
from comcatlib.orm.common import ComCatModel, User


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