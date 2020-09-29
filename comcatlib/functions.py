"""Common functions."""

from random import choices
from string import ascii_letters, digits
from urllib.parse import urlparse, ParseResult

from flask import request

from mdb import Tenement


__all__ = ['change_path_to', 'get_tenement']


def change_path_to(path):
    """Changes the path of the current URL."""

    url = urlparse(request.url)
    new_url = ParseResult(
        url.scheme, url.netloc, path, url.params, url.query, url.fragment)
    return new_url.geturl()


def genpw(*, pool=ascii_letters+digits, length=32):
    """Generates a random password."""

    return ''.join(choices(pool, k=length))


def get_tenement(ident, customer):
    """Returns a tenement by its ID and customer."""

    condition = Tenement.id == ident
    condition &= Tenement.customer == customer
    return Tenement.get(condition)
