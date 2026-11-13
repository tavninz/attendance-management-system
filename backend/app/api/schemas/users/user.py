# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional 
from datetime import datetime
from app.api.models.users.user import UserRole, EducationalLevel

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.STUDENT
    major: Optional[str] = None
    educational_level: Optional[EducationalLevel] = None

# Properties received on user creation/signup
class UserCreate(UserBase):
    password: str

# Properties received on login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Properties returned to the client (excludes sensitive data like password)
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True  # Replaces old orm_mode = True in Pydantic v2
    }

# Token response model for authentication
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse