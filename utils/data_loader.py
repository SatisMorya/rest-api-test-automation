"""Reusable helpers that keep test data and schemas out of test code."""
import json
from typing import Any

from config.settings import PROJECT_ROOT


def load_json(relative_path: str) -> Any:
    with open(PROJECT_ROOT / relative_path, encoding="utf-8") as file:
        return json.load(file)


def load_test_data() -> dict:
    return load_json("test_data/test_data.json")


def load_payload(name: str) -> Any:
    return load_json(f"test_data/payloads/{name}.json")


def load_schema(name: str) -> dict:
    return load_json(f"schemas/{name}")
