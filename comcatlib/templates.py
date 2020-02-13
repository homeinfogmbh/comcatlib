"""Jinja2 template rendering."""

from jinja2 import FileSystemLoader, Environment


__all__ = ['render_template']


TEMPLATE_LOADER = FileSystemLoader(searchpath='/usr/local/share/comcatlib/')
TEMPLATE_ENV = Environment(loader=TEMPLATE_LOADER)


def render_template(template, *args, **kwargs):
    """Renders the respective template."""

    return TEMPLATE_ENV.get_template(template).render(*args, **kwargs)
