"""OpenID Connect authorizationinterface."""

from pathlib import Path

from authlib.oidc.core import grants, UserInfo

from comcatlib.orm.oauth import AuthorizationCode


__all__ = ['OpenIDCode']


PRIVKEY = Path('/usr/local/etc/comcat/jwt.key')


class OpenIDCode(grants.OpenIDCode):
    """OpenID code handler."""

    def exists_nonce(self, nonce, request):     # pylint: disable=R0201
        """Tests if the nonce exists."""
        condition = AuthorizationCode.client_id == request.client_id
        condition &= AuthorizationCode.nonce == nonce

        try:
            AuthorizationCode.get(condition)
        except AuthorizationCode.DoesNotExist:
            return False

        return True

    def get_jwt_config(self, grant):    # pylint: disable=W0613,R0201
        """Returns the JSON web key configuration."""
        with PRIVKEY.open('r') as keyfile:
            private_key = keyfile.read()

        return {
            'key': private_key,
            'alg': 'RS512',
            'iss': 'https://homeinfo.de',
            'exp': 3600
        }

    def generate_user_info(self, user, scope):  # pylint: disable=W0613,R0201
        """Returns user information."""
        user_info = UserInfo(sub=user.id, name=user.uuid.hex())

        #if 'email' in scope:
        #    user_info['email'] = user.email

        return user_info
