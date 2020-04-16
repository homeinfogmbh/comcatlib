"""ORM models based on MySQL Alchemy."""

from peewee import ForeignKeyField

from authlib.common.security import generate_token
from peeweeplus.authlib import OAuth2ClientMixin
from peeweeplus.authlib import OAuth2TokenMixin
from peeweeplus.authlib import OAuth2AuthorizationCodeMixin

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['Client', 'Token', 'AuthorizationCode']


class Client(ComCatModel, OAuth2ClientMixin):   # pylint: disable=R0901
    """An OAuth client."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')


class Token(ComCatModel, OAuth2TokenMixin):     # pylint: disable=R0901
    """An OAuth bearer token."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')


class AuthorizationCode(ComCatModel, OAuth2AuthorizationCodeMixin):
    """An OAuth authorization code."""  # pylint: disable=R0901

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')

    def create_authorization_code(self, client, grant_user, request):
        """Method override for addional nonce for OpenID Connect."""
        code = generate_token(48)
        # openid request MAY have "nonce" parameter
        nonce = request.data.get('nonce')
        record = type(self)(
            code=code,
            client_id=client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            user_id=grant_user.id,
            nonce=nonce
        )
        record.save()
        return code
