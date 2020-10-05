"""HISFS-like file associations and quotas."""

from peewee import BigIntegerField, CharField, ForeignKeyField

from filedb import File as FileDBFile
from hisfs import get_sparse_file
from mdb import Customer

from comcatlib.exceptions import QuotaExceeded
from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['UserFile', 'Quota']


DEFAULT_QUOTA = 10 * (1024 ** 2)    # 10 MiB.


class UserFile(ComCatModel):
    """A user's file."""

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'user_file'

    name = CharField(255, null=True)
    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    file = ForeignKeyField(FileDBFile, column_name='file')

    @classmethod
    def add(cls, user, bytes_, name=None):
        """Adds the respective file."""
        file = cls()
        file.name = name
        file.user = user
        file.file = FileDBFile.from_bytes(bytes_, save=True)
        file.save()
        return file

    @property
    def metadata(self):
        """Returns file meta data."""
        return get_sparse_file(self.file_id)

    @property
    def bytes(self):
        """Returns the file's bytes."""
        return self.file.bytes

    def stream(self):
        """Returns HTTP stream."""
        return self.file.stream()

    def save(self, *args, **kwargs):
        """Saves the filedb.File first."""
        if self.file:
            self.file.save(*args, **kwargs)

        return super().save(*args, **kwargs)

    def to_json(self, *args, **kwargs):
        """Returns a JSON-ish dict."""
        json = super().to_json(*args, **kwargs)
        metadata = self.metadata.to_json(*args, **kwargs)
        json.update(metadata)
        return json


class Quota(ComCatModel):
    """Per-customer file quota."""

    customer = ForeignKeyField(
        Customer, column_name='customer', unique=True, on_delete='CASCADE',
        on_update='CASCADE')
    quota = BigIntegerField(default=DEFAULT_QUOTA)  # Per-user quota in bytes.

    @classmethod
    def for_customer(cls, customer):
        """Returns the quota for the respective customer."""
        try:
            return cls.get(cls.customer == customer)
        except cls.DoesNotExist:
            return cls(customer=customer)

    @property
    def users(self):
        """Returns the amount of users."""
        return User.select().where(User.customer == self.customer)

    @property
    def customer_quota(self):
        """Returns the customer quota."""
        return self.quota * self.users.count()

    @property
    def files(self):
        """Yields file records of the respective customer."""
        condition = User.customer == self.customer
        return UserFile.select().join(User).where(condition)

    @property
    def used(self):
        """Returns used space."""
        return sum(file.metadata.size for file in self.files.iterator())

    @property
    def free(self):
        """Returns free space for the respective customer."""
        return self.quota - self.used

    def alloc(self, size):
        """Tries to allocate the requested size in bytes."""
        if size > self.free:
            raise QuotaExceeded(quota=self.quota, free=self.free, size=size)

        return True

    def to_json(self, **kwargs):
        """Returns a JSON-ish dictionary."""
        json = super().to_json(**kwargs)
        json.update({'free': self.free, 'used': self.used})
        return json
