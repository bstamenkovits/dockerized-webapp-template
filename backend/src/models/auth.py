from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from datetime import datetime
from models.base import Base


class AuthUser(Base):
    __tablename__ = "auth_users"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    display_name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[str] = mapped_column(default=lambda: datetime.now().isoformat())
    updated_at: Mapped[str] = mapped_column(default=lambda: datetime.now().isoformat())


class AuthSession(Base):
    __tablename__ = "auth_sessions"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("auth_users.id"))
    created_at: Mapped[str]
    expires_at: Mapped[str]
    revoked_at: Mapped[str | None] = mapped_column(default=None)
    user_last_active: Mapped[str | None] = mapped_column(default=None)
