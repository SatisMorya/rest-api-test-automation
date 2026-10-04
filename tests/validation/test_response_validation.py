"""Response validation tests: TC-013 to TC-014."""
from http import HTTPStatus

import pytest

from assertions.response_assertions import (
    assert_field_types,
    assert_json_response,
    assert_required_fields,
    assert_response_time,
)
from assertions.schema_assertions import assert_matches_schema
from assertions.status_assertions import assert_status_code
from utils.data_loader import load_test_data

pytestmark = [pytest.mark.get, pytest.mark.regression]
CHECKS = load_test_data()["status_and_time_checks"]
TYPE_MAP = {"int": int, "str": str}


@pytest.mark.parametrize("check", CHECKS, ids=[c["case_id"] for c in CHECKS])
def test_tc013_status_code_and_response_time(api_client, settings, check):
    response = api_client.get(check["endpoint"])

    assert_status_code(response, check["expected_status"])
    assert_response_time(response, settings.max_response_time)


def test_tc014_response_fields_and_data_types(user_service, test_data):
    list_response = user_service.list_users()  # public data, no token needed
    assert_status_code(list_response, HTTPStatus.OK)
    first_user = assert_json_response(list_response)[0]

    response = user_service.get_user(first_user["id"])

    assert_status_code(response, HTTPStatus.OK)
    user = assert_json_response(response)
    assert_required_fields(user, test_data["user_field_types"])
    assert_field_types(user, {k: TYPE_MAP[v] for k, v in test_data["user_field_types"].items()})
    assert "@" in user["email"], "email should contain '@'"
    assert_matches_schema(user)
