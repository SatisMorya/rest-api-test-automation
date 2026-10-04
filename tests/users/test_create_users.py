"""POST tests: TC-005 to TC-007."""
from http import HTTPStatus

import pytest

from assertions.response_assertions import (
    assert_field_types,
    assert_json_response,
    assert_required_fields,
    assert_validation_error,
)
from assertions.status_assertions import assert_status_code
from models.user_model import User
from utils.data_loader import load_payload, load_test_data

pytestmark = [pytest.mark.post, pytest.mark.regression]
REQUIRED_FIELDS = load_test_data()["required_fields"]
INVALID_CASES = load_payload("invalid_user")


@pytest.mark.smoke
def test_tc005_create_user_with_valid_data(user_service, user_cleanup):
    payload = User.build().to_payload()

    response = user_service.create_user(payload)
    if response.status_code == HTTPStatus.CREATED:
        user_cleanup.append(response.json()["id"])  # clean up even if asserts fail

    assert_status_code(response, HTTPStatus.CREATED)
    user = assert_json_response(response)
    assert_required_fields(user, REQUIRED_FIELDS + ["id"])
    assert_field_types(user, {"id": int})
    for field in REQUIRED_FIELDS:
        assert user[field] == payload[field], f"'{field}' was not stored as sent"


@pytest.mark.parametrize("missing_field", REQUIRED_FIELDS)
def test_tc006_create_user_with_missing_required_field(user_service, missing_field):
    payload = User.build().to_payload()
    payload.pop(missing_field)

    response = user_service.create_user(payload)

    assert_status_code(response, HTTPStatus.UNPROCESSABLE_ENTITY)
    assert_validation_error(response, missing_field)


@pytest.mark.parametrize("case", INVALID_CASES, ids=[c["case_id"] for c in INVALID_CASES])
def test_tc007_create_user_with_invalid_data(user_service, request, case):
    payload = User.build().to_payload()
    if case.get("reuse_existing_email"):
        # Only this case needs a pre-existing user, so create it lazily.
        payload["email"] = request.getfixturevalue("created_user")["email"]
    payload.update(case["overrides"])

    response = user_service.create_user(payload)

    assert_status_code(response, HTTPStatus.UNPROCESSABLE_ENTITY)
    assert_validation_error(response, case["expected_field"])
