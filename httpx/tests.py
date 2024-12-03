import httpx
import pytest
from pytest_httpx import HTTPXMock

from tools import get_json, post_json


def test_get_json(httpx_mock: HTTPXMock):
    url = "https://jsonplaceholder.typicode.com/todos/1"
    json = {"id": 1, "title": "Test title"}
    httpx_mock.add_response(
        method="GET",
        url=url,
        json=json,
    )
    response = get_json(url)
    assert response == json


def test_post_json(httpx_mock: HTTPXMock):
    url = "https://jsonplaceholder.typicode.com/todos/1"
    json = {"success": True}
    httpx_mock.add_response(
        method="POST",
        url="https://httpbin.org/post",
        json=json
    )
    response = post_json(url, json)
    assert response == json


def test_get_json_request_error(httpx_mock: HTTPXMock):
    url = "https://jsonplaceholder.typicode.com/todos/1"
    httpx_mock.add_exception(
        method='GET',
        url=url,
        exception=httpx.RequestError('Request Error')
    )
    with pytest.raises(httpx.RequestError):
        get_json(url)


def test_post_json_request_error(httpx_mock: HTTPXMock):
    url = "https://jsonplaceholder.typicode.com/todos/1"
    json = {"success": True}
    httpx_mock.add_exception(
        method='POST',
        url=url,
        exception=httpx.RequestError('Request Error')
    )
    with pytest.raises(httpx.RequestError):
        post_json(url, json)
