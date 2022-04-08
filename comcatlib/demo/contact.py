"""Contact chart creation."""

from cmslib import Chart

from comcatlib.demo.image_text import create_image_text_chart
from comcatlib.orm.menu import Menu, MenuBaseChart


__all__ = ['create_contact']


def create_contact(contact: dict) -> None:
    """Creates a contact chart."""

    chart = create_image_text_chart(contact['title'], contact['text'])
    make_contact(chart)


def make_contact(chart: Chart) -> None:
    """Make the chart a contact chart."""

    menu_base_chart = MenuBaseChart(base_chart=chart.base, menu=Menu.CONTACT)
    menu_base_chart.save()
