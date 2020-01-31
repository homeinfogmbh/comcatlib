"""Object-relational mappings."""

from datetime import datetime, timedelta
from uuid import uuid4

from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import UUIDField

from comcatlib.config import ALLOWED_SESSION_DURATIONS
from comcatlib.config import DEFAULT_SESSION_DURATION
from comcatlib.exceptions import AccountLocked
from comcatlib.exceptions import DurationOutOfBounds
from comcatlib.exceptions import InvalidSession
from comcatlib.orm.user import User
from comcatlib.orm.common import ComCatModel


__all__ = ['Session']


class Session(ComCatModel):
    """A ComCat session."""

    token = UUIDField(default=uuid4)
    user = ForeignKeyField(
        User, column_name='user', backref='sessions', on_delete='CASCADE')
    start = DateTimeField(default=datetime.now)
    end = DateTimeField()

    @classmethod
    def open(cls, user, duration=DEFAULT_SESSION_DURATION):
        """Opens a new session for the respective user."""
        if duration not in ALLOWED_SESSION_DURATIONS:
            raise DurationOutOfBounds()

        now = datetime.now()
        duration = timedelta(minutes=duration)
        session = cls(user=user, start=now, end=now+duration)
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
        return self.alive and self.user.valid

    def renew(self, duration=DEFAULT_SESSION_DURATION):
        """Renews the session."""
        if duration not in ALLOWED_SESSION_DURATIONS:
            raise DurationOutOfBounds()

        if not self.user.can_login:
            raise AccountLocked()

        self.end = datetime.now() + timedelta(minutes=duration)
        self.save()
        return self
