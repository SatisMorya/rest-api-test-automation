"""User model and payload builder.

Useful here because GoRest requires a unique email on every create, so tests
need a single place that produces valid, unique payloads.
"""
import uuid
from dataclasses import asdict, dataclass
from typing import Optional

from utils.data_loader import load_payload, load_test_data


def unique_email() -> str:
    domain = load_test_data()["email_domain"]
    return f"qa.{uuid.uuid4().hex[:12]}@{domain}"


@dataclass
class User:
    name: str
    email: str
    gender: str
    status: str
    id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(**{k: data[k] for k in ("name", "email", "gender", "status")},
                   id=data.get("id"))

    @classmethod
    def build(cls, **overrides) -> "User":
        """A valid user from test_data/payloads/valid_user.json with a unique email."""
        values = {**load_payload("valid_user"), "email": unique_email(), **overrides}
        return cls(**values)

    def to_payload(self) -> dict:
        payload = asdict(self)
        payload.pop("id")
        return payload
