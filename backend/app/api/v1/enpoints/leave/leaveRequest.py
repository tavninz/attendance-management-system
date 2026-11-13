from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import extract, func

from app.api.core.database import get_db
from app.api.models.users.user import User, UserRole
from app.api.models.leave.leave import LeaveRequest, LeaveStatus
from app.api.schemas.leave.leave import LeaveRequestCreate, LeaveRequestResponse
from app.api.v1.enpoints.users.auth import get_current_user

from app.api.models.leave.leave import LeaveStatus
from app.api.v1.enpoints.users.auth import get_current_director
from pydantic import BaseModel

router = APIRouter(prefix="/leave", tags=["Leave Requests"])


class LeaveStatusUpdate(BaseModel):
    status: LeaveStatus  # Can be 'approved' or 'rejected'

@router.get("/director/pending", response_model=List[LeaveRequestResponse])
def get_pending_leave_requests(
    db: Session = Depends(get_db),
    director: User = Depends(get_current_director)
):
    """
    Director-only route: View all leave requests that are pending review and alert verification.
    """
    return db.query(LeaveRequest).filter(LeaveRequest.status == LeaveStatus.PENDING).all()

@router.patch("/director/{leave_id}/review", response_model=LeaveRequestResponse)
def review_leave_request(
    leave_id: int,
    review_in: LeaveStatusUpdate,
    db: Session = Depends(get_db),
    director: User = Depends(get_current_director)
):
    """
    Director-only route: Approve or reject a student/staff leave request.
    """
    leave_req = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave_req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found"
        )

    leave_req.status = review_in.status
    db.commit()
    db.refresh(leave_req)
    return leave_req

@router.post("/", response_model=LeaveRequestResponse, status_code=status.HTTP_201_CREATED)
def submit_leave_request(
    leave_in: LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit a new leave request. It automatically starts as 'pending' 
    awaiting director review or paper submission verification.
    """
    if leave_in.start_date > leave_in.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date cannot be later than end date"
        )
    
    calculated_days = (leave_in.end_date - leave_in.start_date).days + 1
    
    db_leave = LeaveRequest(
        user_id=current_user.id,
        start_date=leave_in.start_date,
        end_date=leave_in.end_date,
        total_days=calculated_days,
        reason=leave_in.reason,
        leave_paper_image_url=leave_in.leave_paper_image_url,
        status=LeaveStatus.PENDING
    )

    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave

@router.get("/", response_model=List[LeaveRequestResponse])
def get_user_leave_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all leave requests submitted by the currently logged-in user.
    """
    requests = db.query(LeaveRequest).filter(LeaveRequest.user_id == current_user.id).all()
    return requests


@router.get("/reports/summary")
def get_teacher_leave_report(
    year: int,
    month: int | None = None,
    db: Session = Depends(get_db),
    director: User = Depends(get_current_director)
):
    """
    Director/Admin Report: Get leave statistics (total requests count & total days taken) 
    grouped by teachers for a specific year and optional month.
    """
    query = db.query(
        User.id,
        User.full_name,
        User.major,
        User.educational_level,
        func.count(LeaveRequest.id).label("total_requests"),
        func.coalesce(func.sum(LeaveRequest.total_days), 0).label("total_days_absent")
    ).outerjoin(LeaveRequest, User.id == LeaveRequest.user_id) \
     .filter(User.role == UserRole.TEACHER)

    # Filter by Year based on start_date
    query = query.filter(extract('year', LeaveRequest.start_date) == year)

    # Optional Filter by Month
    if month:
        query = query.filter(extract('month', LeaveRequest.start_date) == month)

    results = query.group_by(User.id).all()

    return [
        {
            "teacher_id": row.id,
            "full_name": row.full_name,
            "major": row.major,
            "educational_level": row.educational_level,
            "total_leave_requests_in_period": row.total_requests,
            "total_days_absent": row.total_days_absent,
        }
        for row in results
    ]