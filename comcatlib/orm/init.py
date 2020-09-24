"""Client initialization."""

from uuid import uuid4

from peewee import ForeignKeyField, UUIDField

from comcatlib.exceptions import NonceUsed
from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['AuthorizationNonce', 'InitializationNonce']


class InitializationNonce(ComCatModel):     # pylint: disable=R0903
    """Nonces to initialize clients for users."""

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'initialization_nonce'

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

        nonce.delete_instance()
        return nonce.user


class AuthorizationNonce(InitializationNonce):
    """Nonces to authorize clients for users."""

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'authorization_nonce'
