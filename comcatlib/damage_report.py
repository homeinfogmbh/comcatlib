"""Damage reports of accounts."""

from damage_report import DamageReport

from comcatlib.orm import AccountDamageReport


__all__ = ['list_', 'submit']


def list_(account):
    """Lists damage reports submitted by the respective account."""

    for damage_report in DamageReport.select().join(AccountDamageReport).where(
            AccountDamageReport.account == account.id):
        yield damage_report


def submit(json, account):
    """Submits a damage report."""

    damage_report = DamageReport.from_json(
        json, account.customer, account.address)
    damage_report.save()
    account_damage_report = AccountDamageReport(
        account=account.id, damage_report=damage_report)
    account_damage_report.save()
