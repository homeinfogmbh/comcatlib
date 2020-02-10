"""ComCat accounts."""

from datetime import datetime
from uuid import uuid4

from argon2.exceptions import VerifyMismatchError
from peewee import BooleanField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import UUIDField

from mdb import Customer
from peeweeplus import Argon2Field

from comcatlib.exceptions import InvalidCredentials, UserLocked
from comcatlib.orm.common import ComCatModel
from comcatlib.orm.tenement import Tenement


__all__ = ['User']


MAX_FAILED_LOGINS = 5


class User(ComCatModel):
    """A ComCat user."""

    uuid = UUIDField(default=uuid4)
    passwd = Argon2Field(null=True)
    customer = ForeignKeyField(Customer, column_name='customer')
    tenement = ForeignKeyField(
        Tenement, column_name='tenement', null=True, on_delete='SET NULL',
        on_update='CASCADE')
    created = DateTimeField(default=datetime.now)
    last_login = DateTimeField(null=True)
    failed_logins = IntegerField(default=0)
    expires = DateTimeField(null=True)
    locked = BooleanField(default=False)
    admin = BooleanField(default=False)     # Admin across entire customer.
    root = BooleanField(default=False)      # Admin across all users.

    @classmethod
    def add(cls, customer, tenement=None, passwd=None):
        """Creates a new user."""
        user = cls()
        user.customer = customer
        user.tenement = tenement
        user.passwd = passwd
        user.save()
        return user

    @classmethod
    def from_json(cls, json, customer, **kwargs):
        """Creates the user from the respective JSON data."""
        tenement = json.pop('tenement', None)

        if tenement is not None:
            tenement = Tenement.by_value(tenement, customer)

        user = super().from_json(json, **kwargs)
        user.customer = customer
        user.tenement = tenement
        return user

    @property
    def expired(self):
        """Determines whether the user is expired."""
        return self.expires is not None and self.expires <= datetime.now()

    @property
    def valid(self):
        """Determines whether the user may be used."""
        return not self.locked and not self.expired and self.passwd is not None

    @property
    def can_login(self):
        """Determines whether the user may login."""
        return self.valid and self.failed_logins <= MAX_FAILED_LOGINS

    @property
    def instance(self):
        """Returns the user instance.
        This is used to get the actual
        user model from a LocalProxy.
        """
        return self

    def login(self, passwd):
        """Performs a login."""
        if self.can_login:
            try:
                self.passwd.verify(passwd)
            except VerifyMismatchError:
                self.failed_logins += 1
                self.save()
                raise InvalidCredentials()

            if self.passwd.needs_rehash:
                self.passwd = passwd

            self.failed_logins = 0
            self.last_login = datetime.now()
            self.save()
            return True

        raise UserLocked()

    def patch_json(self, json, **kwargs):
        """Patches the user with the respective JSON data."""
        try:
            tenement = json.pop('tenement')
        except KeyError:
            tenement = self.tenement
        else:
            tenement = Tenement.by_value(tenement, self.customer)

        super().patch_json(json, **kwargs)
        self.tenement = tenement

    def to_json(self, cascade=False, **kwargs):
        """Returns JSON-ish dict."""
        dictionary = super().to_json(**kwargs)

        if cascade and self.tenement is not None:
            dictionary['tenement'] = self.tenement.to_json(
                cascade=cascade, **kwargs)

        return dictionary
