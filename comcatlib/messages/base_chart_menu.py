"""Messages regarding BaseChartMenus."""

from wsgilib import JSONMessage


__all__ = [
    'BASE_CHART_MENU_ADDED',
    'BASE_CHART_MENU_DELETED',
    'NO_SUCH_BASE_CHART_MENU'
]


BASE_CHART_MENU_ADDED = JSONMessage('Base chart menu added.', 201)
BASE_CHART_MENU_DELETED = JSONMessage('Base chart menu deleted.', 200)
NO_SUCH_BASE_CHART_MENU = JSONMessage('No such base chart menu.', 404)
