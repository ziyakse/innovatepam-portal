# Research: User Management (Auth + Roles)

## Decision 1: Backend stack = Python + FastAPI
- **Decision**: Implement backend with Python 3.12 and FastAPI.
- **Rationale**: Constitution is explicitly Python-centric (pytest, mypy strict, pylint, mutmut, Playwright Python). FastAPI provides strong request/response validation and clean auth middleware patterns.
- **Alternatives considered**:
  - Node.js + Express: viable but mismatched with constitution tooling defaults.
  - Django/DRF: feature-complete but heavier than MVP needs.

## Decision 2: Database = PostgreSQL
- **Decision**: Use PostgreSQL 15+ as primary relational store.
- **Rationale**: Strong consistency, transactional safety for auth/account workflows, clear constraints for unique identity fields, and mature production operations.
- **Alternatives considered**:
  - SQLite: good for local prototyping, weaker for concurrent production load.
  - MongoDB: flexible schema but less natural fit for relational auth/session/audit model.

## Decision 3: Auth strategy = JWT (access + refresh)
- **Decision**: Use stateless JWT access tokens with refresh token rotation.
- **Rationale**: Works well for API-first frontend/backend split, scales horizontally without sticky server sessions, and supports explicit logout via refresh-token invalidation list/versioning.
- **Alternatives considered**:
  - Session-based auth: simpler invalidation semantics, but requires centralized session storage and tighter server affinity patterns.
  - OAuth-only external identity: out of current MVP scope.

## Decision 4: Password storage and policy
- **Decision**: Store only salted+hashed passwords via bcrypt; enforce minimum complexity and lockout throttling on repeated login failures.
- **Rationale**: Meets baseline security expectations for internal/external portal users and reduces credential compromise risk.
- **Alternatives considered**:
  - Argon2: strong option, but bcrypt selected for widespread operational familiarity in this team context.
  - Minimal password policy: rejected for security posture.

## Decision 5: Role model = enum-based RBAC
- **Decision**: Persist a single role per account in MVP with enum values: `submitter`, `evaluator_admin`.
- **Rationale**: Requirement requests basic distinction only; single-role model keeps authorization checks explicit and easy to test.
- **Alternatives considered**:
  - Multi-role per account: more flexible, unnecessary complexity for MVP.
  - Attribute-based access control (ABAC): overkill for two-role requirement.

## Decision 6: Frontend = React + Tailwind
- **Decision**: Build user auth screens and role-aware route guards with React and Tailwind.
- **Rationale**: Fast iteration for portal UI, straightforward state handling for auth context, and simple role-conditional rendering.
- **Alternatives considered**:
  - Next.js: powerful, but SSR/route framework not required for MVP scope.
  - Server-rendered pages only: less flexible for API-driven portal growth.

## Decision 7: Testing strategy implementation
- **Decision**: Enforce testing pyramid per constitution: unit-heavy service tests, integration tests for API+DB, E2E for critical register/login/logout + RBAC journey.
- **Rationale**: Directly satisfies constitutional non-negotiables and enables fast feedback without sacrificing end-to-end confidence.
- **Alternatives considered**:
  - E2E-heavy strategy: slower and brittle.
  - Integration-only strategy: insufficient UI/workflow confidence.

## Decision 8: External interface pattern
- **Decision**: Expose REST JSON endpoints for register, login, logout, and profile/current-user context; protect privileged routes with role check middleware/dependency.
- **Rationale**: Clear contract boundaries between frontend and backend and explicit authorization behavior testability.
- **Alternatives considered**:
  - GraphQL: unnecessary schema/infra complexity for limited endpoint set.
  - gRPC: poor browser-native ergonomics for this portal use case.
