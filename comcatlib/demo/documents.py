"""Documents chart creation."""

from cmslib import ImageText, ImageTextImage
from comcatlib.demo.common import DEMO_DATASET_ATTACHMENTS
from comcatlib.demo.hisfs import get_or_create_file
from comcatlib.demo.image_text import create_image_text_chart
from comcatlib.orm.menu import Menu, MenuBaseChart


__all__ = ['create_documents_chart']


IMAGES_DIR = DEMO_DATASET_ATTACHMENTS / 'documents'


def create_documents_chart(documents: dict) -> None:
    """Creates a documents chart."""

    chart = create_image_text_chart(documents['title'], documents['text'])
    menu_base_chart = MenuBaseChart(base_chart=chart.base, menu=Menu.DOCUMENTS)
    menu_base_chart.save()

    for file in documents['files']:
        add_attachment(chart, file)


def add_attachment(image_text_chart: ImageText, filename: str) -> None:
    """Adds a file to an image / text chart."""

    with IMAGES_DIR.joinpath(filename).open('rb') as file:
        file = get_or_create_file(filename, file.read())

    image = ImageTextImage(chart=image_text_chart, file=file)
    image.save()
    