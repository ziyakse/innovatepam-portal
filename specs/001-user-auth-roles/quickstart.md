# Quickstart: User Management Feature

## 1) Prerequisites
- Python 3.12+
- Node.js 20+
- PostgreSQL 15+
- `uv` installed

## 2) Backend bootstrap
```bash
cd backend
uv venv
source .venv/bin/activate
uv pip install fastapi uvicorn sqlalchemy alembic psycopg[binary] python-jose passlib[bcrypt] pydantic
uv pip install pytest pytest-mock pytest-cov mypy pylint mutmut playwright
```

## 3) Frontend bootstrap
```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

## 4) Database setup
```bash
createdb innovatepam_portal
# configure DATABASE_URL in backend environment settings
cd backend
alembic upgrade head
```

## 5) TDD workflow per user story
1. Write failing unit/integration test for story slice.
2. Implement minimal code to pass.
3. Refactor without changing behavior.
4. Repeat for next acceptance scenario.

## 6) Run quality gates
```bash
# backend
cd backend
mypy src/
pylint src/
pytest
pytest tests/unit
pytest tests/integration
pytest tests/e2e
pytest --cov=src
mutmut run
```

## 7) Manual smoke checks
1. Register submitter account.
2. Login and verify authenticated profile via `/auth/me`.
3. Logout and confirm protected routes return 401.
4. Login as evaluator/admin and verify `/admin/evaluations` returns 200.
5. Verify submitter receives 403 on `/admin/evaluations`.
