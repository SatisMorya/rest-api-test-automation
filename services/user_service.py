"""Service layer: one method per Users API operation.

Keeps endpoint paths in a single place. If the API changes `/users`, only this
file changes; tests keep calling `user_service.get_user(...)`. It adds no
assertions, so tests still decide what is correct.
"""
from typing import Optional

import requests

from core.api_client import APIClient

USERS_ENDPOINT = "/users"


class UserService:
    def __init__(self, client: APIClient):
        self._client = client

    def list_users(self, params: Optional[dict] = None) -> requests.Response:
        return self._client.get(USERS_ENDPOINT, params=params)

    def get_user(self, user_id) -> requests.Response:
        return self._client.get(f"{USERS_ENDPOINT}/{user_id}")

    def create_user(self, payload: dict) -> requests.Response:
        return self._client.post(USERS_ENDPOINT, json=payload)

    def update_user(self, user_id, payload: dict) -> requests.Response:
        return self._client.put(f"{USERS_ENDPOINT}/{user_id}", json=payload)

    def delete_user(self, user_id) -> requests.Response:
        return self._client.delete(f"{USERS_ENDPOINT}/{user_id}")
