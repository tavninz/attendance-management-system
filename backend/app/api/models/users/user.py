# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.api.core.database import Base 

from sqlalchemy import String, Column, Enum as SQLEnum
import enum

class UserRole(str, enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    DIRECTOR = "director"
    SUPER_ADMIN = "super_admin"

class EducationalLevel(str, enum.Enum):
    SUPERIOR = "Superior"  
    BASIC = "Basic"       

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    major = Column(String, nullable=True)
    educational_level = Column(SQLEnum(EducationalLevel), nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())