"""
Seed data for development and testing
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.models.database import (
    User, SocialAccount, Content, Post, Campaign, Analytics,
    Subscription, SubscriptionTier, ContentStatus, Platform
)
from src.utils.auth import get_password_hash


def seed_database(db: Session):
    """Seed database with sample data"""

    print("🌱 Starting database seeding...")

    # Create demo user
    demo_user = User(
        email="demo@moneymarketing.io",
        hashed_password=get_password_hash("demo123456"),
        full_name="Demo User",
        company_name="Demo Company",
        subscription_tier=SubscriptionTier.PRO,
        is_active=True,
        is_verified=True
    )
    db.add(demo_user)
    db.flush()

    print(f"✓ Created demo user: {demo_user.email}")

    # Create subscription
    subscription = Subscription(
        user_id=demo_user.id,
        tier=SubscriptionTier.PRO,
        max_social_accounts=25,
        max_ai_generations_monthly=-1,
        max_image_generations_monthly=200,
        ai_generations_used=45,
        image_generations_used=12,
        status="active",
        current_period_start=datetime.utcnow(),
        current_period_end=datetime.utcnow() + timedelta(days=30)
    )
    db.add(subscription)

    # Create social accounts
    social_accounts = [
        SocialAccount(
            user_id=demo_user.id,
            platform=Platform.INSTAGRAM,
            account_name="@democompany",
            account_id="instagram_demo_123",
            is_active=True
        ),
        SocialAccount(
            user_id=demo_user.id,
            platform=Platform.LINKEDIN,
            account_name="Demo Company",
            account_id="linkedin_demo_456",
            is_active=True
        ),
        SocialAccount(
            user_id=demo_user.id,
            platform=Platform.TWITTER,
            account_name="@democompany",
            account_id="twitter_demo_789",
            is_active=True
        )
    ]

    for account in social_accounts:
        db.add(account)

    db.flush()
    print(f"✓ Created {len(social_accounts)} social accounts")

    # Create sample content
    contents = [
        Content(
            user_id=demo_user.id,
            title="5 Tips for Better Productivity",
            text_content="Discover 5 proven strategies to boost your productivity and achieve more in less time...",
            platform=Platform.INSTAGRAM,
            content_type="post",
            status=ContentStatus.PUBLISHED,
            generated_by_ai=True,
            ai_model="claude-sonnet-4-20250514",
            hashtags=["#productivity", "#tips", "#business", "#motivation"]
        ),
        Content(
            user_id=demo_user.id,
            title="How AI is Transforming Marketing",
            text_content="Artificial Intelligence is revolutionizing the marketing industry. Here's what you need to know...",
            platform=Platform.LINKEDIN,
            content_type="post",
            status=ContentStatus.PUBLISHED,
            generated_by_ai=True,
            ai_model="claude-sonnet-4-20250514",
            hashtags=["#AI", "#marketing", "#innovation", "#technology"]
        ),
        Content(
            user_id=demo_user.id,
            title="Quick Marketing Tips Thread",
            text_content="Let me share 10 quick marketing tips that can transform your business...",
            platform=Platform.TWITTER,
            content_type="thread",
            status=ContentStatus.SCHEDULED,
            generated_by_ai=True,
            ai_model="claude-sonnet-4-20250514",
            hashtags=["#marketing", "#tips", "#business"]
        )
    ]

    for content in contents:
        db.add(content)

    db.flush()
    print(f"✓ Created {len(contents)} content items")

    # Create posts
    posts = [
        Post(
            content_id=contents[0].id,
            social_account_id=social_accounts[0].id,
            scheduled_time=datetime.utcnow() - timedelta(days=2),
            published_at=datetime.utcnow() - timedelta(days=2),
            status=ContentStatus.PUBLISHED,
            platform_post_id="instagram_post_123",
            impressions=5240,
            reach=4890,
            likes=342,
            comments=28,
            shares=15,
            saves=87,
            engagement_rate=0.065
        ),
        Post(
            content_id=contents[1].id,
            social_account_id=social_accounts[1].id,
            scheduled_time=datetime.utcnow() - timedelta(days=1),
            published_at=datetime.utcnow() - timedelta(days=1),
            status=ContentStatus.PUBLISHED,
            platform_post_id="linkedin_post_456",
            impressions=3890,
            reach=3420,
            likes=198,
            comments=45,
            shares=67,
            engagement_rate=0.058
        ),
        Post(
            content_id=contents[2].id,
            social_account_id=social_accounts[2].id,
            scheduled_time=datetime.utcnow() + timedelta(hours=3),
            status=ContentStatus.SCHEDULED
        )
    ]

    for post in posts:
        db.add(post)

    db.flush()
    print(f"✓ Created {len(posts)} posts")

    # Create campaign
    campaign = Campaign(
        user_id=demo_user.id,
        name="Product Launch Campaign",
        description="Multi-platform campaign for new product launch",
        objective="awareness",
        platforms=["instagram", "linkedin", "twitter"],
        posting_frequency="daily",
        start_date=datetime.utcnow() - timedelta(days=7),
        end_date=datetime.utcnow() + timedelta(days=23),
        budget=5000.0,
        target_reach=50000,
        is_active=True
    )
    db.add(campaign)
    db.flush()

    # Link posts to campaign
    posts[0].campaign_id = campaign.id
    posts[1].campaign_id = campaign.id

    print("✓ Created campaign")

    # Create analytics data
    analytics_data = []
    for i in range(7):
        date = datetime.utcnow() - timedelta(days=6-i)

        analytics_data.append(
            Analytics(
                user_id=demo_user.id,
                platform=Platform.INSTAGRAM,
                date=date,
                total_posts=2 + i % 3,
                total_impressions=4000 + i * 500,
                total_reach=3500 + i * 400,
                total_engagement=250 + i * 30,
                avg_engagement_rate=0.045 + i * 0.005,
                follower_count=5000 + i * 50
            )
        )

    for analytics in analytics_data:
        db.add(analytics)

    print(f"✓ Created {len(analytics_data)} analytics records")

    # Commit all changes
    db.commit()

    print("\n✅ Database seeding completed!")
    print(f"\nDemo account credentials:")
    print(f"  Email: demo@moneymarketing.io")
    print(f"  Password: demo123456")
    print(f"\n🚀 You can now login and explore the platform!")


def clear_database(db: Session):
    """Clear all data from database"""
    print("🗑️  Clearing database...")

    # Delete in reverse order of dependencies
    db.query(Analytics).delete()
    db.query(Post).delete()
    db.query(Campaign).delete()
    db.query(Content).delete()
    db.query(SocialAccount).delete()
    db.query(Subscription).delete()
    db.query(User).delete()

    db.commit()
    print("✓ Database cleared")


if __name__ == "__main__":
    from src.models.database import SessionLocal

    db = SessionLocal()
    try:
        # Clear existing data
        clear_database(db)

        # Seed new data
        seed_database(db)

    finally:
        db.close()
