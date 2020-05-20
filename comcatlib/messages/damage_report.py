"""Damage report-related messages."""

from wsgilib import JSONMessage


__all__ = ['DAMAGE_REPORT_SUBMITTED', 'NO_SUCH_DAMAGE_REPORT']


DAMAGE_REPORT_SUBMITTED = JSONMessage('Damage report submitted.', status=201)
NO_SUCH_DAMAGE_REPORT = JSONMessage('No such damage report.', status=404)
