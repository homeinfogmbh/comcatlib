"""HISFS-like file associations and quotas."""

from __future__ import annotations
from datetime import datetime
from typing import Generator, Iterable

from peewee import BigIntegerField, CharField, ForeignKeyField, ModelSelect

from filedb import File
from mdb import Address, Company, Customer, Tenement

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
    user = ForeignKeyField(
        User, column_name='user', on_delete='CASCADE', lazy_load=False)
    file = ForeignKeyField(File, column_name='file', lazy_load=False)

    @classmethod
    def add(cls, user: User, bytes_: bytes, name: str = None) -> UserFile:
        """Adds the respective file."""
        file = cls(name=name, user=user)
        file.file = File.from_bytes(bytes_, save=True)
        file.save()
        return file

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects user files."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, User, Tenement, Customer, Company, Address, File, *args}
        return super().select(*args, **kwargs).join(User).join(Tenement).join(
            Customer).join(Company).join_from(Tenement, Address).join_from(
            cls, File)

    @property
    def bytes(self):
        """Returns the file's bytes."""
        return self.file.bytes

    @property
    def mimetype(self) -> str:
        """Returns the MIME type."""
        return self.filedb_file.mimetype

    @property
    def sha256sum(self) -> str:
        """Returns the SHA-256 checksum."""
        return self.filedb_file.sha256sum

    @property
    def size(self) -> int:
        """Returns the file size."""
        return self.filedb_file.size

    @property
    def created(self) -> datetime:
        """Returns the create datetime."""
        return self.filedb_file.created

    @property
    def last_access(self) -> datetime:
        """Returns the last access datetime."""
        return self.filedb_file.last_access

    @property
    def accessed(self) -> int:
        """Returns the access count."""
        return self.filedb_file.accessed

    def stream(self) -> Generator[bytes, None, None]:
        """Returns HTTP stream."""
        return self.file.stream()

    def save(self, *args, **kwargs) -> int:
        """Saves the filedb.File first."""
        if self.file:
            self.file.save(*args, **kwargs)

        return super().save(*args, **kwargs)

    def to_json(self, **_) -> dict:
        """Returns a JSON-ish dict."""
        return {
            'id': self.id,
            'mimetype': self.mimetype,
            'sha256sum': self.sha256sum,
            'size': self.size,
            'created': self.created,
            'lastAccess': self.last_access,
            'accessed': self.accessed
        }


class Quota(ComCatModel):
    """Per-customer file quota."""

    customer = ForeignKeyField(
        Customer, column_name='customer', unique=True, on_delete='CASCADE',
        on_update='CASCADE', lazy_load=False)
    quota = BigIntegerField(default=DEFAULT_QUOTA)  # Per-user quota in bytes.

    @classmethod
    def for_customer(cls, customer: Customer) -> Quota:
        """Returns the quota for the respective customer."""
        try:
            return cls.select(cascade=True).where(
                cls.customer == customer).get()
        except cls.DoesNotExist:
            return cls(customer=customer)

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects customer file quotas."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, Customer, Company, *args}
        return super().select(*args, **kwargs).join(Customer).join(Company)

    @property
    def users(self) -> ModelSelect:
        """Returns the amount of users."""
        return User.select(cascade=True).where(Tenement.customer == self.customer)

    @property
    def customer_quota(self) -> int:
        """Returns the customer quota."""
        return self.quota * self.users.count()

    @property
    def files(self) -> Iterable[UserFile]:
        """Yields file records of the respective customer."""
        return UserFile.select(cascade=True).where(
            Tenement.customer == self.customer)

    @property
    def used(self) -> int:
        """Returns used space."""
        return sum(file.size for file in self.files.iterator())

    @property
    def free(self) -> int:
        """Returns free space for the respective customer."""
        return self.quota - self.used

    def alloc(self, size: int) -> bool:
        """Tries to allocate the requested size in bytes."""
        if size > self.free:
            raise QuotaExceeded(quota=self.quota, free=self.free, size=size)

        return True

    def to_json(self, **kwargs) -> dict:
        """Returns a JSON-ish dictionary."""
        json = super().to_json(**kwargs)
        json.update({'free': self.free, 'used': self.used})
        return json
