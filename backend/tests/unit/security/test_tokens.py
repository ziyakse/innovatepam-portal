from src.security.tokens import create_access_token, create_refresh_token, decode_token


def test_should_create_access_token_with_expected_claims() -> None:
    token = create_access_token(user_id="user-1", role="submitter")

    claims = decode_token(token)

    assert claims["sub"] == "user-1"
    assert claims["role"] == "submitter"
    assert claims["type"] == "access"


def test_should_create_refresh_token_with_expected_claims() -> None:
    token = create_refresh_token(user_id="user-1")

    claims = decode_token(token)

    assert claims["sub"] == "user-1"
    assert claims["type"] == "refresh"
