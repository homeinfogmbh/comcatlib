"""Content assigned to ComCat accounts."""

from peewee import ForeignKeyField, IntegerField

from cmslib.functions.charts import get_base_chart
from cmslib.functions.configuration import get_configuration
from cmslib.functions.menu import get_menu
from cmslib.orm.charts import ChartMode, BaseChart
from cmslib.orm.configuration import Configuration
from cmslib.orm.menu import Menu

from comcatlib.functions import get_user
from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ['UserBaseChart', 'UserConfiguration', 'UserMenu']


class UserContent(ComCatModel):
    """Common abstract content mapping."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')

    @classmethod
    def from_json(cls, json, **kwargs):
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
    def from_json(cls, json, **kwargs):
        """Creates a new user content mapping."""
        base_chart = json.pop('base_chart')
        record = super().from_json(json, **kwargs)
        record.base_chart = get_base_chart(base_chart)
        return record

    @property
    def chart(self):
        """Returns the respective chart."""
        return self.base_chart.chart

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {
            'id': self.id,
            'chart': self.chart.to_json(mode=ChartMode.BRIEF),
            'index': self.index
        }


class UserConfiguration(UserContent):
    """Association of a configuration with a user."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'user_configuration'

    configuration = ForeignKeyField(
        Configuration, column_name='configuration', on_delete='CASCADE')

    @classmethod
    def from_json(cls, json, **kwargs):
        """Creates a new user content mapping."""
        configuration = json.pop('configuration')
        record = super().from_json(json, **kwargs)
        record.configuration = get_configuration(configuration)
        return record

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {'id': self.id, 'configuration': self.configuration_id}


class UserMenu(UserContent):
    """Association of a menu with a user."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'user_menu'

    menu = ForeignKeyField(Menu, column_name='menu', on_delete='CASCADE')

    @classmethod
    def from_json(cls, json, **kwargs):
        """Creates a new user content mapping."""
        menu = json.pop('menu')
        record = super().from_json(json, **kwargs)
        record.menu = get_menu(menu)
        return record

    def to_json(self):
        """Returns a JSON-ish dict."""
        return {'id': self.id, 'menu': self.menu_id}
