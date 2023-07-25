"""Image/text charts as news."""

from typing import Iterator

from cmslib import Chart

from comcatlib.demo.chart import create_image_text_chart
from comcatlib.demo.common import DEMO_DATASET_ATTACHMENTS
from comcatlib.demo.common import LOGGER
from comcatlib.demo.common import get_random_date
from comcatlib.demo.hisfs import get_or_create_file
from comcatlib.orm.menu import Menu, MenuBaseChart


__all__ = ["create_news"]


IMAGE_DIR = DEMO_DATASET_ATTACHMENTS / "news"


def create_news(news: list[dict]) -> Iterator[Chart]:
    """Yields image text charts."""

    for chart in news:
        chart = create_chart(chart)
        make_news(chart)
        yield chart


def create_chart(chart: dict) -> Chart:
    """Creates news charts."""

    with IMAGE_DIR.joinpath(filename := chart["image"]).open("rb") as file:
        bytes_ = file.read()

    LOGGER.info("Adding news chart: %s", title := chart["title"])
    return create_image_text_chart(
        title,
        chart["text"],
        image=get_or_create_file(filename, bytes_),
        created=get_random_date(),
    )


def make_news(chart: Chart) -> None:
    """Make the chart a news chart."""

    menu_base_chart = MenuBaseChart(base_chart=chart.base, menu=Menu.NEWS)
    menu_base_chart.save()
