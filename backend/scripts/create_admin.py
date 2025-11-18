#!/usr/bin/env python
"""Create an admin user"""

import sys
from getpass import getpass

from src.models.database import SessionLocal, User, Subscription, SubscriptionTier
from src.utils.auth import get_password_hash


def create_admin():
    print("=== Create Admin User ===\n")

    email = input("Email: ")
    full_name = input("Full Name: ")
    password = getpass("Password: ")
    confirm_password = getpass("Confirm Password: ")

    if password != confirm_password:
        print("❌ Passwords do not match!")
        sys.exit(1)

    db = SessionLocal()

    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"❌ User with email {email} already exists!")
            sys.exit(1)

        # Create admin user
        admin = User(
            email=email,
            full_name=full_name,
            hashed_password=get_password_hash(password),
            subscription_tier=SubscriptionTier.AGENCY,
            is_active=True,
            is_verified=True,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        # Create subscription
        subscription = Subscription(
            user_id=admin.id,
            tier=SubscriptionTier.AGENCY,
            max_social_accounts=-1,  # Unlimited
            max_ai_generations_monthly=-1,
            max_image_generations_monthly=-1,
            status="active",
        )

        db.add(subscription)
        db.commit()

        print(f"\n✓ Admin user created successfully!")
        print(f"  ID: {admin.id}")
        print(f"  Email: {admin.email}")
        print(f"  Tier: {admin.subscription_tier.value}")

    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
