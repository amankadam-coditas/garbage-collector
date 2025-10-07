from pydantic import BaseModel, EmailStr, Field
from src.garbage_collector.schemas.enums import UserRoles


class User(BaseModel):
    email: EmailStr = Field(...)
    role: UserRoles


class UserSignIn(User):
    password: str = Field(...,)


class UserOutput(BaseModel):
    email: EmailStr = Field(...)
    user_role: str
