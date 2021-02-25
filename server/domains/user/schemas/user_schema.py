from typing import Optional
from pydantic import BaseModel
from enum import Enum

class UserRole(Enum):
    Admin = "admin"    
    Parent = "parent"
    Student = "student"
    teacher = "teacher"

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    role_id: Optional[int]

class UserCreateRequest(UserBase):
    password: str
    role: UserRole


class UserDelete(UserBase):
    pass


class UserSchema(UserBase):
    id: int
    is_activate: bool = True
    role_id: int

    class Config:
        orm_mode = True
