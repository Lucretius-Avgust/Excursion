from enum import IntEnum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Enum
from sqlalchemy.schema import UniqueConstraint, Index

from app.core.db import Base
from app.models.mixins.timestamp import TimestampMixin
from app.core.constants import (
    USERNAME_LEN, EMAIL_LEN, PHONE_LEN, HASHED_PASSWORD_LEN
)


class UserRole(IntEnum):
    """
    Роли пользователей.

    Используется для обозначения текущей роли:
    - CUSTOMER      (1): Покупатель.
    - GUIDE         (2): Гид.
    - ADMIN         (3): Админ.
    """

    CUSTOMER = 1
    GUIDE = 2
    ADMIN = 3

    @property
    def label(self) -> str:
        return {
            UserRole.CUSTOMER: "Customer",
            UserRole.GUIDE: "Guide",
            UserRole.ADMIN: "Admin",
        }[self]


class User(Base, TimestampMixin):

    first_name: Mapped[str] = mapped_column(
        String(USERNAME_LEN), nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(USERNAME_LEN), nullable=False
    )
    middle_name: Mapped[str] = mapped_column(
        String(USERNAME_LEN), nullable=True
    )
    email: Mapped[str] = mapped_column(
        String(EMAIL_LEN), nullable=False
    )
    phone: Mapped[str] = mapped_column(
        String(PHONE_LEN), nullable=True
    )
    hashed_password: Mapped[str] = mapped_column(
        String(HASHED_PASSWORD_LEN), nullable=False
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.CUSTOMER
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        Index("ix_users_email", "email"),
        Index("ix_users_role", "role"),
    )

    def role_label(self) -> str:
        return self.role.label

    def __repr__(self) -> str:
        return f"User: {self.id} email: {self.email} role: {self.role_label()}"

    @property
    def is_superuser(self) -> bool:
        return self.role == UserRole.ADMIN
