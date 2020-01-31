"""Facebook image link proxy."""

from hashlib import sha256
from urllib.parse import urlparse, ParseResult

from flask import request, Response
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
        'fragment': parse_result.fragment
    }


def proxy_url(url):
    """Proxies the respective URL."""

    response = get(url)

    if response.status_code != 200:
        return ('Could not get Facebook image.', 400)

    sha256sum = sha256(response.content).hexdigest()

    if sha256sum == request.headers.get('sha256sum'):
        return ('Not Modified', 304)

    headers = {'sha256sum': sha256sum}

    return Response(
        response.content, status=response.status_code, headers=headers,
        content_type=response.headers['Content-Type'])
