# app/schemas/leave.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from app.api.models.leave.leave import LeaveStatus

class LeaveRequestCreate(BaseModel):
    start_date: date
    end_date: date
    reason: str
    leave_paper_image_url: Optional[str] = None  # URL or path to uploaded paper slip image

class LeaveRequestResponse(BaseModel):
    id: int
    user_id: int
    start_date: date
    end_date: date
    reason: str
    leave_paper_image_url: Optional[str] = None
    status: LeaveStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }