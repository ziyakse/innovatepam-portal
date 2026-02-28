from fastapi import HTTPException, status

from src.services.auth_service import DuplicateUserError, InvalidCredentialsError


def map_auth_error(error: Exception) -> HTTPException:
    if isinstance(error, DuplicateUserError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
    if isinstance(error, InvalidCredentialsError):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request failed")
