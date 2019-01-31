"""Facebook image link proxy."""

from urllib.parse import urlparse, ParseResult

from flask import Response
from requests import get


__all__ = ['decode_url', 'encode_url', 'proxy_url']


def decode_url(json):
    """Returns the URL from a JSON-ish dict."""

    parse_result = ParseResult(
        scheme=json['scheme'], netloc=json['netloc'],
        path=json.get('path', ''), params=json.get('params', ''),
        query=json.get('query', ''), fragment=json('fragment', ''))
    return parse_result.geturl()


def encode_url(url):
    """Encodes a URL into a JSON object."""

    parse_result = urlparse(url)
    return {
        'scheme': parse_result.scheme,
        'netloc': parse_result.netloc,
        'path': parse_result.path,
        'params': parse_result.params,
        'query': parse_result.query,
        'fragment': parse_result.fragment}


def proxy_url(url):
    """Proxies the respective URL."""

    response = get(url)

    if response.status_code != 200:
        return ('Could not get Facebook image.', 400)

    return Response(
        response.content, status=response.status_code,
        content_type=response.headers['Content-Type'])
