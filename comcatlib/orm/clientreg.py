"""Client registration tokens."""

from datetime import datetime, timedelta
from uuid import uuid4

from peewee import BooleanField, CharField, DateTimeField, ForeignKeyField

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['ClientRegistrationToken']


VALIDITY = timedelta(months=1)


class ClientRegistrationToken(ComCatModel):
    """One-time tokens for client registrations."""

    token = CharField(32, default=lambda: uuid4().hex)
    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    used = BooleanField(default=False)
    best_before = DateTimeField(default=lambda: datetime.now() + VALIDITY)

    @property
    def valid(self):
        """Determines whether the token is valid."""
        if self.used:
            return False

        if self.best_before < datetime.now():
            return False

        return True
