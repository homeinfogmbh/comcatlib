"""Demo user management."""

from typing import Iterator

from mdb import Customer, Tenement

from comcatlib.orm.user import User
from comcatlib.pwgen import genpw


__all__ = ['create_users', 'delete_users']


def create_user(email: str, name: str, tenement: Tenement) -> User:
    """Creates a user account and returns its ID."""

    user = User(email=email, name=name, tenement=tenement, passwd=genpw())
    user.save()
    return user


def create_users(users: list[dict], tenement: Tenement) -> Iterator[User]:
    """Creates user accounts and yields their IDs."""

    for user in users:
        yield create_user(user['email'], user['name'], tenement=tenement)


def delete_users(customer: Customer) -> None:
    """Creates user accounts and yields their IDs."""

    for user in User.select().join(Tenement).where(
            Tenement.Customer == customer
    ):
        user.delete_instance()
