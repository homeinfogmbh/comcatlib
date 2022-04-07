"""Dummy marketplace offers management."""

from typing import Iterable

from marketplace import Offer
from mdb import Customer, Tenement

from comcatlib.orm.user import User


__all__ = ['create_offers', 'delete_offers']


def create_offer(user: User, title: str, description: str, price: int) -> None:
    """Creates a marketplace offer."""

    offer = Offer(user=user, title=title, description=description, price=price)
    offer.save()


def create_offers(users: Iterable[User], offers: Iterable[dict]) -> None:
    """Creates the respective offers."""

    for user, offer in zip(users, offers):
        create_offer(
            user,
            offer['title'],
            offer['description'],
            offer['price']
        )


def delete_offers(customer: Customer) -> None:
    """Deletes all offers of the given customer."""

    for offer in Offer.select().join(User).join(Tenement).where(
            Tenement.customer == customer
    ):
        offer.delete_instance()
