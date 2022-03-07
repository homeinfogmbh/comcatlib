"""User registration."""

from __future__ import annotations
from datetime import datetime, timedelta
from typing import Union
from xml.etree.ElementTree import Element, SubElement

from peewee import CharField, DateTimeField, ForeignKeyField, Select

from mdb import Company, Customer, Tenement
from notificationlib import get_email_orm_model

from comcatlib.exceptions import AlreadyRegistered, DuplicateUser
from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User
from comcatlib.pwgen import genpw


__all__ = ['UserRegistration', 'RegistrationNotificationEmails']


class UserRegistration(ComCatModel):
    """A user registration."""

    class Meta:
        table_name = 'user_registration'

    name = CharField()
    email = CharField()
    tenant_id = CharField()
    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE'
    )
    registered = DateTimeField(default=datetime.now)

    @classmethod
    def select(cls, *args, cascade: bool = False) -> Select:
        """Selects user registrations."""
        if not cascade:
            return super().select(*args)

        return super().select(*{
            cls, Customer, Company, *args
        }).join(Customer).join(Company)

    @classmethod
    def from_json(cls, json: dict, customer: Customer, **kwargs):
        """Creates a record from a JSON-ish dict."""
        record = super().from_json(json, **kwargs)
        record.customer = customer
        return record

    @classmethod
    def same_ids_sel(cls, tenant_id: str, email: str) -> Select:
        """Returns a select condition to match records with the same IDs."""
        return (cls.tenant_id == tenant_id) | (cls.email == email)

    @classmethod
    def dupes_select(
            cls,
            tenant_id: str,
            email: str,
            customer: Union[Customer, int]
    ) -> Select:
        """Returns a select condition to match duplicates."""
        return cls.same_ids_sel(tenant_id, email) & (cls.customer == customer)

    @classmethod
    def add(cls, name: str, email: str, tenant_id: str,
            customer: Union[Customer, int]) -> UserRegistration:
        """Adds a new user registration."""
        condition = cls.dupes_select(tenant_id, email, customer)

        try:
            record = cls.select().where(condition).get()
        except cls.DoesNotExist:
            return cls(
                name=name, email=email, tenant_id=tenant_id, customer=customer
            )

        raise AlreadyRegistered(record)

    @classmethod
    def of_today(cls) -> Select:
        """Selects today's registrations."""
        now = datetime.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        return cls.select().where(
            (cls.registered >= today) & (cls.registered < tomorrow)
        )

    def confirm(self, tenement: Tenement):
        """Confirm the user registration."""
        if tenement.customer != self.customer:
            raise ValueError('Customers do not match.')

        passwd = genpw()
        user = User(
            name=self.name, email=self.email, tenement=tenement, passwd=passwd
        )
        self.delete_instance()

        if user.is_unique:
            return user, passwd

        raise DuplicateUser()

    def to_html(self) -> Element:
        """Returns a HTML element."""
        tr = Element('tr')
        td = SubElement(tr, 'td')
        td.text = self.name
        td = SubElement(tr, 'td')
        td.text = self.email
        td = SubElement(tr, 'td')
        td.text = self.tenant_id
        td = SubElement(tr, 'td')
        td.text = self.registered.isoformat()
        return tr


RegistrationNotificationEmails = get_email_orm_model(
    ComCatModel, table_name='registration_notification_emails'
)
