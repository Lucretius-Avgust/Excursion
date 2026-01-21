from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID

from app.core.constants import PASSWORD_LEN_MAX, PASSWORD_LEN_MIN

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    password: str = Field(
        ...,
        min_length=PASSWORD_LEN_MIN,
        max_length=PASSWORD_LEN_MAX
    )


class UserLogin(BaseModel):
    login: str
    password: str


class UserRead(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
