"""Common functions."""

from random import choices
from string import ascii_letters, digits
from urllib.parse import urlparse, ParseResult

from flask import request


__all__ = ['change_path_to', 'genpw']


def change_path_to(path: str) -> str:
    """Changes the path of the current URL."""

    url = urlparse(request.url)
    new_url = ParseResult(
        url.scheme, url.netloc, path, url.params, url.query, url.fragment)
    return new_url.geturl()


def genpw(*, pool: str = ascii_letters+digits, length: int = 32) -> str:
    """Generates a random password."""

    return ''.join(choices(pool, k=length))
