# Data Model: User Management

## Entity: UserAccount
- **Purpose**: Represents a registered portal identity.
- **Fields**:
  - `id` (UUID, primary key)
  - `email` (string, unique, required, normalized lowercase)
  - `password_hash` (string, required)
  - `role` (enum: `submitter` | `evaluator_admin`, required)
  - `status` (enum: `active` | `locked` | `disabled`, default `active`)
  - `failed_login_attempts` (integer, default `0`)
  - `last_login_at` (datetime, nullable)
  - `created_at` (datetime, required)
  - `updated_at` (datetime, required)
- **Validation Rules**:
  - `email` must be valid format and unique.
  - `password_hash` must never store plain text.
  - `role` must be one of the allowed enum values.

## Entity: SessionToken
- **Purpose**: Tracks refresh-token/session continuity and revocation.
- **Fields**:
  - `id` (UUID, primary key)
  - `user_id` (UUID, foreign key -> UserAccount.id)
  - `token_id` (string, unique, required)  
  - `issued_at` (datetime, required)
  - `expires_at` (datetime, required)
  - `revoked_at` (datetime, nullable)
  - `replaced_by_token_id` (string, nullable)
- **Validation Rules**:
  - `expires_at` must be greater than `issued_at`.
  - revoked tokens cannot be used for refresh/logout continuation.

## Entity: AuthenticationEvent
- **Purpose**: Audit trail for register/login/logout outcomes.
- **Fields**:
  - `id` (UUID, primary key)
  - `user_id` (UUID, nullable for failed unknown-user login attempts)
  - `event_type` (enum: `register_success` | `login_success` | `login_failed` | `logout_success` | `access_denied`)
  - `event_time` (datetime, required)
  - `source_ip` (string, nullable)
  - `user_agent` (string, nullable)
  - `metadata` (JSON, nullable)
- **Validation Rules**:
  - `event_type` must be valid enum value.
  - `event_time` must be server-generated.

## Relationships
- UserAccount `1 -> many` SessionToken
- UserAccount `1 -> many` AuthenticationEvent

## State Transitions

### UserAccount.status
- `active -> locked` (threshold of failed login attempts reached)
- `locked -> active` (admin/manual unlock or cooldown policy)
- `active -> disabled` (administrative action)
- `disabled` is terminal for login until explicitly re-enabled.

### SessionToken lifecycle
- `issued` (created on successful login)
- `rotated` (new token issued, previous token marked replaced)
- `revoked` (logout or compromise response)
- `expired` (time-based invalidation)
