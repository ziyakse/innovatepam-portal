from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.models.auth_models import UserRecord
from src.services.auth_service import AuthService, UnauthorizedError

http_bearer = HTTPBearer(auto_error=False)


def require_access_token(credentials: HTTPAuthorizationCredentials | None) -> str:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return credentials.credentials


def get_current_user_or_401(access_token: str, service: AuthService) -> UserRecord:
    try:
        return service.get_current_user_from_access_token(access_token)
    except UnauthorizedError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        ) from exc
