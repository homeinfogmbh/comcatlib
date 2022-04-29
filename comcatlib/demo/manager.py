"""Demo data manager."""

from json import load
from logging import INFO, basicConfig

from mdb import Customer

from comcatlib.demo.common import DEMO_CUSTOMER_ID
from comcatlib.demo.common import DEMO_DATASET_FILE
from comcatlib.demo.common import DEMO_USER_ADDRESS
from comcatlib.demo.common import LOG_FORMAT
from comcatlib.demo.common import LOGGER
from comcatlib.demo.contact import create_contact
from comcatlib.demo.damage_report import create_damage_reports
from comcatlib.demo.damage_report import delete_damage_reports
from comcatlib.demo.documents import create_documents_chart
from comcatlib.demo.hisfs import remove_files
from comcatlib.demo.chart import delete_image_text_charts, map_charts
from comcatlib.demo.marketplace import create_offers, delete_offers
from comcatlib.demo.news import create_news
from comcatlib.demo.service import create_service_chart
from comcatlib.demo.tenantcalendar import create_events, delete_events
from comcatlib.demo.tenement import create_tenement, delete_tenements
from comcatlib.demo.tenantforum import create_topics, delete_topics
from comcatlib.demo.users import create_demo_user, create_users, delete_users


__all__ = ['main']


def create_demo_data(dataset: dict) -> None:
    """Creates demo data."""

    tenement = create_tenement(DEMO_CUSTOMER_ID, *DEMO_USER_ADDRESS)
    LOGGER.info('Using tenement: %s (%i)', tenement.address, tenement.id)
    users = list(create_users(dataset['users'], tenement))
    contact_chart = create_contact(dataset['contact'])
    create_damage_reports(users, dataset['damage_reports'])
    documents_chart = create_documents_chart(dataset['documents'])
    news_charts = list(create_news(dataset['news']))
    create_offers(users, dataset['marketplace'])
    service_chart = create_service_chart(dataset['service'])
    create_events(users, dataset['calendar'])
    create_topics(users, dataset['forum'])
    demo_user = create_demo_user(tenement)
    map_charts(
        [contact_chart, documents_chart, service_chart, *news_charts],
        demo_user
    )


def delete_demo_data() -> None:
    """Deletes the demo data."""

    customer = Customer[DEMO_CUSTOMER_ID]
    delete_damage_reports(customer)
    delete_image_text_charts(customer)
    delete_offers(customer)
    delete_events(customer)
    delete_topics(customer)
    delete_users(customer)
    remove_files(customer)
    delete_tenements(customer)


def main() -> None:
    """Re-generates the demo data."""

    basicConfig(level=INFO, format=LOG_FORMAT)
    delete_demo_data()

    with DEMO_DATASET_FILE.open('rb') as file:
        dataset = load(file)

    create_demo_data(dataset)
