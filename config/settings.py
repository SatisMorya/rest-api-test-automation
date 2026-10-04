"""Central configuration. Values come from environment variables.

Secrets (the API token) are never hard-coded. Locally they can live in an
untracked .env file; in CI they come from GitHub Secrets.
"""
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from config.environments import DEFAULT_ENVIRONMENT, ENVIRONMENTS

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _load_dotenv(path: Path) -> None:
    """Load KEY=VALUE lines from a .env file without overriding real env vars."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@dataclass(frozen=True)
class Settings:
    environment: str
    base_url: str
    timeout: float
    max_response_time: float
    max_retries: int
    # repr=False keeps the token out of logs and tracebacks.
    token: Optional[str] = field(default=None, repr=False)


def get_settings() -> Settings:
    _load_dotenv(PROJECT_ROOT / ".env")

    environment = os.getenv("APP_ENV", DEFAULT_ENVIRONMENT).lower()
    if environment not in ENVIRONMENTS:
        raise ValueError(
            f"Unknown APP_ENV '{environment}'. Choose one of: {', '.join(ENVIRONMENTS)}"
        )

    base_url = os.getenv("API_BASE_URL") or ENVIRONMENTS[environment]["base_url"]
    return Settings(
        environment=environment,
        base_url=base_url.rstrip("/"),
        timeout=float(os.getenv("API_TIMEOUT", "10")),
        max_response_time=float(os.getenv("MAX_RESPONSE_TIME", "5")),
        max_retries=int(os.getenv("API_MAX_RETRIES", "2")),
        token=os.getenv("GOREST_TOKEN") or None,
    )
