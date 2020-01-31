"""Damage reports of accounts."""

from damage_report import DamageReport

from comcatlib.orm import UserDamageReport


__all__ = ['list_', 'submit']


def list_(user):
    """Lists damage reports submitted by the respective user."""

    for damage_report in DamageReport.select().join(AccountDamageReport).where(
            AccountDamageReport.user == user.id):
        yield damage_report


def submit(json, user):
    """Submits a damage report."""

    damage_report = DamageReport.from_json(json, user.customer, user.address)
    damage_report.save()
    user_damage_report = UserDamageReport(
        user=user.id, damage_report=damage_report)
    user_damage_report.save()
