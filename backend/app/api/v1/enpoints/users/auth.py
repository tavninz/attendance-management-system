# app/api/v1/endpoints/auth.py
import json
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from passlib.context import CryptContext 
from jose import JWTError, jwt

from app.api.core.config import settings
from app.api.core.database import get_db
from app.api.models.users.user import User,UserRole
from app.api.schemas.users.user import UserLogin, UserCreate, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Generate a secure signed JWT token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# --- DEPENDENCY TO PROTECT ROUTES (e.g., Orders) ---
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security), 
    db: Session = Depends(get_db)
) -> User:
    """
    Extracts the Bearer token from headers, verifies the signature and expiration,
    and returns the authenticated user from the database.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
        raise credentials_exception
        
    return user

def get_current_super_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Ensures the authenticated user has 'super_admin' privileges.
    """
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super Admin privileges required"
        )
    return current_user

def get_current_director(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.DIRECTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges (Director access required)"
        )
    return current_user

def get_current_admin_or_director(current_user: User = Depends(get_current_user)) -> User:
    """
    Allows access if the user is either a Super Admin or a Director.
    """
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.DIRECTOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Super Admin or Director privileges required."
        )
    return current_user

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Any logged-in user, but we check permissions below
):
    # 1. Check if user has permission to register new accounts
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.DIRECTOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create accounts."
        )

    # 2. Enforce tier restrictions: Directors cannot create other Directors or Super Admins
    if current_user.role == UserRole.DIRECTOR and user_in.role in [UserRole.DIRECTOR, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Directors can only register Teachers or Students."
        )

    # 3. Check if email already exists
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 4. Create the user
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role,
        major=user_in.major,
        educational_level=user_in.educational_level,
        is_active=True
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user account")

    # Generate real signed JWT token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id, "sub": user.email}, 
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user),
    }