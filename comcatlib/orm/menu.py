"""ComCat menu tagging."""

from enum import Enum

from flask import request
from peewee import ForeignKeyField

from cmslib.functions.charts import get_chart
from cmslib.orm.charts import BaseChart
from peeweeplus import EnumField

from comcatlib.orm.common import ComCatModel


__all__ = ['Menu', 'BaseChartMenu']


class Menu(Enum):
    """Available menus."""

    IMPRINT = 'imprint'
    EMERGENCY = 'emergency'
    HOUSE_INFO = 'house info'
    NEWS = 'news'


class BaseChartMenu(ComCatModel):
    """Many-to-many mapping of charts an menus."""

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'base_chart_menu'

    base_chart = ForeignKeyField(
        BaseChart, column_name='base_chart', on_delete='CASCADE')
    menu = EnumField(Menu)

    @classmethod
    def from_json(cls, *args, **kwargs):
        """Creates a new record from a JSON-ish dict."""
        base_chart_id = request.json.pop('chart')
        record = super().from_json(*args, **kwargs)
        record.base_chart = get_chart(base_chart_id).base_id
        return record
