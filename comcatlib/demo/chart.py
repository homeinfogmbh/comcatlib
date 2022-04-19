"""Image text chart handling."""

from datetime import datetime
from typing import Iterable, Optional

from cmslib import BaseChart, Chart, ImageText, ImageTextImage, ImageTextText
from filedb import File
from mdb import Customer

from comcatlib.demo.common import DEMO_CUSTOMER_ID, LOGGER
from comcatlib.orm.user import User
from comcatlib.orm.content import UserBaseChart


__all__ = ['create_image_text_chart', 'delete_image_text_charts', 'map_charts']


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
        type=ImageText.__name__,
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


def map_charts(charts: Iterable[Chart], user: User) -> None:
    """Maps the given charts to the given user."""

    for chart in charts:
        LOGGER.info(
            'Assigning chart "%s" to user %s', chart.base.title, user.email
        )
        user_base_chart = UserBaseChart(base_chart=chart.base, user=user)
        user_base_chart.save()
