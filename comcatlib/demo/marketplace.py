"""Dummy marketplace offers management."""

from pathlib import Path
from typing import Sequence

from filedb import File
from marketplace import Offer, Image
from mdb import Customer, Tenement

from comcatlib.demo.common import DEMO_DATASET_ATTACHMENTS, LOGGER, randzipfill
from comcatlib.orm.user import User


__all__ = ['create_offers', 'delete_offers']


def create_offers(users: Sequence[User], offers: Sequence[dict]) -> None:
    """Creates the respective offers."""

    for index, (user, offer) in enumerate(randzipfill(users, offers)):
        create_offer(
            user,
            offer['title'],
            offer['description'],
            offer['price'],
            index
        )


def delete_offers(customer: Customer) -> None:
    """Deletes all offers of the given customer."""

    for offer in Offer.select().join(User).join(Tenement).where(
            Tenement.customer == customer
    ):
        LOGGER.info('Deleting offer: "%s"', offer.title)
        offer.delete_instance()


def create_offer(
        user: User,
        title: str,
        description: str,
        price: int,
        index: int
) -> None:
    """Creates a marketplace offer."""

    LOGGER.info('Creating offer: "%s" for user %s', title, user.email)
    offer = Offer(
        user=user,
        title=title,
        description=description,
        email=user.email,
        price=price
    )
    offer.save()

    for idx, image in enumerate(DEMO_DATASET_ATTACHMENTS.glob(f'{index}-*')):
        create_image(offer, image, idx)


def create_image(offer: Offer, image: Path, index: int) -> None:
    """Creates an image attachment."""

    with image.open('rb') as file:
        file = File.from_bytes(file.read(), save=True)

    LOGGER.info(
        'Adding image "%s" with index %i to offer %i', image, index, offer.id
    )
    image = Image(offer=offer, file=file, index=index)
    image.save()
