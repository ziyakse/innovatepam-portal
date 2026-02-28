# Implementation Plan: InnovatEPAM Portal - User Management

**Branch**: `001-user-auth-roles` | **Date**: 2026-02-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-user-auth-roles/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Deliver secure user management for InnovatEPAM Portal with registration, login, logout, and role distinction (submitter vs evaluator/admin). Implementation uses a Python FastAPI backend with PostgreSQL for persistence, JWT-based stateless auth, and a React + Tailwind frontend for auth flows and role-aware UI access; testing remains TDD-first with pytest/mypy/pylint, targeted Playwright E2E, and coverage/mutation gates from constitution.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.12 (backend), TypeScript 5.x (frontend)  
**Primary Dependencies**: FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, python-jose, passlib[bcrypt], React 18, Vite, Tailwind CSS  
**Storage**: PostgreSQL 15+  
**Testing**: pytest, pytest-mock, pytest-cov, mutmut, mypy (strict), pylint, Playwright (Python)  
**Target Platform**: Linux containerized web deployment + modern desktop browsers
**Project Type**: Web application (frontend + backend)  
**Performance Goals**: p95 auth API response < 300ms under 100 concurrent users; login/logout success path < 2s UI round-trip  
**Constraints**: TDD-first delivery; RBAC correctness 100% for protected routes; stateless JWT auth; constitution quality gates (coverage + mutation)  
**Scale/Scope**: MVP for one portal with up to 10k user accounts and two roles

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Gate 1 — TDD First**: PASS (all implementation tasks will be written RED→GREEN→REFACTOR with tests authored before code).
- **Gate 2 — Test Taxonomy & Naming**: PASS (`tests/unit`, `tests/integration`, `tests/e2e`; `test_*.py`; AAA and independent tests enforced).
- **Gate 3 — Quality Thresholds**: PASS (line ≥80%, branch ≥75%, mutation ≥75%; mypy strict + pylint mandatory in CI).
- **Gate 4 — Mocking Rules**: PASS (only external services mocked; domain logic remains real in unit tests).
- **Gate 5 — Speed/Determinism**: PASS (unit <1s target, integration <5s target, deterministic fixtures).

Post-Design Re-check: PASS (Phase 1 artifacts preserve test-first flow and quality thresholds with no constitution violations).

## Project Structure

### Documentation (this feature)

```text
specs/001-user-auth-roles/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
│   ├── auth/
│   ├── rbac/
│   └── security/
├── migrations/
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── services/
│   └── guards/
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

**Structure Decision**: Web application structure selected because feature requires server-side auth/session control plus role-aware UI flows; backend and frontend are developed and tested independently with shared contract alignment.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
