"""Registration related functions."""

from collections import defaultdict
from pathlib import Path
from typing import Iterable, Iterator
from xml.etree.ElementTree import Element, SubElement

from emaillib import EMail
from mdb import Customer
from notificationlib import get_email_func

from comcatlib.email import SENDER, get_mailer
from comcatlib.orm.registration import UserRegistration
from comcatlib.orm.registration import RegistrationNotificationEmails


__all__ = ['notify_customer', 'notify_user']


NOTIFICATION_SUBJECT = 'Neue Benutzerregistrierungen für Ihre App'
USER_REG_SUBJECT = 'Mieter-App'
USER_REG_TEMP = Path('/usr/local/etc/comcat.d/userreg.temp')
RegistrationMap = dict[Customer, list[UserRegistration]]


def to_html(user_registrations: Iterable[UserRegistration]) -> Element:
    """Converts user registrations into an HTML element."""

    html = Element('html')
    body = SubElement(html, 'body')
    h1 = SubElement(body, 'h1')
    h1.text = 'Neue Registrierungen'
    p = SubElement(body, 'p')
    p.text = 'Folgende Benutzer haben sich für die App registriert:'
    SubElement(body, 'br')
    table = SubElement(body, 'table', attrs={'border': '1'})

    for user_registration in user_registrations:
        table.append(user_registration.to_html())

    p = SubElement(body, 'p')
    p.text = 'Mit freundlichen Grüßen'
    SubElement(body, 'br')
    p = SubElement(body, 'p')
    p.text = 'Ihre HOMEINFO GmbH'
    return html


def to_emails(customer: Customer,
              user_registrations: Iterable[UserRegistration]
              ) -> Iterator[EMail]:
    """Converts a user registration records into an email and deletes them."""

    if not user_registrations:
        return

    for notification_email in RegistrationNotificationEmails.select().where(
            Customer == customer):
        yield EMail(NOTIFICATION_SUBJECT, SENDER, notification_email.email,
                    html=to_html(user_registrations))


def get_user_registrations_by_customer() -> RegistrationMap:
    """Returns a dict of customer -> UserRegistration."""

    result = defaultdict(list)

    for user_registration in UserRegistration.of_today():
        result[user_registration.customer].append(user_registration)

    return result


def get_emails() -> Iterator[EMail]:
    """Yields emails to send."""

    user_registrations_by_customer = get_user_registrations_by_customer()

    for customer, user_registrations in user_registrations_by_customer.items():
        yield from to_emails(customer, user_registrations)


def make_user_registration_email(email: str, login: int, passwd: str) -> EMail:
    """Creates a user registration email."""

    with USER_REG_TEMP.open(encoding='utf-8') as file:
        template = file.read()

    text = template.format(name=login, passwd=passwd)
    return EMail(USER_REG_SUBJECT, SENDER, email, plain=text)


def notify_user(user_registration: UserRegistration, passwd: str) -> None:
    """Sends a notification email to the registered email address."""

    email = make_user_registration_email(
        user_registration.email, user_registration.id, passwd)
    get_mailer().send([email])


notify_customer = get_email_func(get_emails)
