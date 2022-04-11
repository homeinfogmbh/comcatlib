"""Service chart creation."""

from comcatlib.demo.common import LOGGER
from comcatlib.demo.image_text import create_image_text_chart
from comcatlib.orm.menu import Menu, MenuBaseChart


__all__ = ['create_service_chart']


def create_service_chart(service: dict) -> None:
    """Creates a service chart."""

    LOGGER.info('Adding service chart: %s', title := service['title'])
    chart = create_image_text_chart(title, service['text'])
    menu_base_chart = MenuBaseChart(
        base_chart=chart.base,
        menu=Menu.SERVICE_NUMBERS
    )
    menu_base_chart.save()
