# Tasks: InnovatEPAM Portal - User Management

**Input**: Design documents from `/specs/001-user-auth-roles/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/auth-api.openapi.yaml

**Tests**: Test tasks are mandatory for this feature and follow constitution Test-First principles.
**Testing Pyramid Allocation (MANDATORY)**: **7 Unit / 2 Integration / 1 E2E** = **70% / 20% / 10%**

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no direct dependency)
- **[Story]**: `US1`, `US2`, `US3`, or `Shared`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create project skeleton and baseline tooling.

- [ ] T001 [Shared] Create backend/frontend folder structure from plan in `backend/` and `frontend/`
- [ ] T002 [P] [Shared] Initialize backend dependencies and config in `backend/pyproject.toml`
- [ ] T003 [P] [Shared] Initialize frontend dependencies and config in `frontend/package.json`
- [ ] T004 [Shared] Configure CI quality gates (mypy, pylint, pytest, pytest-cov, mutmut) in `.github/workflows/ci.yml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core auth/rbac/database infrastructure required before user stories.

**⚠️ CRITICAL**: No user story implementation starts before this phase completes.

- [ ] T005 [Shared] Define base SQLAlchemy models and metadata in `backend/src/models/base.py`
- [ ] T006 [P] [Shared] Create Alembic initial migration setup in `backend/migrations/`
- [ ] T007 [P] [Shared] Implement password hashing and verification utilities in `backend/src/security/passwords.py`
- [ ] T008 [P] [Shared] Implement JWT token issue/verify helpers in `backend/src/security/tokens.py`
- [ ] T009 [Shared] Implement auth dependency and request user context in `backend/src/auth/dependencies.py`
- [ ] T010 [Shared] Implement RBAC guard for `submitter` vs `evaluator_admin` in `backend/src/rbac/guards.py`
- [ ] T011 [Shared] Implement centralized API error mapping for 401/403/409 in `backend/src/api/errors.py`
- [ ] T012 [Shared] Wire FastAPI app router + middleware skeleton in `backend/src/api/app.py`

**Checkpoint**: Foundation complete.

---

## Phase 3: User Story 1 - Account Access (Priority: P1) 🎯 MVP

**Goal**: Registration, login, logout with authenticated session behavior.

**Independent Test**: Register new user → login → logout → protected endpoint rejected.

### Tests for User Story 1 (write FIRST; ensure FAIL before code)

- [ ] T013 [P] [US1] **UNIT** test password utility behavior in `backend/tests/unit/security/test_passwords.py`
- [ ] T014 [P] [US1] **UNIT** test JWT token utility behavior in `backend/tests/unit/security/test_tokens.py`
- [ ] T015 [P] [US1] **UNIT** test auth service register/login/logout rules in `backend/tests/unit/services/test_auth_service.py`
- [ ] T016 [US1] **INTEGRATION** test `/auth/register`, `/auth/login`, `/auth/logout`, `/auth/me` flow in `backend/tests/integration/auth/test_auth_flow.py`

### Implementation for User Story 1

- [ ] T017 [US1] Implement `UserAccount`, `SessionToken`, `AuthenticationEvent` models in `backend/src/models/auth_models.py`
- [ ] T018 [US1] Implement auth service logic in `backend/src/services/auth_service.py` (depends on T017)
- [ ] T019 [US1] Implement auth API endpoints in `backend/src/api/auth_routes.py` (depends on T018)
- [ ] T020 [US1] Implement frontend auth pages (register/login) in `frontend/src/pages/auth/`
- [ ] T021 [US1] Implement frontend logout + auth state provider in `frontend/src/hooks/useAuth.tsx`

**Checkpoint**: US1 independently functional and testable (MVP).

---

## Phase 4: User Story 2 - Role-Based Experience Separation (Priority: P2)

**Goal**: Submitter/evaluator-admin role distinction and route protection.

**Independent Test**: Submitter denied on admin route; evaluator/admin granted.

### Tests for User Story 2 (write FIRST; ensure FAIL before code)

