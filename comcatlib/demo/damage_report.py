"""Demo damage report management."""

from typing import Iterable

from damage_report import DamageReport
from mdb import Customer

from comcatlib.orm.user import User
from comcatlib.orm.damage_report import UserDamageReport


__all__ = ['create_damage_reports', 'delete_damage_reports']


def create_damage_report(user: User, message: str, damage_type: str) -> None:
    """Creates a dummy damage report of the given user."""

    damage_report = DamageReport(
        customer=user.tenement.customer,
        address=user.tenement.address,
        message=message,
        name=user.name,
        damage_type=damage_type
    )
    damage_report.save()
    user_damage_report = UserDamageReport(
        user=user,
        damage_report=damage_report
    )
    user_damage_report.save()


def create_damage_reports(
        users: Iterable[User],
        damage_reports: Iterable[dict]
) -> None:
    """Creates user damage reports."""

    for user, damage_report in zip(users, damage_reports):
        create_damage_report(
            user,
            damage_report['message'],
            damage_report['type']
        )


def delete_damage_reports(customer: Customer) -> None:
    """Deletes all damage reports of the given customer."""

    for damage_report in DamageReport.select().where(
            DamageReport.customer == customer
    ):
        damage_report.delete_instance()
