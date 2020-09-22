"""ORM models based on MySQL Alchemy."""

from datetime import datetime
from random import choices
from string import ascii_letters, digits
from uuid import uuid4

from peewee import ForeignKeyField

from authlib.common.security import generate_token
from peeweeplus import Transaction
from peeweeplus.authlib import OAuth2ClientMixin
from peeweeplus.authlib import OAuth2TokenMixin
from peeweeplus.authlib import OAuth2AuthorizationCodeMixin

from comcatlib.orm.common import ComCatModel
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


class Client(ComCatModel, OAuth2ClientMixin):   # pylint: disable=R0901
    """An OAuth client."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')

    @classmethod
    def from_json(cls, json, user, **kwargs):
        """Creates a new client from a JSON-ish dict."""
        if json.pop('user', None) is not None:
            raise ValueError('Setting of user is not allowed.')

        if json.pop('clientId', None) is not None:
            raise ValueError('Setting of client ID is not allowed.')

        if json.pop('clientSecret', None) is not None:
            raise ValueError('Setting of client secret is not allowed.')

        if json.pop('client_id_issued_at', None) is not None:
            raise ValueError('Setting of ID issued timestamp is not allowed.')

        redirect_uris = json.pop('redirectURIs', None) or ()
        grant_types = json.pop('grantTypes', None) or ()
        response_types = json.pop('responseTypes', None) or ()
        scopes = json.pop('scopes', None) or ()
        contacts = json.pop('contacts', None) or ()
        jwks = json.pop('jwks', None) or ()
        client = super().from_json(json, **kwargs)
        client.user = user
        client.client_id = uuid4().hex
        client.client_id_issued_at = datetime.now().timestamp()
        client.client_secret = secret = choices(ascii_letters+digits, k=32)
        transaction = Transaction()
        transaction.add(client, primary=True)

        for uri in redirect_uris:
            transaction.add(RedirectURI(client=client, uri=uri))

        for typ in grant_types:
            transaction.add(GrantType(client=client, type=typ))

        for typ in response_types:
            transaction.add(ResponseType(client=client, type=typ))

        for scope in scopes:
            transaction.add(Scope(client=client, scope=scope))

        for contact in contacts:
            transaction.add(Contact(client=client, contact=contact))

        for jwk in jwks:
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
