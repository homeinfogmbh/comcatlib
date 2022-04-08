"""Image/text charts as news."""

from datetime import datetime, timedelta
from typing import Iterable, Iterator

from cmslib import Chart

from comcatlib.demo.common import DEMO_DATASET_ATTACHMENTS
from comcatlib.demo.common import LOGGER
from comcatlib.demo.common import randdate
from comcatlib.demo.hisfs import get_or_create_file
from comcatlib.demo.image_text import create_image_text_chart
from comcatlib.orm.user import User
from comcatlib.orm.content import UserBaseChart
from comcatlib.orm.menu import Menu, MenuBaseChart


__all__ = ['create_news', 'map_news']


IMAGE_DIR = DEMO_DATASET_ATTACHMENTS / 'news'


def create_news(news: list[dict]) -> Iterator[Chart]:
    """Yields image text charts."""

    for chart in news:
        image_text_chart = create_chart(chart)
        make_news(image_text_chart)
        yield image_text_chart


def map_news(charts: Iterable[Chart], user: User) -> None:
    """Maps the given charts to the given user."""

    for chart in charts:
        LOGGER.info(
            'Assigning chart "%s" to user %s', chart.base.title, user.email
        )
        user_base_chart = UserBaseChart(base_chart=chart.base, user=user)
        user_base_chart.save()


def create_chart(chart: dict) -> Chart:
    """Creates news charts."""

    with IMAGE_DIR.joinpath(filename := chart['image']).open('rb') as file:
        bytes_ = file.read()

    return create_image_text_chart(
        chart['title'],
        chart['text'],
        image=get_or_create_file(filename, bytes_),
        created=get_random_date()
    )


def make_news(chart: Chart) -> None:
    """Make the base chart a news chart."""

    menu_base_chart = MenuBaseChart(base_chart=chart.base, menu=Menu.NEWS)
    menu_base_chart.save()


def get_random_date() -> datetime:
    """Returns a random datetime within the last sixty days."""

    return randdate((now := datetime.now()) - timedelta(days=60), now)
