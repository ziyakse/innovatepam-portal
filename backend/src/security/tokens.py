from __future__ import annotations

from typing import Any
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from jose import jwt

JWT_SECRET = "dev-secret-change-me"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 30
REFRESH_TOKEN_DAYS = 7


def _now() -> datetime:
    return datetime.now(timezone.utc)


def create_access_token(user_id: str, role: str) -> str:
    issued_at = _now()
    payload = {
        "sub": user_id,
        "role": role,
        "type": "access",
        "jti": str(uuid4()),
        "iat": int(issued_at.timestamp()),
        "exp": int((issued_at + timedelta(minutes=ACCESS_TOKEN_MINUTES)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    issued_at = _now()
    payload = {
        "sub": user_id,
        "type": "refresh",
        "jti": str(uuid4()),
        "iat": int(issued_at.timestamp()),
        "exp": int((issued_at + timedelta(days=REFRESH_TOKEN_DAYS)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
