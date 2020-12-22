"""ComCat accounts."""

from __future__ import annotations
from datetime import datetime
from typing import Iterable, Tuple

from argon2.exceptions import VerifyMismatchError
from peewee import BooleanField, DateTimeField, ForeignKeyField

from his import CUSTOMER
from mdb import Customer, Tenement
from peeweeplus import Argon2Field

from comcatlib.exceptions import DuplicateUser
from comcatlib.exceptions import InvalidPassword
from comcatlib.exceptions import UserExpired
from comcatlib.exceptions import UserLocked
from comcatlib.functions import genpw, get_tenement
from comcatlib.messages import NO_SUCH_USER
from comcatlib.orm.common import ComCatModel


__all__ = ['get_user', 'User']


def get_user(ident: int) -> User:
    """Returns the respective user."""

    condition = User.id == ident
    condition &= Tenement.customer == CUSTOMER.id

    try:
        return User.select().join(Tenement).where(condition).get()
    except User.DoesNotExist:
        raise NO_SUCH_USER from None


class User(ComCatModel):
    """A ComCat user."""

    tenement = ForeignKeyField(Tenement, column_name='tenement')
    created = DateTimeField(default=datetime.now)
    expires = DateTimeField(null=True)
    locked = BooleanField(default=False)
    admin = BooleanField(default=False)     # Admin across entire customer.
    passwd = Argon2Field()

    @classmethod
    def from_json(cls, json: dict, tenement: Tenement,
                  **kwargs) -> Tuple[User, str]:
        """Creates the user from the respective JSON data."""
        if 'passwd' in json:
            passwd = None
        else:
            json['passwd'] = passwd = genpw()

        user = super().from_json(json, **kwargs)
        user.tenement = tenement

        if user.is_unique:
            return (user, passwd)

        raise DuplicateUser()

    @property
    def customer(self) -> Customer:
        """Delegates to the tenement's customer."""
        return self.tenement.customer

    @property
    def expired(self) -> bool:
        """Determines whether the user is expired."""
        return self.expires is not None and self.expires <= datetime.now()

    @property
    def valid(self) -> bool:
        """Determines whether the user may be used."""
        return not self.locked and not self.expired

    @property
    def duplicates(self) -> Iterable[User]:
        """Returns the duplicates of this user."""
        cls = type(self)
        condition = cls.tenement == self.tenement

        if self.id is not None:
            condition &= cls.id != self.id

        return cls.select().where(condition)

    @property
    def is_unique(self) -> bool:
        """Checks whether the user is unique for the tenement."""
        return not self.duplicates

    def login(self, passwd: str) -> bool:
        """Authenticates the user."""
        if self.locked:
            raise UserLocked()

        if self.expired:
            raise UserExpired()

        try:
            self.passwd.verify(passwd)
        except VerifyMismatchError:
            raise InvalidPassword() from None

        if self.passwd.needs_rehash:
            self.passwd = passwd

        self.save()
        return True

    def patch_json(self, json: dict, **kwargs):
        """Patches the user with the respective JSON data."""
        tenement = json.pop('tenement', None)

        if tenement is not None:
            self.tenement = get_tenement(tenement, self.customer)

        super().patch_json(json, **kwargs)

    def to_json(self, tenement: bool = False, **kwargs) -> dict:
        """Returns JSON-ish dict."""
        dictionary = super().to_json(**kwargs)

        if tenement:
            dictionary['tenement'] = self.tenement.to_json(**kwargs)

        return dictionary
