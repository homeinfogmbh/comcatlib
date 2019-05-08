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

from comcatlib.contextlocals import CUSTOMER
from comcatlib.exceptions import AccountLocked
from comcatlib.exceptions import InvalidCredentials
from comcatlib.messages import NO_SUCH_ACCOUNT, NO_SUCH_ADDRESS
from comcatlib.orm.address import Address
from comcatlib.orm.common import ComCatModel
from comcatlib.orm.tenement import Tenement


__all__ = ['get_account', 'Account']


MAX_FAILED_LOGINS = 5


def _extract_tenement(json, customer):
    """Returns the respective address."""

    ident = json.pop('tenement')

    if ident is None:
        return None

    try:
        return Tenement.get(
            (Tenement.id == ident)
            & (Tenement.customer == customer))
    except Address.DoesNotExist:
        raise NO_SUCH_ADDRESS


def get_account(ident):
    """Returns the respective account."""

    try:
        return Account.get(
            (Account.id == ident) & (Account.customer == CUSTOMER.id))
    except Account.DoesNotExist:
        raise NO_SUCH_ACCOUNT


class Account(ComCatModel):
    """A ComCat account."""

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
    admin = BooleanField(default=False)
    root = BooleanField(default=False)

    @classmethod
    def add(cls, customer, tenement=None, passwd=None):
        """Creates a new account."""
        account = cls()
        account.customer = customer
        account.tenement = tenement
        account.passwd = passwd
        account.save()
        return account

    @classmethod
    def from_json(cls, json, customer, **kwargs):
        """Creates the account from the respective JSON data."""
        try:
            tenement = json.pop('tenement', None)
        except KeyError:
            tenement = None
        else:
            tenement = Tenement.by_value(tenement, customer)

        account = super().from_json(json, **kwargs)
        account.customer = customer
        account.tenement = tenement
        return account

    @property
    def expired(self):
        """Determines whether the account is expired."""
        return self.expires is not None and self.expires <= datetime.now()

    @property
    def valid(self):
        """Determines whether the account may be used."""
        return not self.locked and not self.expired and self.passwd is not None

    @property
    def can_login(self):
        """Determines whether the account may login."""
        return self.valid and self.failed_logins <= MAX_FAILED_LOGINS

    @property
    def instance(self):
        """Returns the account instance.
        This is used to get the actual
        account model from a LocalProxy.
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

        raise AccountLocked()

    def patch_json(self, json, **kwargs):
        """Patches the account with the respective JSON data."""
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
