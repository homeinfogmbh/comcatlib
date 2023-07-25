"""Contact chart creation."""

from cmslib import ImageText

from comcatlib.demo.chart import create_image_text_chart
from comcatlib.demo.common import LOGGER
from comcatlib.orm.menu import Menu, MenuBaseChart


__all__ = ["create_contact"]


def create_contact(contact: dict) -> ImageText:
    """Creates a contact chart."""

    LOGGER.info("Adding contact chart: %s", title := contact["title"])
    chart = create_image_text_chart(title, contact["text"])
    menu_base_chart = MenuBaseChart(base_chart=chart.base, menu=Menu.CONTACT)
    menu_base_chart.save()
    return chart
