from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Float,
    Boolean,
    ForeignKey,
    JSON,
    Enum as SQLEnum,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum

from src.config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    pool_size=settings.database_pool_size,
    max_overflow=20,
    echo=settings.debug,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Enums
class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"
    AGENCY = "agency"


class ContentStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"


class Platform(str, enum.Enum):
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    PINTEREST = "pinterest"


# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    company_name = Column(String(255))
    subscription_tier = Column(SQLEnum(SubscriptionTier), default=SubscriptionTier.FREE)
    stripe_customer_id = Column(String(255), unique=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    social_accounts = relationship("SocialAccount", back_populates="user", cascade="all, delete-orphan")
    contents = relationship("Content", back_populates="user", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="user", cascade="all, delete-orphan")


class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(SQLEnum(Platform), nullable=False)
    account_name = Column(String(255))
    account_id = Column(String(255))  # Platform-specific account ID
    access_token = Column(Text)  # Encrypted in production
    refresh_token = Column(Text)  # Encrypted in production
    token_expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    connected_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="social_accounts")
    posts = relationship("Post", back_populates="social_account")


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(500))
    text_content = Column(Text)
    platform = Column(SQLEnum(Platform), nullable=False)
    content_type = Column(String(50))  # post, story, reel, carousel, thread
    status = Column(SQLEnum(ContentStatus), default=ContentStatus.DRAFT)

    # AI Generation metadata
    generated_by_ai = Column(Boolean, default=True)
    ai_model = Column(String(100))
    generation_params = Column(JSON)

    # Media
    media_urls = Column(JSON)  # List of image/video URLs
    thumbnail_url = Column(String(500))

    # Metadata
    hashtags = Column(JSON)  # List of hashtags
    mentions = Column(JSON)  # List of mentions

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="contents")
    posts = relationship("Post", back_populates="content")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    social_account_id = Column(Integer, ForeignKey("social_accounts.id"), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)

    # Scheduling
    scheduled_time = Column(DateTime)
    published_at = Column(DateTime)

    # Platform response
    platform_post_id = Column(String(255))  # ID from the social platform
    platform_url = Column(String(500))

    # Status
    status = Column(SQLEnum(ContentStatus), default=ContentStatus.SCHEDULED)
    error_message = Column(Text)

    # Metrics (updated periodically)
    impressions = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)

    metrics_last_updated = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    content = relationship("Content", back_populates="posts")
    social_account = relationship("SocialAccount", back_populates="posts")
    campaign = relationship("Campaign", back_populates="posts")


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    # Campaign settings
    objective = Column(String(100))  # awareness, engagement, conversions
    target_audience = Column(JSON)
    platforms = Column(JSON)  # List of platforms

    # Scheduling
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    posting_frequency = Column(String(50))  # daily, weekly, custom

    # Budget & Goals
    budget = Column(Float)
    target_reach = Column(Integer)
    target_engagement = Column(Float)

    # Status
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="campaigns")
    posts = relationship("Post", back_populates="campaign")


class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(SQLEnum(Platform))

    # Date
    date = Column(DateTime, nullable=False, index=True)

    # Aggregated metrics
    total_posts = Column(Integer, default=0)
    total_impressions = Column(Integer, default=0)
    total_reach = Column(Integer, default=0)
    total_engagement = Column(Integer, default=0)
    avg_engagement_rate = Column(Float, default=0.0)

    # Growth metrics
    follower_count = Column(Integer)
    follower_growth = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)


class AIUsage(Base):
    __tablename__ = "ai_usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Usage tracking
    generation_type = Column(String(50))  # content, image, email, ad_copy
    model_used = Column(String(100))
    tokens_used = Column(Integer)
    cost = Column(Float)

    # Request details
    request_params = Column(JSON)
    success = Column(Boolean, default=True)
    error_message = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    tier = Column(SQLEnum(SubscriptionTier), nullable=False)
    stripe_subscription_id = Column(String(255))
    stripe_price_id = Column(String(255))

    # Limits
    max_social_accounts = Column(Integer)
    max_ai_generations_monthly = Column(Integer)
    max_image_generations_monthly = Column(Integer)

    # Usage this period
    ai_generations_used = Column(Integer, default=0)
    image_generations_used = Column(Integer, default=0)

    # Billing
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    cancel_at_period_end = Column(Boolean, default=False)

    status = Column(String(50))  # active, canceled, past_due, etc.

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Create all tables
def init_db():
    Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
