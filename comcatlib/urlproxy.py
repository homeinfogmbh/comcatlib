"""Facebook image link proxy."""

from hashlib import sha256
from typing import Union
from urllib.parse import urlparse, ParseResult

from flask import request, Response
from requests import get


__all__ = ['decode_url', 'encode_url', 'proxy_url']


def decode_url(json: dict) -> str:
    """Returns the URL from a JSON-ish dict."""

    return ParseResult(
        scheme=json['scheme'], netloc=json['netloc'],
        path=json.get('path', ''), params=json.get('params', ''),
        query=json.get('query', ''), fragment=json.get('fragment', '')
    ).geturl()


def encode_url(url: str) -> dict:
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


def proxy_url(url: str) -> Union[Response, tuple[str, int]]:
    """Proxies the respective URL."""

    response = get(url)

    if response.status_code != 200:
        return 'Could not proxy URL.', 400

    sha256sum = sha256(response.content).hexdigest()

    if sha256sum == request.headers.get('sha256sum'):
        return 'Not Modified', 304

    headers = {'sha256sum': sha256sum}

    return Response(
        response.content, status=response.status_code, headers=headers,
        content_type=response.headers['Content-Type']
    )
