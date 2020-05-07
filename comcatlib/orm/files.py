"""HISFS-like file associations and quotas."""

from peewee import BigIntegerField, CharField, ForeignKeyField

from filedb import File as FileDBFile
from hisfs import QuotaExceeded, get_sparse_file
from mdb import Customer

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['File', 'Quota']


DEFAULT_QUOTA = 10 * (1024 ** 2)    # 10 MiB.


class File(ComCatModel):
    """A user's file."""

    name = CharField(255)
    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    file = ForeignKeyField(FileDBFile, column_name='file')

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

    def to_json(self, *args, **kwargs):
        """Returns a JSON-ish dict."""
        json = super().to_json(*args, **kwargs)
        metadata = self.metadata.to_json(*args, **kwargs)
        json.update(metadata)
        return json


class Quota(ComCatModel):
    """Per-customer file quota."""

    customer = ForeignKeyField(
        Customer, column_name='quota', unique=True, on_delete='CASCADE',
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
    def customer_quota(self):
        """Returns the customer quota."""
        users = User.select().where(User.customer == self.customer).count()
        return self.quota * users

    @property
    def files(self):
        """Yields file records of the respective customer."""
        return File.select().where(File.user == self.user)

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