- [ ] T022 [P] [US2] **UNIT** test RBAC guard decision matrix in `backend/tests/unit/rbac/test_guards.py`
- [ ] T023 [P] [US2] **UNIT** test role-aware UI guard logic in `frontend/tests/unit/guards/test_role_guard.ts`
- [ ] T024 [US2] **INTEGRATION** test backend protected admin route authorization in `backend/tests/integration/rbac/test_admin_access.py`

### Implementation for User Story 2

- [ ] T025 [US2] Implement admin-only route example `/admin/evaluations` in `backend/src/api/admin_routes.py`
- [ ] T026 [US2] Enforce role checks in protected endpoints via dependencies in `backend/src/api/`
- [ ] T027 [US2] Implement frontend role guard and restricted route behavior in `frontend/src/guards/RoleGuard.tsx`
- [ ] T028 [US2] Add role-aware navigation visibility in `frontend/src/components/navigation/`

**Checkpoint**: US1 + US2 both independently testable.

---

## Phase 5: User Story 3 - Admin/Evaluator Continuity (Priority: P3)

**Goal**: Privileged session continuity and revocation correctness for evaluator/admin.

**Independent Test**: Admin login keeps privileged access in-session; logout removes access immediately.

### Tests for User Story 3 (write FIRST; ensure FAIL before code)

- [ ] T029 [P] [US3] **UNIT** test refresh-token rotation/revocation behavior in `backend/tests/unit/auth/test_session_token_lifecycle.py`
- [ ] T030 [P] [US3] **UNIT** test failed-login lockout/cooldown policy in `backend/tests/unit/services/test_login_protection.py`
- [ ] T031 [US3] **E2E** test full user journey (register/login/logout + role-restricted access) in `backend/tests/e2e/test_user_management_journey.py`

### Implementation for User Story 3

- [ ] T032 [US3] Implement session token rotation + revocation persistence in `backend/src/services/session_service.py`
- [ ] T033 [US3] Implement failed-login throttling/lockout policy in `backend/src/services/auth_service.py`
- [ ] T034 [US3] Integrate policy feedback responses (locked/unauthorized) in `backend/src/api/auth_routes.py`

**Checkpoint**: All user stories independently functional.

---

## Phase 6: Polish & Cross-Cutting

- [ ] T035 [P] [Shared] Update API contract examples and response docs in `specs/001-user-auth-roles/contracts/auth-api.openapi.yaml`
- [ ] T036 [Shared] Validate quickstart flow end-to-end using `specs/001-user-auth-roles/quickstart.md`
- [ ] T037 [Shared] Run full quality gate and record results (coverage/mutation/type/lint) in `specs/001-user-auth-roles/checklists/requirements.md`

---

## Dependencies & Execution Order

### Phase Dependencies
- Setup (Phase 1) → Foundational (Phase 2) → User Stories (Phase 3/4/5) → Polish (Phase 6)
- User stories start only after Phase 2 completion.

### User Story Dependencies
- **US1 (P1)**: No dependency on other stories (MVP).
- **US2 (P2)**: Depends on foundational RBAC + integrates with US1 auth context.
- **US3 (P3)**: Depends on US1 auth lifecycle; extends privileged-session behavior.

### Within Each Story (TDD Enforcement)
- Tests first and failing before any implementation tasks.
- Models/services before API wiring.
- Backend authorization correctness before frontend guard polish.

---

## Parallel Execution Examples

### US1 Test Parallelism
- Run T013, T014, T015 together (separate files).

### US2 Parallelism
- Run T022 and T023 in parallel (backend/frontend separate files).

### US3 Parallelism
- Run T029 and T030 in parallel (independent service concerns).

---

## Implementation Strategy

### MVP First
1. Finish Phase 1 and 2.
2. Deliver US1 completely (tests + implementation).
3. Validate against SC-001, SC-002, SC-004.

### Incremental Delivery
1. Add US2 and validate SC-003.
2. Add US3 and validate continuity requirements + SC-005.
3. Execute full quality gate from constitution.
