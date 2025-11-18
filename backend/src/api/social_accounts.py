from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from src.models.database import get_db, SocialAccount, Platform
from sqlalchemy.orm import Session

router = APIRouter()


# Request models
class ConnectAccountRequest(BaseModel):
    platform: str
    account_name: str
    account_id: str
    access_token: str
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None


class UpdateAccountRequest(BaseModel):
    is_active: bool


# Endpoints
@router.post("/connect")
async def connect_social_account(
    user_id: int, request: ConnectAccountRequest, db: Session = Depends(get_db)
):
    """Connect a new social media account"""
    try:
        # Validate platform
        try:
            platform_enum = Platform[request.platform.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Invalid platform: {request.platform}")

        # Check if account already exists
        existing = (
            db.query(SocialAccount)
            .filter(
                SocialAccount.user_id == user_id,
                SocialAccount.platform == platform_enum,
                SocialAccount.account_id == request.account_id,
            )
            .first()
        )

        if existing:
            # Update existing account
            existing.access_token = request.access_token
            existing.refresh_token = request.refresh_token
            existing.token_expires_at = request.token_expires_at
            existing.is_active = True
            existing.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(existing)

            return {
                "success": True,
                "message": "Account updated successfully",
                "data": {
                    "account_id": existing.id,
                    "platform": existing.platform.value,
                    "account_name": existing.account_name,
                },
            }
        else:
            # Create new account
            new_account = SocialAccount(
                user_id=user_id,
                platform=platform_enum,
                account_name=request.account_name,
                account_id=request.account_id,
                access_token=request.access_token,
                refresh_token=request.refresh_token,
                token_expires_at=request.token_expires_at,
                is_active=True,
            )

            db.add(new_account)
            db.commit()
            db.refresh(new_account)

            return {
                "success": True,
                "message": "Account connected successfully",
                "data": {
                    "account_id": new_account.id,
                    "platform": new_account.platform.value,
                    "account_name": new_account.account_name,
                },
            }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_social_accounts(user_id: int, db: Session = Depends(get_db)):
    """List all connected social accounts for a user"""
    try:
        accounts = (
            db.query(SocialAccount)
            .filter(SocialAccount.user_id == user_id)
            .all()
        )

        result = []
        for account in accounts:
            result.append(
                {
                    "id": account.id,
                    "platform": account.platform.value,
                    "account_name": account.account_name,
                    "account_id": account.account_id,
                    "is_active": account.is_active,
                    "connected_at": account.connected_at.isoformat(),
                    "token_expires_at": account.token_expires_at.isoformat()
                    if account.token_expires_at
                    else None,
                }
            )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{account_id}")
async def get_social_account(account_id: int, db: Session = Depends(get_db)):
    """Get details of a specific social account"""
    try:
        account = db.query(SocialAccount).filter(SocialAccount.id == account_id).first()

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        return {
            "success": True,
            "data": {
                "id": account.id,
                "platform": account.platform.value,
                "account_name": account.account_name,
                "account_id": account.account_id,
                "is_active": account.is_active,
                "connected_at": account.connected_at.isoformat(),
                "updated_at": account.updated_at.isoformat(),
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{account_id}")
async def update_social_account(
    account_id: int, request: UpdateAccountRequest, db: Session = Depends(get_db)
):
    """Update social account settings"""
    try:
        account = db.query(SocialAccount).filter(SocialAccount.id == account_id).first()

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        account.is_active = request.is_active
        account.updated_at = datetime.utcnow()

        db.commit()

        return {"success": True, "message": "Account updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{account_id}")
async def disconnect_social_account(account_id: int, db: Session = Depends(get_db)):
    """Disconnect and remove a social account"""
    try:
        account = db.query(SocialAccount).filter(SocialAccount.id == account_id).first()

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        db.delete(account)
        db.commit()

        return {"success": True, "message": "Account disconnected successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
