"""Object-relational mappings."""

from datetime import datetime, timedelta
from uuid import uuid4

from argon2.exceptions import VerifyMismatchError
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import UUIDField

from mdb import Customer
from peeweeplus import MySQLDatabase, JSONModel, Argon2Field

from comcatlib.config import CONFIG
from comcatlib.config import ALLOWED_SESSION_DURATIONS
from comcatlib.config import DEFAULT_SESSION_DURATION
from comcatlib.exceptions import AccountLocked
from comcatlib.exceptions import DurationOutOfBounds
from comcatlib.exceptions import InvalidSession
from comcatlib.exceptions import InvalidCredentials


__all__ = ['Account', 'Session']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])
MAX_FAILED_LOGINS = 5


class _ComCatModel(JSONModel):
    """Basic comcat model."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


class Account(_ComCatModel):
    """A ComCat account."""

    uuid = UUIDField(default=uuid4)
    passwd = Argon2Field(null=True)
    customer = ForeignKeyField(Customer, column_name='customer')
    annotation = CharField(255)
    created = DateTimeField(default=datetime.now)
    last_login = DateTimeField(null=True)
    failed_logins = IntegerField(default=0)
    expires = DateTimeField(null=True)
    locked = BooleanField(default=False)

    @classmethod
    def add(cls, customer, passwd=None):
        """Creates a new account."""
        account = cls()
        account.customer = customer
        account.passwd = passwd
        account.save()
        return account

    @property
    def expired(self):
        """Determines whether the account is expired."""
        return self.expires is None or self.expires > datetime.now()

    @property
    def valid(self):
        """Determines whether the account may be used."""
        return not self.locked and not self.expired and self.passwd is not None

    @property
    def can_login(self):
        """Determines whether the account may login."""
        return self.valid and self.failed_logins <= MAX_FAILED_LOGINS

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


class Session(_ComCatModel):
    """A ComCat session."""

    token = UUIDField(default=uuid4)
    account = ForeignKeyField(
        Account, column_name='account', backref='sessions',
        on_delete='CASCADE')
    start = DateTimeField(default=datetime.now)
    end = DateTimeField()

    @classmethod
    def open(cls, account, duration=DEFAULT_SESSION_DURATION):
        """Opens a new session for the respective account."""
        if duration not in ALLOWED_SESSION_DURATIONS:
            raise DurationOutOfBounds()

        now = datetime.now()
        duration = timedelta(minutes=duration)
        session = cls(account=account, start=now, end=now+duration)
        session.save()
        return session

    @classmethod
    def fetch(cls, token):
        """Returns the respective session."""
        try:
            session = cls.get(cls.token == token)
        except cls.DoesNotExist:
            raise InvalidSession()

        if session.valid:
            return session

        raise InvalidSession()

    @property
    def alive(self):
        """Determines whether the session is alive."""
        return self.start <= datetime.now() <= self.end

    @property
    def valid(self):
        """Determines whether the session is valid."""
        return self.alive and self.account.valid

    def renew(self, duration=DEFAULT_SESSION_DURATION):
        """Renews the session."""
        if duration not in ALLOWED_SESSION_DURATIONS:
            raise DurationOutOfBounds()

        if not self.account.can_login:
            raise AccountLocked()

        self.end = datetime.now() + timedelta(minutes=duration)
        self.save()
        return self
