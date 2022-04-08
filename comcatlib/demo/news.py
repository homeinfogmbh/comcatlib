"""Image/text charts as news."""

from typing import Iterable, Iterator

from cmslib import BaseChart, ImageText, ImageTextImage, ImageTextText
from hisfs import FileExists, File
from mdb import Customer

from comcatlib.demo.common import DEMO_CUSTOMER_ID
from comcatlib.demo.common import DEMO_DATASET_ATTACHMENTS
from comcatlib.demo.common import LOGGER
from comcatlib.orm.user import User
from comcatlib.orm.content import UserBaseChart


__all__ = ['create_news', 'delete_news', 'map_news']


IMAGE_DIR = DEMO_DATASET_ATTACHMENTS / 'news'


def create_news(news: list[dict]) -> Iterator[BaseChart]:
    """Yields image text charts."""

    for chart in news:
        yield create_chart(chart)


def delete_news(customer: Customer) -> None:
    """Deletes the news."""

    for image_text_chart in ImageText.select().join(BaseChart).where(
            BaseChart.customer == customer
    ):
        image_text_chart.delete_instance()


def map_news(base_charts: Iterable[BaseChart], user: User) -> None:
    """Maps the given charts to the given user."""

    for base_chart in base_charts:
        LOGGER.info(
            'Assigning chart "%s" to user %s', base_chart.title, user.email
        )
        user_base_chart = UserBaseChart(base_chart=base_chart, user=user)
        user_base_chart.save()


def create_chart(chart: dict) -> BaseChart:
    """Creates news charts."""

    LOGGER.info('Creating news chart "%s"', title := chart['title'])
    base = BaseChart(customer=DEMO_CUSTOMER_ID, title=title)
    base.save()
    image_text = ImageText(base=base, title=title)
    image_text.save()
    text = ImageTextText(text=chart['text'])
    text.save()

    with IMAGE_DIR.joinpath(filename := chart['image']).open('rb') as file:
        bytes_ = file.read()

    image = ImageTextImage(file=get_or_create_file(filename, bytes_))
    image.save()
    return base


def get_or_create_file(
        name: str,
        bytes_: bytes,
        *,
        customer: int = DEMO_CUSTOMER_ID
) -> File:
    """Creates or re-uses the given file."""

    LOGGER.info('Adding file: %s', name)

    try:
        file = File.add(name, customer, bytes_)
    except FileExists:
        return File.get((File.name == name) & (File.customer == customer))

    file.file.save()
    file.save()
    return file
