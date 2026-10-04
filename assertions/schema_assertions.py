"""JSON Schema validation (jsonschema library)."""
from typing import Any

from jsonschema import Draft7Validator

from utils.data_loader import load_schema


def assert_matches_schema(data: Any, schema_name: str = "user_schema.json") -> None:
    validator = Draft7Validator(load_schema(schema_name))
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    assert not errors, "Schema validation failed: " + "; ".join(
        f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors
    )
