from src.services.auth_service import AuthService


def test_should_register_user_when_valid_input_given() -> None:
    service = AuthService()

    user = service.register(email="user1@example.com", password="SecretPass123!")

    assert user.email == "user1@example.com"
    assert user.role == "submitter"


def test_should_login_user_when_valid_credentials_given() -> None:
    service = AuthService()
    service.register(email="user2@example.com", password="SecretPass123!")

    auth = service.login(email="user2@example.com", password="SecretPass123!")

    assert auth.access_token
    assert auth.refresh_token
    assert auth.user.email == "user2@example.com"


def test_should_logout_user_when_valid_refresh_token_given() -> None:
    service = AuthService()
    service.register(email="user3@example.com", password="SecretPass123!")
    auth = service.login(email="user3@example.com", password="SecretPass123!")

    service.logout(auth.refresh_token)

    assert service.is_refresh_token_revoked(auth.refresh_token) is True
