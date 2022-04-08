"""Documents chart creation."""

from comcatlib.demo.image_text import create_image_text_chart
from comcatlib.orm.menu import Menu, MenuBaseChart


__all__ = ['create_documents_chart']


def create_documents_chart(service: dict) -> None:
    """Creates a documents chart."""

    chart = create_image_text_chart(service['title'], service['text'])
    menu_base_chart = MenuBaseChart(base_chart=chart.base, menu=Menu.DOCUMENTS)
    menu_base_chart.save()
