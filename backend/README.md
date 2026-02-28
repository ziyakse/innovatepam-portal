# US1 (MVP) - User Authentication

This folder contains the US1 scope: register (`/auth/register`), login (`/auth/login`), logout (`/auth/logout`), and profile (`/auth/me`).

## Setup

```bash
cd backend
uv venv
uv pip install -e '.[dev]'
```

## Run the Application

```bash
cd backend
uv run uvicorn src.api.app:app --reload --port 8000
```

## US1 Tests (TDD)

```bash
cd backend
uv run pytest -q tests/unit/security/test_passwords.py \
  tests/unit/security/test_tokens.py \
  tests/unit/services/test_auth_service.py \
  tests/integration/auth/test_auth_flow.py
```

## Quality Gate

```bash
cd backend
uv run mypy --strict src/
uv run pylint src/
```
