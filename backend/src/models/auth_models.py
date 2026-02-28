from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from sqlalchemy import DateTime, Enum as SAEnum, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class UserRole(str, Enum):
    SUBMITTER = "submitter"
    EVALUATOR_ADMIN = "evaluator_admin"


@dataclass
class UserRecord:
    id: str
    email: str
    password_hash: str
    role: str


class UserAccount(Base):
    __tablename__ = "user_accounts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, name="user_role"),
        default=UserRole.SUBMITTER,
        nullable=False,
    )


class SessionToken(Base):
    __tablename__ = "session_tokens"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    token: Mapped[str] = mapped_column(String(1024), unique=True, nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    issued_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class AuthenticationEvent(Base):
    __tablename__ = "authentication_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), nullable=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    event_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
