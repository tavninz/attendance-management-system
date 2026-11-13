# app/models/leave.py
from sqlalchemy import Column, Date, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.api.core.database import Base 
import enum

class LeaveStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Change DateTime to Date for leave periods
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_days = Column(Integer, nullable=False)
    reason = Column(Text, nullable=False)
    leave_paper_image_url = Column(String, nullable=True)
    status = Column(SQLEnum(LeaveStatus), default=LeaveStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())