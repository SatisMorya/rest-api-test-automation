"""GET tests: TC-001 to TC-004."""
from http import HTTPStatus

import pytest

from assertions.response_assertions import assert_json_response, assert_required_fields
from assertions.schema_assertions import assert_matches_schema
from assertions.status_assertions import assert_status_code
from utils.data_loader import load_test_data

pytestmark = [pytest.mark.get, pytest.mark.regression]
INVALID_IDS = load_test_data()["invalid_ids"]
USER_FIELDS = load_test_data()["required_fields"] + ["id"]


@pytest.mark.smoke
def test_tc001_get_all_users(user_service):
    response = user_service.list_users()

    assert_status_code(response, HTTPStatus.OK)
    users = assert_json_response(response)
    assert isinstance(users, list), "Expected a JSON array of users"
    assert users, "Expected at least one user"


@pytest.mark.smoke
def test_tc002_get_user_by_valid_id(user_service, created_user):
    response = user_service.get_user(created_user["id"])

    assert_status_code(response, HTTPStatus.OK)
    user = assert_json_response(response)
    assert user["id"] == created_user["id"]
    assert user["email"] == created_user["email"]


@pytest.mark.parametrize("case", INVALID_IDS, ids=[c["case_id"] for c in INVALID_IDS])
def test_tc003_get_user_by_invalid_id(user_service, case):
    response = user_service.get_user(case["id"])

    assert_status_code(response, HTTPStatus.NOT_FOUND)


def test_tc004_get_users_response_structure(user_service):
    response = user_service.list_users()

    assert_status_code(response, HTTPStatus.OK)
    users = assert_json_response(response)
    assert users, "Expected at least one user to validate"
    for user in users:
        assert_required_fields(user, USER_FIELDS)
        assert_matches_schema(user)
