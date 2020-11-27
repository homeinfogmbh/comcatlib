"""Nonces for client initialization."""

from __future__ import annotations
from uuid import UUID, uuid4

from peewee import ForeignKeyField, UUIDField

from comcatlib.exceptions import NonceUsed
from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['AuthorizationNonce']


class Nonce(ComCatModel):
    """Basic Nonce."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    uuid = UUIDField(default=uuid4)

    @classmethod
    def add(cls, user: User) -> Nonce:
        """Returns a new nonce for the given user."""
        nonce = cls(user=user)
        nonce.save()
        return nonce

    @classmethod
    def use(cls, uuid: UUID) -> User:
        """Uses a nonce and returns its user."""
        try:
            nonce = cls.get(cls.uuid == uuid)
        except cls.DoesNotExist:
            raise NonceUsed() from None

        return nonce.user


class AuthorizationNonce(Nonce):
    """Nonces to authorize clients for users."""

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'authorization_nonce'
