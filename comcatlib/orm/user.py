"""ComCat accounts."""

from datetime import datetime

from peewee import BooleanField
from peewee import DateTimeField
from peewee import ForeignKeyField

from his import CUSTOMER
from mdb import Tenement

from comcatlib.exceptions import DuplicateUser
from comcatlib.functions import get_tenement
from comcatlib.messages import NO_SUCH_USER
from comcatlib.orm.common import ComCatModel


__all__ = ['get_user', 'User']


def get_user(ident):
    """Returns the respective user."""

    condition = User.id == ident
    condition &= Tenement.customer == CUSTOMER.id

    try:
        return User.select().join(Tenement).where(condition).get()
    except User.DoesNotExist:
        raise NO_SUCH_USER


class User(ComCatModel):
    """A ComCat user."""

    tenement = ForeignKeyField(Tenement, column_name='tenement')
    created = DateTimeField(default=datetime.now)
    expires = DateTimeField(null=True)
    locked = BooleanField(default=False)
    admin = BooleanField(default=False)     # Admin across entire customer.

    @classmethod
    def from_json(cls, json, tenement, **kwargs):
        """Creates the user from the respective JSON data."""
        tenement = json.pop('tenement')
        user = super().from_json(json, **kwargs)
        user.tenement = tenement

        if user.unique:
            return user

        raise DuplicateUser()

    @property
    def expired(self):
        """Determines whether the user is expired."""
        return self.expires is not None and self.expires <= datetime.now()

    @property
    def valid(self):
        """Determines whether the user may be used."""
        return not self.locked and not self.expired

    @property
    def duplicates(self):
        """Returns the duplicates of this user."""
        cls = type(self)
        condition = cls.tenement == self.tenement

        if self.id is not None:
            condition &= cls.id != self.id

        return cls.select().where(condition)

    @property
    def is_unique(self):
        """Checks whether the user is unique for the tenement."""
        return not self.duplicates

    def patch_json(self, json, **kwargs):
        """Patches the user with the respective JSON data."""
        tenement = json.pop('tenement', None)

        if tenement is not None:
            self.tenement = get_tenement(tenement, self.customer)

        super().patch_json(json, **kwargs)

    def to_json(self, tenement=False, **kwargs):
        """Returns JSON-ish dict."""
        dictionary = super().to_json(**kwargs)

        if tenement:
            dictionary['tenement'] = self.tenement.to_json(**kwargs)

        return dictionary
