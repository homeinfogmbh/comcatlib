"""ORM models based on MySQL Alchemy."""

from __future__ import annotations
from datetime import datetime
from typing import Any
from uuid import uuid4

from peewee import ForeignKeyField, ModelSelect

from authlib.common.security import generate_token
from mdb import Address, Company, Customer, Tenement
from peeweeplus import Transaction
from peeweeplus.authlib import OAuth2ClientMixin
from peeweeplus.authlib import OAuth2TokenMixin
from peeweeplus.authlib import OAuth2AuthorizationCodeMixin

from comcatlib.config import OAUTH2
from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User
from comcatlib.pwgen import genpw


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

    user = ForeignKeyField(
        User, column_name='user', on_delete='CASCADE', lazy_load=False)

    @classmethod
    def add(cls, user: User) -> Client:
        """Adds a new client for the given user."""
        client = cls(
            user=user,
            client_id=uuid4().hex,
            client_id_issued_at=datetime.now().timestamp(),
            token_endpoint_auth_method=OAUTH2.get('token_endpoint_auth_method')
        )
        client.client_secret = secret = genpw()     # pylint: disable=W0201
        transaction = Transaction()
        transaction.add(client, primary=True)

        for uri in OAUTH2.get('redirect_uris', []):
            transaction.add(RedirectURI(client=client, uri=uri))

        for typ in OAUTH2.get('grant_types', []):
            transaction.add(GrantType(client=client, type=typ))

        for typ in OAUTH2.get('response_types', []):
            transaction.add(ResponseType(client=client, type=typ))

        for scope in OAUTH2.get('scopes', []):
            transaction.add(Scope(client=client, scope=scope))

        for contact in OAUTH2.get('contacts', []):
            transaction.add(Contact(client=client, contact=contact))

        for jwk in OAUTH2.get('jwks', []):
            transaction.add(JWKS(client=client, jwk=jwk))

        return (transaction, secret)

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects clients."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, User, Tenement, Customer, Company, Address, *args}
        return super().select(*args, **kwargs).join(User).join(Tenement).join(
            Customer).join(Company).join_from(Tenement, Address)


RedirectURI, GrantType, ResponseType, Scope, Contact, JWKS = \
    Client.get_related_models(ComCatModel)


class Token(ComCatModel, OAuth2TokenMixin):     # pylint: disable=R0901,R0903
    """An OAuth bearer token."""

    user = ForeignKeyField(
        User, column_name='user', on_delete='CASCADE', lazy_load=False)

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects clients."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, User, Tenement, Customer, Company, Address, *args}
        return super().select(*args, **kwargs).join(User).join(Tenement).join(
            Customer).join(Company).join_from(Tenement, Address)


class AuthorizationCode(ComCatModel, OAuth2AuthorizationCodeMixin):
    """An OAuth authorization code."""  # pylint: disable=R0901

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'authorization_code'

    user = ForeignKeyField(
        User, column_name='user', on_delete='CASCADE', lazy_load=False)

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects clients."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, User, Tenement, Customer, Company, Address, *args}
        return super().select(*args, **kwargs).join(User).join(Tenement).join(
            Customer).join(Company).join_from(Tenement, Address)

    def create_authorization_code(self, client: Client, grant_user: User,
                                  request: Any) -> str:
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
