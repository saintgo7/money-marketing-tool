from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime

from src.models.database import get_db, User, Subscription, SubscriptionTier
from src.utils.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_active_user,
)

router = APIRouter()


# Request/Response models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    company_name: str = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    company_name: str = None
    subscription_tier: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)

    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        company_name=user_data.company_name,
        subscription_tier=SubscriptionTier.FREE,
        is_active=True,
        is_verified=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create free subscription
    subscription = Subscription(
        user_id=new_user.id,
        tier=SubscriptionTier.FREE,
        max_social_accounts=3,
        max_ai_generations_monthly=30,
        max_image_generations_monthly=0,
        status="active",
    )

    db.add(subscription)
    db.commit()

    return new_user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token"""
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information"""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    full_name: str = None,
    company_name: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user information"""
    if full_name:
        current_user.full_name = full_name

    if company_name:
        current_user.company_name = company_name

    current_user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(current_user)

    return current_user


@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    from src.utils.auth import verify_password, get_password_hash

    # Verify current password
    if not verify_password(current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    # Update password
    current_user.hashed_password = get_password_hash(new_password)
    current_user.updated_at = datetime.utcnow()

    db.commit()

    return {"message": "Password updated successfully"}


@router.delete("/me")
async def delete_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete user account"""
    db.delete(current_user)
    db.commit()

    return {"message": "Account deleted successfully"}
