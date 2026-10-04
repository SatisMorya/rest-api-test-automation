"""HTTP communication layer.

Responsibility: build the request, send it, log it, return the raw response.
It deliberately contains NO test assertions. A 404 is a failure in one test and
the expected result in another, so only the test may decide what is correct.
"""
from typing import Any, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from utils.logger import get_logger

logger = get_logger()


class APIClientError(Exception):
    """Base class for communication problems (not for HTTP error statuses)."""


class APIConnectionError(APIClientError):
    """The server could not be reached."""


class APITimeoutError(APIClientError):
    """The server did not answer within the timeout."""


RETRY_STATUSES = (429, 502, 503, 504)


class APIClient:
    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        timeout: float = 10.0,
        max_retries: int = 0,
        retry_backoff: float = 1.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        if max_retries:
            # Retry only on "try again later" statuses (rate limit / gateway).
            # Connection errors and timeouts are NOT retried, so they stay visible.
            retry = Retry(
                total=max_retries,
                connect=0,
                read=0,
                status=max_retries,
                backoff_factor=retry_backoff,
                status_forcelist=RETRY_STATUSES,
                allowed_methods=None,
                respect_retry_after_header=True,
                raise_on_status=False,
            )
            self._session.mount("https://", HTTPAdapter(max_retries=retry))
            self._session.mount("http://", HTTPAdapter(max_retries=retry))
        self._session.headers.update(
            {"Accept": "application/json", "Content-Type": "application/json"}
        )
        if token:
            # Set on the session only; headers are never written to the log.
            self._session.headers["Authorization"] = f"Bearer {token}"

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[dict] = None,
        json: Optional[Any] = None,
        headers: Optional[dict] = None,
        timeout: Optional[float] = None,
    ) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        method = method.upper()
        try:
            response = self._session.request(
                method,
                url,
                params=params,
                json=json,
                headers=headers,
                timeout=timeout or self.timeout,
            )
        except requests.exceptions.Timeout as exc:
            logger.error("%s %s -> TIMEOUT", method, endpoint)
            raise APITimeoutError(f"{method} {endpoint} timed out") from exc
        except requests.exceptions.ConnectionError as exc:
            logger.error("%s %s -> CONNECTION ERROR", method, endpoint)
            raise APIConnectionError(f"Cannot connect to {self.base_url}") from exc
        except requests.exceptions.RequestException as exc:
            logger.error("%s %s -> REQUEST ERROR: %s", method, endpoint, type(exc).__name__)
            raise APIClientError(f"{method} {endpoint} failed: {exc}") from exc

        logger.info(
            "%s %s -> %s (%.0f ms)",
            method,
            endpoint,
            response.status_code,
            response.elapsed.total_seconds() * 1000,
        )
        return response

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("DELETE", endpoint, **kwargs)

    def close(self) -> None:
        self._session.close()
