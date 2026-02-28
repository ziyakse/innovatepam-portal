from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field

from src.api.errors import map_auth_error
from src.auth.dependencies import get_current_user_or_401, http_bearer, require_access_token
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LogoutRequest(BaseModel):
    refresh_token: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest) -> dict[str, str]:
    try:
        user = auth_service.register(email=payload.email, password=payload.password)
        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
        }
    except Exception as exc:
        raise map_auth_error(exc) from exc


@router.post("/login", status_code=status.HTTP_200_OK)
def login(payload: LoginRequest) -> dict[str, object]:
    try:
        auth = auth_service.login(email=payload.email, password=payload.password)
        return {
            "access_token": auth.access_token,
            "refresh_token": auth.refresh_token,
            "token_type": "Bearer",
            "user": {
                "id": auth.user.id,
                "email": auth.user.email,
                "role": auth.user.role,
            },
        }
    except Exception as exc:
        raise map_auth_error(exc) from exc


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    payload: LogoutRequest,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(http_bearer)],
) -> Response:
    access_token = require_access_token(credentials)
    auth_service.logout(refresh_token=payload.refresh_token, access_token=access_token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", status_code=status.HTTP_200_OK)
def me(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(http_bearer)],
) -> dict[str, str]:
    access_token = require_access_token(credentials)
    user = get_current_user_or_401(access_token, auth_service)
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
    }
