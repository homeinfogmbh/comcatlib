"""Demo data manager."""

from json import load

from mdb import Customer, Tenement

from comcatlib.demo.common import DEMO_CUSTOMER_ID, DEMO_DATASET_FILE
from comcatlib.demo.damage_report import create_damage_reports
from comcatlib.demo.damage_report import delete_damage_reports
from comcatlib.demo.marketplace import create_offers, delete_offers
from comcatlib.demo.tenentforum import create_topics, delete_topics
from comcatlib.demo.users import create_users, delete_users


__all__ = ['main']


def create_demo_data(dataset: dict) -> None:
    """Creates demo data."""

    tenement = Tenement.get(Tenement.customer == DEMO_CUSTOMER_ID)
    users = list(create_users(dataset['users'], tenement))
    create_damage_reports(users, dataset['damage_reports'])
    create_topics(users, dataset['forum'])
    create_offers(users, dataset['offers'])


def delete_demo_data() -> None:
    """Deletes the demo data."""

    customer = Customer[DEMO_CUSTOMER_ID]
    delete_damage_reports(customer)
    delete_offers(customer)
    delete_topics(customer)
    delete_users(customer)


def main() -> None:
    """Re-generates the demo data."""

    delete_demo_data()

    with DEMO_DATASET_FILE.open('rb') as file:
        dataset = load(file)

    create_demo_data(dataset)
