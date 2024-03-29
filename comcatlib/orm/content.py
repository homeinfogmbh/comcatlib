"""Content assigned to ComCat accounts."""

from __future__ import annotations
from typing import Union

from peewee import ForeignKeyField, IntegerField, Select

from cmslib import BaseChart, Chart, ChartMode, Configuration, Menu
from mdb import Address, Company, Customer, Tenement

from comcatlib.orm.common import ComCatModel
from comcatlib.orm.user import User


__all__ = ["UserBaseChart", "UserConfiguration", "UserMenu"]


class UserContent(ComCatModel):
    """Common abstract content mapping."""

    user = ForeignKeyField(
        User, column_name="user", on_delete="CASCADE", lazy_load=False
    )

    @classmethod
    def from_json(cls, json: dict, user: Union[User, int], **kwargs) -> UserContent:
        """Creates a new user content mapping."""
        record = super().from_json(json, **kwargs)
        record.user = user
        return record

    @classmethod
    def select(cls, *args, cascade: bool = False) -> Select:
        """Selects user content."""
        if not cascade:
            return super().select(*args)

        return (
            super()
            .select(*{cls, User, Tenement, Customer, Company, Address, *args})
            .join(User)
            .join(Tenement)
            .join(Customer)
            .join(Company)
            .join_from(Tenement, Address)
        )


class UserBaseChart(UserContent):
    """Association of a base chart with a user."""

    class Meta:
        table_name = "user_base_chart"

    base_chart = ForeignKeyField(
        BaseChart, column_name="base_chart", on_delete="CASCADE", lazy_load=False
    )
    index = IntegerField(default=0)

    @classmethod
    def from_json(
        cls,
        json: dict,
        user: Union[User, int],
        base_chart: Union[BaseChart, int],
        **kwargs,
    ) -> UserBaseChart:
        """Creates a new user <> base chart mapping."""
        record = super().from_json(json, user, **kwargs)
        record.base_chart = base_chart
        return record

    @classmethod
    def select(cls, *args, cascade: bool = False) -> Select:
        """Selects user base charts."""
        if not cascade:
            return super().select(*args)

        return (
            super()
            .select(*{cls, BaseChart, *args}, cascade=True)
            .join_from(cls, BaseChart)
        )

    @property
    def chart(self) -> Chart:
        """Returns the respective chart."""
        return self.base_chart.chart

    def to_json(self, *args, chart: bool = False, **kwargs) -> dict:
        """Returns a JSON-ish dict."""
        json = super().to_json(*args, **kwargs)

        if chart:
            json["chart"] = self.chart.to_json(mode=ChartMode.BRIEF)

        return json


class UserConfiguration(UserContent):
    """Association of a configuration with a user."""

    class Meta:
        table_name = "user_configuration"

    configuration = ForeignKeyField(
        Configuration, column_name="configuration", on_delete="CASCADE", lazy_load=False
    )

    @classmethod
    def from_json(
        cls,
        json: dict,
        user: Union[User, int],
        configuration: Union[Configuration, int],
        **kwargs,
    ) -> UserConfiguration:
        """Creates a new user <> configuration mapping."""
        record = super().from_json(json, user, **kwargs)
        record.configuration = configuration
        return record

    @classmethod
    def select(cls, *args, cascade: bool = False) -> Select:
        """Selects user configurations."""
        if not cascade:
            return super().select(*args)

        return (
            super()
            .select(*{cls, Configuration, *args}, cascade=True)
            .join_from(cls, Configuration)
        )

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        return {"id": self.id, "configuration": self.configuration_id}


class UserMenu(UserContent):
    """Association of a menu with a user."""

    class Meta:  # pylint: disable=C0111,R0903
        table_name = "user_menu"

    menu = ForeignKeyField(
        Menu, column_name="menu", on_delete="CASCADE", lazy_load=False
    )

    @classmethod
    def from_json(
        cls, json: dict, user: Union[User, int], menu: Union[Menu, int], **kwargs
    ) -> UserMenu:
        """Creates a new user <> menu mapping."""
        record = super().from_json(json, user, **kwargs)
        record.menu = menu
        return record

    @classmethod
    def select(cls, *args, cascade: bool = False) -> Select:
        """Selects user menus."""
        if not cascade:
            return super().select(*args)

        return super().select(*{cls, Menu, *args}, cascade=True).join_from(cls, Menu)

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        return {"id": self.id, "menu": self.menu_id}
