from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # Application
    app_name: str = "Money Marketing Tool"
    app_env: str = "development"
    debug: bool = True
    secret_key: str
    api_version: str = "v1"

    # Database
    database_url: str
    database_pool_size: int = 20

    # Redis
    redis_url: str

    # Celery
    celery_broker_url: str
    celery_result_backend: str

    # AI APIs
    anthropic_api_key: str
    openai_api_key: Optional[str] = None
    replicate_api_token: Optional[str] = None

    # Social Media APIs
    meta_app_id: Optional[str] = None
    meta_app_secret: Optional[str] = None
    twitter_api_key: Optional[str] = None
    twitter_api_secret: Optional[str] = None
    twitter_bearer_token: Optional[str] = None
    linkedin_client_id: Optional[str] = None
    linkedin_client_secret: Optional[str] = None

    # Email
    sendgrid_api_key: Optional[str] = None

    # Payment
    stripe_secret_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None

    # Monitoring
    sentry_dsn: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
