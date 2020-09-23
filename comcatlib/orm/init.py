"""Client initialization."""

from uuid import uuid4

from peewee import ForeignKeyField, UUIDField

from comcatlib.exceptions import NonceUsed
from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['InitializationNonce']


class InitializationNonce(ComCatModel):
    """Nonces to initialize clients for users."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    nonce = UUIDField(default=uuid4)

    @classmethod
    def use(cls, nonce):
        """Uses a nonce and returns its user."""
        try:
            nonce = cls.get(cls.nonce == nonce)
        except cls.DoesNotExist:
            raise NonceUsed()

        nonce.delete_instance()
        return nonce.user
