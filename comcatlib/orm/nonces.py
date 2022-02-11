"""Nonces for client initialization."""

from __future__ import annotations
from datetime import datetime, timedelta
from typing import Union
from uuid import UUID, uuid4

from peewee import DateTimeField, ForeignKeyField, Select, UUIDField

from mdb import Address, Company, Customer, Tenement
from peeweeplus import HTMLCharField

from comcatlib.exceptions import NonceUsed, PasswordResetPending
from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['AuthorizationNonce', 'EMailChangeNonce', 'PasswordResetNonce']


class Nonce(ComCatModel):
    """Basic Nonce."""

    user = ForeignKeyField(
        User, column_name='user', on_delete='CASCADE', lazy_load=False)
    uuid = UUIDField(default=uuid4)

    @classmethod
    def add(cls, user: Union[User, int]) -> Nonce:
        """Returns a new nonce for the given user."""
        nonce = cls(user=user)
        nonce.save()
        return nonce

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> Select:
        """Selects nonces."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, User, Tenement, Customer, Company, Address, *args}
        return super().select(*args, **kwargs).join(User).join(Tenement).join(
            Customer).join(Company).join_from(Tenement, Address)

    @classmethod
    def use(cls, uuid: UUID) -> Nonce:
        """Uses a nonce and returns its user."""
        try:
            nonce = cls.select(cascade=True).where(cls.uuid == uuid).get()
        except cls.DoesNotExist:
            raise NonceUsed() from None

        nonce.delete_instance()
        return nonce


class AuthorizationNonce(Nonce):
    """Nonces to authorize clients for users."""

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'authorization_nonce'


class EMailChangeNonce(Nonce):
    """Nonces to change email addresses."""

    email = HTMLCharField()

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'email_change_nonce'

    @classmethod    # pylint: disable-next=W0221
    def add(cls, user: Union[User, int], email: str) -> EMailChangeNonce:
        """Adds a new email change nonce."""
        nonce = cls(user=user, email=email)
        nonce.save()
        return nonce

    @classmethod
    def use(cls, uuid: UUID) -> EMailChangeNonce:
        """Uses the nonce."""
        nonce = super().use(uuid)
        (user := nonce.user).email = nonce.email
        user.save()
        return nonce


class PasswordResetNonce(Nonce):
    """Nonce to reset the password."""

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'password_reset_nonce'

    VALIDITY = timedelta(days=1)

    issued = DateTimeField(default=datetime.now)

    @classmethod
    def clean(cls, user: User) -> None:
        """Remove all outdated nonces for the given user."""
        return cls.delete().where(
            (cls.user == user)
            & (cls.issued < (datetime.now() + cls.VALIDITY))
        )

    @classmethod
    def generate(cls, user: User) -> PasswordResetNonce:
        """Generates a password reset nonce for the given user."""
        cls.clean(user)

        try:
            cls.get(cls.user == user)
        except cls.DoesNotExist:
            return cls(user=user)

        raise PasswordResetPending()

    @classmethod
    def use(cls, uuid: UUID) -> User:
        """Uses a nonce and returns its user."""
        if not (nonce := super().use(uuid)).is_valid():
            raise NonceUsed()

        return nonce

    def is_valid(self) -> bool:
        """Checks if the nonce is valid."""
        return self.issued + self.VALIDITY >= datetime.now()
