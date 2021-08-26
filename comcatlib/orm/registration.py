"""User registration."""

from __future__ import annotations
from datetime import datetime, timedelta
from typing import Union
from xml.etree.ElementTree import Element, SubElement

from peewee import CharField, DateTimeField, ForeignKeyField, ModelSelect

from mdb import Customer, Tenement
from notificationlib import get_email_orm_model

from comcatlib.exceptions import AlreadyRegistered, DuplicateUser
from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User
from comcatlib.pwgen import genpw


__all__ = ['UserRegistration', 'RegistrationNotificationEmails']


class UserRegistration(ComCatModel):    # pylint: disable=R0903
    """A user registration."""

    class Meta:     # pylint: disable=R0903,C0115
        table_name = 'user_registration'

    name = CharField(255)
    email = CharField(255)
    tenant_id = CharField(255)
    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE')
    registered = DateTimeField(default=datetime.now)

    @classmethod
    def from_json(cls, json: dict, customer: Customer, **kwargs):
        """Creates a record froma JSON-ish dict."""
        record = super().from_json(json, **kwargs)
        record.customer = customer
        return record

    @classmethod
    def same_ids_sel(cls, tenant_id: str, email: str) -> ModelSelect:
        """Returns a select condition to match records with the same IDs."""
        return (cls.tenant_id == tenant_id) | (cls.email == email)

    @classmethod
    def dupes_select(cls, tenant_id: str, email: str,
                     customer: Union[Customer, int]) -> ModelSelect:
        """Returns a select condition to match duplicales."""
        return cls.same_ids_sel(tenant_id, email) & (cls.customer == customer)

    @classmethod
    def add(cls, name: str, email: str, tenant_id: str,
            customer: Union[Customer, int]) -> UserRegistration:
        """Adds a new user registration."""
        condition = cls.dupes_select(tenant_id, email, customer)

        try:
            record = cls.select().where(condition).get()
        except cls.DoesNotExist:
            return cls(name=name, email=email, tenant_id=tenant_id,
                       customer=customer)

        raise AlreadyRegistered(record)

    @classmethod
    def of_today(cls) -> ModelSelect:
        """Selects today's registrations."""
        now = datetime.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        return cls.select().where(
            (cls.registered >= today) & (cls.registered < tomorrow))

    def confirm(self, tenement: Tenement):
        """Confirm the user registration."""
        passwd = genpw()
        user = User(tenement=tenement, passwd=passwd)
        self.delete_instance()

        if user.is_unique:
            return (user, passwd)

        raise DuplicateUser()

    def to_html(self) -> Element:
        """Returns a HTML element."""
        tr = Element('tr')  # pylint: disable=C0103
        td = SubElement(tr, 'td')   # pylint: disable=C0103
        td.text = self.name
        td = SubElement(tr, 'td')   # pylint: disable=C0103
        td.text = self.email
        td = SubElement(tr, 'td')   # pylint: disable=C0103
        td.text = self.tenant_id
        td = SubElement(tr, 'td')   # pylint: disable=C0103
        td.text = self.registered.isoformat()
        return tr

    def notify(self, passwd: str) -> bool:
        """Sends a notification email to the registered email address."""

        raise NotImplementedError('Notification not implemented.')


RegistrationNotificationEmails = get_email_orm_model(
    ComCatModel, table_name='registration_notification_emails')
