"""Demo user management."""

from typing import Iterator

from mdb import Customer, Tenement

from comcatlib.demo.common import DEMO_USER_EMAIL
from comcatlib.demo.common import DEMO_USER_NAME
from comcatlib.demo.common import DEMO_USER_PASSWD
from comcatlib.demo.common import LOGGER
from comcatlib.orm.user import User
from comcatlib.pwgen import genpw


__all__ = ["create_demo_user", "create_users", "delete_users"]


def create_demo_user(tenement) -> User:
    """Creates the demo user."""

    LOGGER.info("Creating demo user")
    user = User(
        email=DEMO_USER_EMAIL,
        name=DEMO_USER_NAME,
        tenement=tenement,
        passwd=DEMO_USER_PASSWD,
    )
    user.save()
    return user


def create_users(users: dict[str, str], tenement: Tenement) -> Iterator[User]:
    """Creates user accounts and yields their IDs."""

    for email, name in users.items():
        yield create_user(email, name, tenement=tenement)


def delete_users(customer: Customer) -> None:
    """Creates user accounts and yields their IDs."""

    for user in User.select().join(Tenement).where(Tenement.customer == customer):
        LOGGER.info('Deleting user "%s"', user.email)
        user.delete_instance()


def create_user(email: str, name: str, tenement: Tenement) -> User:
    """Creates a user account and returns its ID."""

    LOGGER.info('Creating user "%s"', email)
    user = User(email=email, name=name, tenement=tenement, passwd=genpw())
    user.save()
    return user
