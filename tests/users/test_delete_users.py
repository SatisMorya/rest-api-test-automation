"""DELETE tests: TC-011 to TC-012."""
from http import HTTPStatus

import pytest

from assertions.status_assertions import assert_status_code
from utils.data_loader import load_test_data

pytestmark = [pytest.mark.delete, pytest.mark.regression]


@pytest.mark.smoke
def test_tc011_delete_existing_user(user_service, created_user):
    response = user_service.delete_user(created_user["id"])

    assert_status_code(response, HTTPStatus.NO_CONTENT)
    assert not response.content, "A 204 response must have an empty body"
    # The user must really be gone.
    assert_status_code(user_service.get_user(created_user["id"]), HTTPStatus.NOT_FOUND)


def test_tc012_delete_non_existing_user(user_service):
    response = user_service.delete_user(load_test_data()["non_existing_user_id"])

    assert_status_code(response, HTTPStatus.NOT_FOUND)
