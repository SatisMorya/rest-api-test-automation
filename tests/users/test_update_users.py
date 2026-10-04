"""PUT tests: TC-008 to TC-010."""
from http import HTTPStatus

import pytest

from assertions.response_assertions import assert_json_response, assert_validation_error
from assertions.status_assertions import assert_status_code
from models.user_model import User
from utils.data_loader import load_payload, load_test_data

pytestmark = [pytest.mark.put, pytest.mark.regression]
TEST_DATA = load_test_data()
BOUNDARY_CASES = load_payload("boundary_user")


def _full_payload(user: dict, **overrides) -> dict:
    """PUT replaces the whole record, so send every field."""
    return {**User.from_dict(user).to_payload(), **overrides}


@pytest.mark.smoke
def test_tc008_update_existing_user(user_service, created_user):
    new_values = TEST_DATA["update_values"]

    response = user_service.update_user(
        created_user["id"], _full_payload(created_user, **new_values)
    )

    assert_status_code(response, HTTPStatus.OK)
    updated = assert_json_response(response)
    for field, value in new_values.items():
        assert updated[field] == value
    # Confirm the change was really persisted, not just echoed.
    stored_response = user_service.get_user(created_user["id"])
    assert_status_code(stored_response, HTTPStatus.OK)
    stored = stored_response.json()
    for field, value in new_values.items():
        assert stored[field] == value, f"'{field}' was not persisted"


def test_tc009_update_non_existing_user(user_service):
    payload = User.build().to_payload()

    response = user_service.update_user(TEST_DATA["non_existing_user_id"], payload)

    assert_status_code(response, HTTPStatus.NOT_FOUND)


@pytest.mark.parametrize("case", BOUNDARY_CASES, ids=[c["case_id"] for c in BOUNDARY_CASES])
def test_tc010_update_user_with_boundary_or_invalid_data(user_service, created_user, case):
    response = user_service.update_user(
        created_user["id"], _full_payload(created_user, **case["overrides"])
    )

    assert_status_code(response, case["expected_status"])
    if case["expected_field"]:
        assert_validation_error(response, case["expected_field"])
