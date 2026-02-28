from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from src.models.auth_models import UserRecord
from src.security.passwords import hash_password, verify_password
from src.security.tokens import create_access_token, create_refresh_token, decode_token


class AuthError(Exception):
    pass


class DuplicateUserError(AuthError):
    pass


class InvalidCredentialsError(AuthError):
    pass


class UnauthorizedError(AuthError):
    pass


@dataclass
class AuthResult:
    access_token: str
    refresh_token: str
    user: UserRecord


class AuthService:
    def __init__(self) -> None:
        self._users_by_email: dict[str, UserRecord] = {}
        self._users_by_id: dict[str, UserRecord] = {}
        self._revoked_refresh_tokens: set[str] = set()
        self._revoked_access_tokens: set[str] = set()

    def register(self, email: str, password: str) -> UserRecord:
        normalized_email = email.strip().lower()
        if normalized_email in self._users_by_email:
            raise DuplicateUserError("User already exists")

        user = UserRecord(
            id=str(uuid4()),
            email=normalized_email,
            password_hash=hash_password(password),
            role="submitter",
        )
        self._users_by_email[normalized_email] = user
        self._users_by_id[user.id] = user
        return user

    def login(self, email: str, password: str) -> AuthResult:
        normalized_email = email.strip().lower()
        user = self._users_by_email.get(normalized_email)
        if user is None:
            raise InvalidCredentialsError("Invalid credentials")

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid credentials")

        access_token = create_access_token(user_id=user.id, role=user.role)
        refresh_token = create_refresh_token(user_id=user.id)
        return AuthResult(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user,
        )

    def logout(self, refresh_token: str, access_token: str | None = None) -> None:
        if refresh_token:
            self._revoked_refresh_tokens.add(refresh_token)
        if access_token:
            self._revoked_access_tokens.add(access_token)

    def is_refresh_token_revoked(self, refresh_token: str) -> bool:
        return refresh_token in self._revoked_refresh_tokens

    def is_access_token_revoked(self, access_token: str) -> bool:
        return access_token in self._revoked_access_tokens

    def get_current_user_from_access_token(self, access_token: str) -> UserRecord:
        if self.is_access_token_revoked(access_token):
            raise UnauthorizedError("Token revoked")

        claims = decode_token(access_token)
        if claims.get("type") != "access":
            raise UnauthorizedError("Invalid token type")

        user_id_claim = claims.get("sub")
        if not isinstance(user_id_claim, str):
            raise UnauthorizedError("Invalid token subject")

        user_id = user_id_claim
        user = self._users_by_id.get(user_id)
        if user is None:
            raise UnauthorizedError("User not found")
        return user
