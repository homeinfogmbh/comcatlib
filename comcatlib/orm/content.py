"""Content assigned to ComCat accounts."""

from __future__ import annotations

from peewee import ForeignKeyField, IntegerField

from cmslib.functions.charts import Chart, get_chart
from cmslib.functions.configuration import get_configuration
from cmslib.functions.menu import get_menu
from cmslib.orm.charts import ChartMode, BaseChart
from cmslib.orm.configuration import Configuration
from cmslib.orm.menu import Menu

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import get_user, User


__all__ = ['UserBaseChart', 'UserConfiguration', 'UserMenu']


class UserContent(ComCatModel):     # pylint: disable=R0903
    """Common abstract content mapping."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')

    @classmethod
    def from_json(cls, json: dict, **kwargs) -> UserContent:
        """Creates a new user content mapping."""
        user = json.pop('user')
        record = super().from_json(json, **kwargs)
        record.user = get_user(user)
        return record


class UserBaseChart(UserContent):
    """Association of a base chart with a user."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'user_base_chart'

    base_chart = ForeignKeyField(
        BaseChart, column_name='base_chart', on_delete='CASCADE')
    index = IntegerField(default=0)

    @classmethod
    def from_json(cls, json: dict, **kwargs) -> UserBaseChart:
        """Creates a new user content mapping."""
        chart_id = json.pop('chart')
        record = super().from_json(json, **kwargs)
        record.base_chart = get_chart(chart_id).base
        return record

    @property
    def chart(self) -> Chart:
        """Returns the respective chart."""
        return self.base_chart.chart

    def to_json(self, *args, chart: bool = False, **kwargs) -> dict:
        """Returns a JSON-ish dict."""
        json = super().to_json(*args, **kwargs)

        if chart:
            json['chart'] = self.chart.to_json(mode=ChartMode.BRIEF)

        return json


class UserConfiguration(UserContent):
    """Association of a configuration with a user."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'user_configuration'

    configuration = ForeignKeyField(
        Configuration, column_name='configuration', on_delete='CASCADE')

    @classmethod
    def from_json(cls, json: dict, **kwargs) -> UserConfiguration:
        """Creates a new user content mapping."""
        configuration = json.pop('configuration')
        record = super().from_json(json, **kwargs)
        record.configuration = get_configuration(configuration)
        return record

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        return {'id': self.id, 'configuration': self.configuration_id}


class UserMenu(UserContent):
    """Association of a menu with a user."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'user_menu'

    menu = ForeignKeyField(Menu, column_name='menu', on_delete='CASCADE')

    @classmethod
    def from_json(cls, json: dict, **kwargs) -> UserMenu:
        """Creates a new user content mapping."""
        menu = json.pop('menu')
        record = super().from_json(json, **kwargs)
        record.menu = get_menu(menu)
        return record

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        return {'id': self.id, 'menu': self.menu_id}
