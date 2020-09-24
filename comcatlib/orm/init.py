"""Client initialization."""

from uuid import uuid4

from peewee import ForeignKeyField, UUIDField

from comcatlib.exceptions import NonceUsed
from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['InitializationNonce']


class InitializationNonce(ComCatModel):     # pylint: disable=R0903
    """Nonces to initialize clients for users."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    uuid = UUIDField(default=uuid4)

    @classmethod
    def use(cls, uuid):
        """Uses a nonce and returns its user."""
        try:
            nonce = cls.get(cls.uuid == uuid)
        except cls.DoesNotExist:
            raise NonceUsed() from None

        nonce.delete_instance()
        return nonce.user
