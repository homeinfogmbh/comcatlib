"""Image text chart handling."""

from datetime import datetime
from typing import Optional

from cmslib import BaseChart, ImageText, ImageTextImage, ImageTextText
from filedb import File
from mdb import Customer

from comcatlib.demo.common import DEMO_CUSTOMER_ID, LOGGER


__all__ = ['create_image_text_chart', 'delete_image_text_charts']


def create_image_text_chart(
        title: str,
        text: str,
        *,
        created: Optional[datetime] = None,
        image: Optional[File] = None,
        customer: int = DEMO_CUSTOMER_ID
) -> ImageText:
    """Creates news charts."""

    LOGGER.info('Creating news chart "%s"', title)
    base = BaseChart(
        customer=customer,
        created=created or datetime.now(),
        title=title
    )
    base.save()
    image_text = ImageText(base=base, title=title)
    image_text.save()
    text = ImageTextText(chart=image_text, text=text)
    text.save()

    if image is not None:
        image = ImageTextImage(
            chart=image_text,
            file=image
        )
        image.save()

    return image_text


def delete_image_text_charts(customer: Customer) -> None:
    """Deletes the customer's image text charts."""

    for image_text_chart in ImageText.select(cascade=True).where(
            BaseChart.customer == customer
    ):
        image_text_chart.delete_instance()
