from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# ─── AssesmentType Schemas ─────────────────────────────────────────────────────────────────

class AssessmentTypeBase(BaseModel):
    name: str

class AssessmentTypeCreate(AssessmentTypeBase):
    pass

class AssessmentTypeRead(AssessmentTypeBase):
    id: int

    class Config:
        orm_mode = True

# ─── UserGroup Schemas ─────────────────────────────────────────────────────────────────

from pydantic import BaseModel

class UserGroupBase(BaseModel):
    name: str
    assessment_type_id: int

class UserGroupCreate(UserGroupBase):
    pass  # Inherits directly without additional fields

class UserGroupRead(UserGroupBase):
    id: int  # Additional field for reading data

    class Config:
        orm_mode = True


# ─── User Schemas ─────────────────────────────────────────────────────────────────

from pydantic import BaseModel, EmailStr
from typing import Optional
from .schemas import UserGroupRead

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    group_id: int

class UserRead(UserBase):
    id: int
    group: UserGroupRead  # Nested schema to include group details

    class Config:
        orm_mode = True

# ─── Assesment Schemas ─────────────────────────────────────────────────────────────────

class AssessmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    type_id: int

class AssessmentCreate(AssessmentBase):
    pass  # No 'is_active' field allowed from client

class AssessmentRead(AssessmentBase):
    id: int
    version: int
    is_active: bool
    type: AssessmentTypeRead

    class Config:
        orm_mode = True

