"""Nonces for client initialization."""

from __future__ import annotations
from uuid import UUID, uuid4

from peewee import ForeignKeyField, ModelSelect, UUIDField

from mdb import Address, Company, Customer, Tenement
from peeweeplus import HTMLCharField

from comcatlib.exceptions import NonceUsed
from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['AuthorizationNonce', 'EMailChangeNonce']


class Nonce(ComCatModel):
    """Basic Nonce."""

    user = ForeignKeyField(
        User, column_name='user', on_delete='CASCADE', lazy_load=False)
    uuid = UUIDField(default=uuid4)

    @classmethod
    def add(cls, user: User) -> Nonce:
        """Returns a new nonce for the given user."""
        nonce = cls(user=user)
        nonce.save()
        return nonce

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects nonces."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, User, Tenement, Customer, Company, Address, *args}
        return super().select(*args, **kwargs).join(User).join(Tenement).join(
            Customer).join(Company).join_from(Tenement, Address)

    @classmethod
    def use(cls, uuid: UUID) -> User:
        """Uses a nonce and returns its user."""
        try:
            nonce = cls.select(cascade=True).where(cls.uuid == uuid).get()
        except cls.DoesNotExist:
            raise NonceUsed() from None

        nonce.delete_instance()
        return nonce.user


class AuthorizationNonce(Nonce):
    """Nonces to authorize clients for users."""

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'authorization_nonce'


class EMailChangeNonce(Nonce):
    """Nonces to change email addresses."""

    email = HTMLCharField()

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'email_change_nonce'

    @classmethod
    def add(cls, user: User, email: str) -> EMailChangeNonce:
        """Adds a new email change nonce."""
        nonce = cls(user=user, email=email)
        nonce.save()
        return nonce
