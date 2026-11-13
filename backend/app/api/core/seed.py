# app/api/core/seed.py
from sqlalchemy.orm import Session
from app.api.models.users.user import User, UserRole
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_initial_users(db: Session):
    """Automatically seed default Super Admin and Director accounts if they don't exist."""
    
    # 1. Seed Super Admin
    existing_super_admin = db.query(User).filter(User.role == UserRole.SUPER_ADMIN).first()
    if not existing_super_admin:
        super_admin = User(
            email="superadmin@school.com",
            hashed_password=pwd_context.hash("supersecurepassword123"),
            full_name="System Super Admin",
            role=UserRole.SUPER_ADMIN,
            is_active=True
        )
        db.add(super_admin)
        db.commit()
        print("Default Super Admin account created: superadmin@school.com / supersecurepassword123")

    # 2. Seed Director
    existing_director = db.query(User).filter(User.role == UserRole.DIRECTOR).first()
    if not existing_director:
        director = User(
            email="director@school.com",
            hashed_password=pwd_context.hash("securepassword123"),
            full_name="School Director",
            role=UserRole.DIRECTOR,
            is_active=True
        )
        db.add(director)
        db.commit()
        print("Default Director account created: director@school.com / securepassword123")