"""Status-code assertions with failure messages that show the response body."""
from typing import Iterable

import requests


def _body_snippet(response: requests.Response, limit: int = 300) -> str:
    return response.text[:limit] if response.text else "<empty body>"


def assert_status_code(response: requests.Response, expected: int) -> None:
    assert response.status_code == expected, (
        f"Expected status {expected} but got {response.status_code}. "
        f"Body: {_body_snippet(response)}"
    )


def assert_status_in(response: requests.Response, allowed: Iterable[int]) -> None:
    allowed = list(allowed)
    assert response.status_code in allowed, (
        f"Expected status in {allowed} but got {response.status_code}. "
        f"Body: {_body_snippet(response)}"
    )
