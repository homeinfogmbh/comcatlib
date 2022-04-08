"""Demo user management."""

from typing import Iterator

from mdb import Customer, Tenement

from comcatlib.demo.common import DEMO_USER_EMAIL
from comcatlib.demo.common import DEMO_USER_NAME
from comcatlib.demo.common import DEMO_USER_PASSWD
from comcatlib.orm.user import User
from comcatlib.pwgen import genpw


__all__ = ['create_demo_user', 'create_users', 'delete_users']


def create_demo_user(tenement) -> None:
    """Creates the demo user."""

    user = User(
        email=DEMO_USER_EMAIL,
        name=DEMO_USER_NAME,
        tenement=tenement,
        passwd=DEMO_USER_PASSWD
    )
    user.save()


def create_users(users: dict[str, str], tenement: Tenement) -> Iterator[User]:
    """Creates user accounts and yields their IDs."""

    for email, name in users.items():
        yield create_user(email, name, tenement=tenement)


def delete_users(customer: Customer) -> None:
    """Creates user accounts and yields their IDs."""

    for user in User.select().join(Tenement).where(
            Tenement.Customer == customer
    ):
        user.delete_instance()


def create_user(email: str, name: str, tenement: Tenement) -> User:
    """Creates a user account and returns its ID."""

    user = User(email=email, name=name, tenement=tenement, passwd=genpw())
    user.save()
    return user
