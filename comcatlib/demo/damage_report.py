"""Demo damage report management."""

from datetime import datetime
from typing import Sequence

from damage_report import DamageReport
from mdb import Customer

from comcatlib.demo.common import randzipfill
from comcatlib.orm.user import User
from comcatlib.orm.damage_report import UserDamageReport


__all__ = ['create_damage_reports', 'delete_damage_reports']


def create_damage_report(
        user: User,
        message: str,
        damage_type: str,
        timestamp: datetime
) -> None:
    """Creates a dummy damage report of the given user."""

    damage_report = DamageReport(
        customer=user.tenement.customer,
        address=user.tenement.address,
        message=message,
        name=user.name,
        damage_type=damage_type,
        timestamp=timestamp
    )
    damage_report.save()
    user_damage_report = UserDamageReport(
        user=user,
        damage_report=damage_report
    )
    user_damage_report.save()


def create_damage_reports(
        users: Sequence[User],
        damage_reports: Sequence[dict]
) -> None:
    """Creates user damage reports."""

    for user, damage_report in randzipfill(users, damage_reports):
        create_damage_report(
            user,
            damage_report['message'],
            damage_report['type'],
            datetime.fromisoformat(damage_report['timestamp']),
        )


def delete_damage_reports(customer: Customer) -> None:
    """Deletes all damage reports of the given customer."""

    for damage_report in DamageReport.select().where(
            DamageReport.customer == customer
    ):
        damage_report.delete_instance()
