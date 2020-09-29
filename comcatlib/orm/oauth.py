"""ORM models based on MySQL Alchemy."""

from datetime import datetime
from enum import Enum
from uuid import uuid4

from peewee import ForeignKeyField

from authlib.common.security import generate_token
from peeweeplus import Transaction
from peeweeplus.authlib import OAuth2ClientMixin
from peeweeplus.authlib import OAuth2TokenMixin
from peeweeplus.authlib import OAuth2AuthorizationCodeMixin

from comcatlib.orm.common import ComCatModel
from comcatlib.functions import genpw
from comcatlib.orm.user import User


__all__ = [
    'Client',
    'RedirectURI',
    'GrantType',
    'ResponseType',
    'Scope',
    'Contact',
    'JWKS',
    'Token',
    'AuthorizationCode'
]


class Defaults(Enum):
    """Client defaults."""

    REDIRECT_URIS = [
        'https://comcat.homeinfo.de/oauth/authorize',
        'https://comcat.homeinfo.de/oauth/token',
        'de.homeinfo.comcat://auth',
        'de.homeinfo.comcat://token'
    ]
    GRANT_TYPES = ['authorization_code', 'refresh_token']
    RESPONSE_TYPES = ['code', 'token']
    SCOPES = ['comcat']
    CONTACTS = []
    JWKS = []


class Client(ComCatModel, OAuth2ClientMixin):   # pylint: disable=R0901
    """An OAuth client."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')

    @classmethod
    def add(cls, user):
        """Adds a new client for the given user."""
        client = cls(user=user)
        client.client_id = uuid4().hex
        client.client_id_issued_at = datetime.now().timestamp()
        client.client_secret = secret = genpw()
        transaction = Transaction()
        transaction.add(client, primary=True)

        for uri in Defaults.REDIRECT_URIS:
            transaction.add(RedirectURI(client=client, uri=uri))

        for typ in Defaults.GRANT_TYPES:
            transaction.add(GrantType(client=client, type=typ))

        for typ in Defaults.RESPONSE_TYPES:
            transaction.add(ResponseType(client=client, type=typ))

        for scope in Defaults.SCOPES:
            transaction.add(Scope(client=client, scope=scope))

        for contact in Defaults.CONTACTS:
            transaction.add(Contact(client=client, contact=contact))

        for jwk in Defaults.JWKS:
            transaction.add(JWKS(client=client, jwk=jwk))

        return (transaction, secret)


RedirectURI, GrantType, ResponseType, Scope, Contact, JWKS = \
    Client.get_related_models(ComCatModel)


class Token(ComCatModel, OAuth2TokenMixin):     # pylint: disable=R0901
    """An OAuth bearer token."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')


class AuthorizationCode(ComCatModel, OAuth2AuthorizationCodeMixin):
    """An OAuth authorization code."""  # pylint: disable=R0901

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'authorization_code'

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')

    def create_authorization_code(self, client, grant_user, request):
        """Method override with addional nonce for OpenID Connect."""
        code = generate_token(48)
        record = type(self)(
            code=code,
            client_id=client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            user_id=grant_user.id,
            # OpenID request *may* have "nonce" parameter
            nonce=request.data.get('nonce')
        )
        record.save()
        return code
