from src.security.passwords import hash_password, verify_password


def test_should_hash_password_when_plain_text_given() -> None:
    plain = "SecretPass123!"

    hashed = hash_password(plain)

    assert hashed != plain
    assert hashed.startswith("$2")


def test_should_verify_password_when_valid_hash_given() -> None:
    plain = "SecretPass123!"
    hashed = hash_password(plain)

    valid = verify_password(plain, hashed)

    assert valid is True


def test_should_reject_password_when_hash_does_not_match() -> None:
    hashed = hash_password("SecretPass123!")

    valid = verify_password("WrongPassword", hashed)

    assert valid is False
