"""Assertions about response content: JSON, fields, types, validation errors, time."""
from typing import Any, Iterable

import requests


def _payload(source: Any) -> Any:
    """Accept either a Response or already-parsed JSON data."""
    if isinstance(source, requests.Response):
        return assert_json_response(source)
    return source


def assert_json_response(response: requests.Response) -> Any:
    """Assert the body is valid JSON and return it."""
    content_type = response.headers.get("Content-Type", "")
    assert "json" in content_type.lower(), (
        f"Expected a JSON Content-Type but got '{content_type}'"
    )
    try:
        return response.json()
    except ValueError as exc:
        raise AssertionError(f"Response body is not valid JSON: {response.text[:200]}") from exc


def assert_required_fields(source: Any, fields: Iterable[str]) -> None:
    data = _payload(source)
    assert isinstance(data, dict), f"Expected a JSON object but got {type(data).__name__}"
    missing = [name for name in fields if name not in data]
    assert not missing, f"Missing required fields: {missing}. Present: {sorted(data)}"


def assert_field_types(source: Any, expected_types: dict) -> None:
    data = _payload(source)
    for name, expected in expected_types.items():
        assert name in data, f"Field '{name}' is missing"
        value = data[name]
        # bool is a subclass of int in Python, so reject it explicitly for ints.
        is_bool_as_int = expected is int and isinstance(value, bool)
        assert isinstance(value, expected) and not is_bool_as_int, (
            f"Field '{name}' expected {expected.__name__} but got {type(value).__name__}"
        )


def assert_validation_error(source: Any, field: str) -> None:
    """GoRest reports validation failures as [{"field": ..., "message": ...}]."""
    errors = _payload(source)
    assert isinstance(errors, list) and errors, f"Expected a list of errors, got: {errors}"
    fields = [item.get("field") for item in errors if isinstance(item, dict)]
    assert field in fields, f"Expected a validation error for '{field}', got errors for {fields}"


def assert_response_time(response: requests.Response, max_seconds: float) -> None:
    elapsed = response.elapsed.total_seconds()
    assert elapsed <= max_seconds, (
        f"Response took {elapsed:.2f}s, limit is {max_seconds:.2f}s"
    )
