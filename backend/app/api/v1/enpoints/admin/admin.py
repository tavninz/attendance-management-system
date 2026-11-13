# app/api/v1/endpoints/admin.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.core.database import get_db
from app.api.models.users.user import User, UserRole
from app.api.schemas.users.user import UserResponse
from app.api.v1.enpoints.users.auth import get_current_super_admin

router = APIRouter(prefix="/admin", tags=["Super Admin"])

@router.get("/users", response_model=List[UserResponse])
def get_all_system_users(
    db: Session = Depends(get_db),
    super_admin: User = Depends(get_current_super_admin)
):
    """
    Super Admin only: View all users in the system (Students, Teachers, Directors).
    """
    return db.query(User).all()

@router.patch("/users/{user_id}/promote", response_model=UserResponse)
def promote_user_role(
    user_id: int,
    new_role: UserRole,
    db: Session = Depends(get_db),
    super_admin: User = Depends(get_current_super_admin)
):
    """
    Super Admin only: Promote any user account to Director, Teacher, or Super Admin.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.role = new_role
    db.commit()
    db.refresh(user)
    return user