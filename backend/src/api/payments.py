from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
import stripe

from src.config import settings
from src.models.database import get_db, User, Subscription, SubscriptionTier
from src.utils.auth import get_current_active_user

# Initialize Stripe
if settings.stripe_secret_key:
    stripe.api_key = settings.stripe_secret_key

router = APIRouter()


# Subscription tier pricing
TIER_PRICING = {
    SubscriptionTier.FREE: {"price": 0, "price_id": None},
    SubscriptionTier.STARTER: {"price": 29, "price_id": "price_starter"},
    SubscriptionTier.PRO: {"price": 79, "price_id": "price_pro"},
    SubscriptionTier.AGENCY: {"price": 199, "price_id": "price_agency"},
}

# Tier limits
TIER_LIMITS = {
    SubscriptionTier.FREE: {
        "max_social_accounts": 3,
        "max_ai_generations_monthly": 30,
        "max_image_generations_monthly": 0,
    },
    SubscriptionTier.STARTER: {
        "max_social_accounts": 10,
        "max_ai_generations_monthly": 200,
        "max_image_generations_monthly": 50,
    },
    SubscriptionTier.PRO: {
        "max_social_accounts": 25,
        "max_ai_generations_monthly": -1,  # Unlimited
        "max_image_generations_monthly": 200,
    },
    SubscriptionTier.AGENCY: {
        "max_social_accounts": -1,  # Unlimited
        "max_ai_generations_monthly": -1,
        "max_image_generations_monthly": -1,
    },
}


class CreateCheckoutSessionRequest(BaseModel):
    tier: str
    success_url: str
    cancel_url: str


class SubscriptionResponse(BaseModel):
    tier: str
    status: str
    max_social_accounts: int
    max_ai_generations_monthly: int
    max_image_generations_monthly: int
    ai_generations_used: int
    image_generations_used: int
    current_period_end: Optional[datetime] = None


@router.post("/create-checkout-session")
async def create_checkout_session(
    request: CreateCheckoutSessionRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Create a Stripe checkout session for subscription"""

    if not settings.stripe_secret_key:
        raise HTTPException(status_code=500, detail="Stripe not configured")

    try:
        tier = SubscriptionTier[request.tier.upper()]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid subscription tier")

    if tier == SubscriptionTier.FREE:
        raise HTTPException(status_code=400, detail="Cannot checkout for free tier")

    pricing = TIER_PRICING[tier]

    # Create or get Stripe customer
    if not current_user.stripe_customer_id:
        customer = stripe.Customer.create(
            email=current_user.email,
            name=current_user.full_name,
            metadata={"user_id": current_user.id},
        )
        current_user.stripe_customer_id = customer.id
        db.commit()

    # Create checkout session
    session = stripe.checkout.Session.create(
        customer=current_user.stripe_customer_id,
        payment_method_types=["card"],
        line_items=[
            {
                "price": pricing["price_id"],
                "quantity": 1,
            }
        ],
        mode="subscription",
        success_url=request.success_url,
        cancel_url=request.cancel_url,
        metadata={
            "user_id": current_user.id,
            "tier": tier.value,
        },
    )

    return {"checkout_url": session.url, "session_id": session.id}


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhooks"""

    if not settings.stripe_webhook_secret:
        raise HTTPException(status_code=500, detail="Stripe webhook secret not configured")

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        await handle_checkout_completed(session, db)

    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        await handle_subscription_updated(subscription, db)

    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        await handle_subscription_cancelled(subscription, db)

    return {"status": "success"}


async def handle_checkout_completed(session, db: Session):
    """Handle successful checkout"""
    user_id = int(session["metadata"]["user_id"])
    tier = SubscriptionTier(session["metadata"]["tier"])

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return

    # Update user subscription tier
    user.subscription_tier = tier

    # Get or create subscription
    subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()

    if not subscription:
        subscription = Subscription(user_id=user_id)
        db.add(subscription)

    # Update subscription
    limits = TIER_LIMITS[tier]
    subscription.tier = tier
    subscription.stripe_subscription_id = session["subscription"]
    subscription.max_social_accounts = limits["max_social_accounts"]
    subscription.max_ai_generations_monthly = limits["max_ai_generations_monthly"]
    subscription.max_image_generations_monthly = limits["max_image_generations_monthly"]
    subscription.current_period_start = datetime.utcnow()
    subscription.current_period_end = datetime.utcnow() + timedelta(days=30)
    subscription.status = "active"

    db.commit()


async def handle_subscription_updated(subscription_data, db: Session):
    """Handle subscription updates"""
    stripe_subscription_id = subscription_data["id"]

    subscription = db.query(Subscription).filter(
        Subscription.stripe_subscription_id == stripe_subscription_id
    ).first()

    if subscription:
        subscription.status = subscription_data["status"]
        subscription.current_period_end = datetime.fromtimestamp(
            subscription_data["current_period_end"]
        )
        db.commit()


async def handle_subscription_cancelled(subscription_data, db: Session):
    """Handle subscription cancellation"""
    stripe_subscription_id = subscription_data["id"]

    subscription = db.query(Subscription).filter(
        Subscription.stripe_subscription_id == stripe_subscription_id
    ).first()

    if subscription:
        subscription.status = "canceled"
        subscription.cancel_at_period_end = True

        # Downgrade user to free tier at period end
        user = db.query(User).filter(User.id == subscription.user_id).first()
        if user:
            user.subscription_tier = SubscriptionTier.FREE

        db.commit()


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get current user's subscription"""
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).first()

    if not subscription:
        # Create free subscription if not exists
        subscription = Subscription(
            user_id=current_user.id,
            tier=SubscriptionTier.FREE,
            **TIER_LIMITS[SubscriptionTier.FREE],
            status="active",
        )
        db.add(subscription)
        db.commit()
        db.refresh(subscription)

    return subscription


@router.post("/cancel-subscription")
async def cancel_subscription(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Cancel current subscription"""
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).first()

    if not subscription or not subscription.stripe_subscription_id:
        raise HTTPException(status_code=400, detail="No active subscription")

    # Cancel at period end
    stripe.Subscription.modify(
        subscription.stripe_subscription_id,
        cancel_at_period_end=True
    )

    subscription.cancel_at_period_end = True
    db.commit()

    return {"message": "Subscription will be cancelled at period end"}


@router.get("/usage")
async def get_usage(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get current usage statistics"""
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).first()

    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    # Calculate percentages
    ai_percentage = 0
    if subscription.max_ai_generations_monthly > 0:
        ai_percentage = (subscription.ai_generations_used / subscription.max_ai_generations_monthly) * 100

    image_percentage = 0
    if subscription.max_image_generations_monthly > 0:
        image_percentage = (subscription.image_generations_used / subscription.max_image_generations_monthly) * 100

    return {
        "tier": subscription.tier.value,
        "ai_generations": {
            "used": subscription.ai_generations_used,
            "limit": subscription.max_ai_generations_monthly,
            "percentage": ai_percentage,
            "unlimited": subscription.max_ai_generations_monthly == -1,
        },
        "image_generations": {
            "used": subscription.image_generations_used,
            "limit": subscription.max_image_generations_monthly,
            "percentage": image_percentage,
            "unlimited": subscription.max_image_generations_monthly == -1,
        },
        "period_end": subscription.current_period_end,
    }
