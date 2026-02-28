from fastapi.testclient import TestClient

from src.api.app import app


def test_should_register_login_logout_and_reject_after_logout() -> None:
    client = TestClient(app)

    register = client.post(
        "/auth/register",
        json={"email": "flowuser@example.com", "password": "SecretPass123!"},
    )
    assert register.status_code == 201

    login = client.post(
        "/auth/login",
        json={"email": "flowuser@example.com", "password": "SecretPass123!"},
    )
    assert login.status_code == 200
    access_token = login.json()["access_token"]
    refresh_token = login.json()["refresh_token"]

    me_ok = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_ok.status_code == 200

    logout = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"refresh_token": refresh_token},
    )
    assert logout.status_code == 204

    me_after = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_after.status_code == 401
