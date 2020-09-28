"""Nonces for client initialization."""

from uuid import uuid4

from peewee import ForeignKeyField, UUIDField

from comcatlib.exceptions import NonceUsed
from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['AuthorizationNonce', 'InitializationNonce']


class _Nonce(ComCatModel):
    """Basic Nonce."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    uuid = UUIDField(default=uuid4)

    @classmethod
    def add(cls, user):
        """Returns a new nonce for the given user."""
        nonce = cls(user=user)
        nonce.save()
        return nonce.uuid.hex   # pylint: disable=E1101

    @classmethod
    def use(cls, uuid):
        """Uses a nonce and returns its user."""
        try:
            nonce = cls.get(cls.uuid == uuid)
        except cls.DoesNotExist:
            raise NonceUsed() from None

        # XXX: Allow repeated usage for testing only.
        #nonce.delete_instance()
        return nonce.user


class InitializationNonce(_Nonce):
    """Nonces to initialize clients for users."""

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'initialization_nonce'

    @property
    def url(self):
        """Returns the URL."""
        return f'de.homeinfo.comcat://register/{self.uuid.hex}'


class AuthorizationNonce(_Nonce):
    """Nonces to authorize clients for users."""

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'authorization_nonce'
