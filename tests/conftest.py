"""Shared fixtures. Kept small on purpose: client, service, data, cleanup."""
from http import HTTPStatus

import pytest

from assertions.status_assertions import assert_status_code
from config.settings import get_settings
from core.api_client import APIClient, APIClientError
from models.user_model import User
from services.user_service import UserService
from utils.data_loader import load_test_data
from utils.logger import get_logger, set_current_test

logger = get_logger()
WRITE_MARKERS = {"post", "put", "delete"}


def pytest_collection_modifyitems(config, items):
    """Write operations need a token; skip them with a clear reason if missing."""
    if get_settings().token:
        return
    skip = pytest.mark.skip(reason="GOREST_TOKEN is not set (required for write requests)")
    for item in items:
        if WRITE_MARKERS & {mark.name for mark in item.iter_markers()}:
            item.add_marker(skip)


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest.fixture(scope="session")
def api_client(settings):
    client = APIClient(
        settings.base_url,
        token=settings.token,
        timeout=settings.timeout,
        max_retries=settings.max_retries,
    )
    yield client
    client.close()


@pytest.fixture(scope="session")
def user_service(api_client):
    return UserService(api_client)


@pytest.fixture(scope="session")
def test_data():
    return load_test_data()


@pytest.fixture(autouse=True)
def _log_test_name(request):
    set_current_test(request.node.name)
    yield
    set_current_test("-")


@pytest.fixture
def user_cleanup(user_service):
    """Collect created user IDs and delete them after the test (best effort)."""
    created_ids = []
    yield created_ids
    for user_id in created_ids:
        try:
            response = user_service.delete_user(user_id)
            logger.info("Cleanup of user %s -> %s", user_id, response.status_code)
        except APIClientError as exc:
            logger.warning("Cleanup of user %s failed: %s", user_id, exc)


@pytest.fixture
def created_user(user_service, settings, user_cleanup):
    """A real user created through the API; removed again after the test."""
    if not settings.token:
        pytest.skip("GOREST_TOKEN is not set (required to create a user)")
    response = user_service.create_user(User.build().to_payload())
    assert_status_code(response, HTTPStatus.CREATED)
    data = response.json()
    user_cleanup.append(data["id"])
    return data
