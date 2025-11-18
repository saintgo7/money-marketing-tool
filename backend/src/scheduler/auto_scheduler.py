from celery import Celery
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
import pytz
from enum import Enum

from src.config import settings


# Initialize Celery
celery_app = Celery(
    "marketing_scheduler",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes
    task_soft_time_limit=240,  # 4 minutes
)


class PostStatus(str, Enum):
    SCHEDULED = "scheduled"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"


class AutoScheduler:
    """Intelligent scheduling system for optimal content posting"""

    def __init__(self):
        self.celery = celery_app

    def find_optimal_time(
        self,
        platform: str,
        audience_timezone: str = "UTC",
        historical_data: Optional[pd.DataFrame] = None,
        content_type: Optional[str] = None,
    ) -> datetime:
        """Calculate optimal posting time based on historical performance

        Args:
            platform: Social media platform
            audience_timezone: Target audience timezone
            historical_data: DataFrame with past post performance
            content_type: Type of content (text, image, video, carousel)

        Returns:
            Optimal datetime to post
        """

        # Default optimal times by platform (based on industry research)
        default_times = {
            "instagram": {"day": 2, "hour": 11},  # Wednesday 11 AM
            "facebook": {"day": 2, "hour": 13},  # Wednesday 1 PM
            "twitter": {"day": 2, "hour": 9},  # Wednesday 9 AM
            "linkedin": {"day": 1, "hour": 10},  # Tuesday 10 AM
            "tiktok": {"day": 1, "hour": 19},  # Tuesday 7 PM
            "youtube": {"day": 4, "hour": 14},  # Friday 2 PM
            "pinterest": {"day": 5, "hour": 20},  # Saturday 8 PM
        }

        best_day = None
        best_hour = None

        # If we have historical data, analyze it
        if historical_data is not None and not historical_data.empty:
            try:
                # Calculate engagement rate if not present
                if "engagement_rate" not in historical_data.columns:
                    historical_data["engagement_rate"] = (
                        historical_data["likes"]
                        + historical_data["comments"]
                        + historical_data["shares"]
                    ) / historical_data["impressions"]

                # Group by day of week and hour
                historical_data["day_of_week"] = historical_data["posted_at"].dt.dayofweek
                historical_data["hour"] = historical_data["posted_at"].dt.hour

                # Filter by content type if specified
                if content_type and "content_type" in historical_data.columns:
                    historical_data = historical_data[
                        historical_data["content_type"] == content_type
                    ]

                # Find best performing time
                engagement_by_time = (
                    historical_data.groupby(["day_of_week", "hour"])["engagement_rate"]
                    .mean()
                )

                if not engagement_by_time.empty:
                    best_time_idx = engagement_by_time.idxmax()
                    best_day, best_hour = best_time_idx

            except Exception as e:
                print(f"Error analyzing historical data: {e}")

        # Fall back to defaults if no historical data or analysis failed
        if best_day is None or best_hour is None:
            defaults = default_times.get(
                platform.lower(), {"day": 2, "hour": 12}
            )
            best_day = defaults["day"]
            best_hour = defaults["hour"]

        # Calculate next occurrence
        tz = pytz.timezone(audience_timezone)
        now = datetime.now(tz)

        # Start with today at the optimal hour
        target = now.replace(hour=best_hour, minute=0, second=0, microsecond=0)

        # Advance to the optimal day of week
        days_ahead = best_day - target.weekday()
        if days_ahead < 0 or (days_ahead == 0 and target <= now):
            # If optimal day has passed this week, schedule for next week
            days_ahead += 7

        target += timedelta(days=days_ahead)

        # Ensure it's in the future
        while target <= now:
            target += timedelta(days=7)

        return target

    def schedule_post(
        self,
        content_id: str,
        platform: str,
        scheduled_time: datetime,
        user_id: str,
        account_id: str,
    ) -> str:
        """Schedule a post for publication

        Args:
            content_id: ID of the content to publish
            platform: Target platform
            scheduled_time: When to publish
            user_id: User ID
            account_id: Social media account ID

        Returns:
            Task ID
        """
        task = self.celery.send_task(
            "tasks.publish_content",
            args=[content_id, platform, user_id, account_id],
            eta=scheduled_time,
            task_id=f"post_{content_id}_{int(scheduled_time.timestamp())}",
        )

        return task.id

    def schedule_campaign(
        self,
        campaign_id: str,
        content_items: List[Dict],
        start_date: datetime,
        frequency: str = "daily",  # daily, weekly, custom
        optimal_timing: bool = True,
    ) -> List[str]:
        """Schedule multiple posts as part of a campaign

        Args:
            campaign_id: Campaign ID
            content_items: List of content items to schedule
            start_date: Campaign start date
            frequency: Posting frequency
            optimal_timing: Use optimal timing algorithm

        Returns:
            List of task IDs
        """
        task_ids = []
        current_date = start_date

        frequency_delta = {
            "daily": timedelta(days=1),
            "weekly": timedelta(weeks=1),
            "biweekly": timedelta(weeks=2),
            "monthly": timedelta(days=30),
        }

        delta = frequency_delta.get(frequency, timedelta(days=1))

        for item in content_items:
            if optimal_timing:
                # Find optimal time for this specific post
                scheduled_time = self.find_optimal_time(
                    platform=item["platform"],
                    audience_timezone=item.get("timezone", "UTC"),
                    content_type=item.get("content_type"),
                )

                # Ensure it's after current_date
                if scheduled_time < current_date:
                    scheduled_time = current_date
            else:
                scheduled_time = current_date

            task_id = self.schedule_post(
                content_id=item["content_id"],
                platform=item["platform"],
                scheduled_time=scheduled_time,
                user_id=item["user_id"],
                account_id=item["account_id"],
            )

            task_ids.append(task_id)
            current_date += delta

        return task_ids

    def reschedule_post(
        self,
        task_id: str,
        new_time: datetime,
    ) -> str:
        """Reschedule an existing post

        Args:
            task_id: Existing task ID
            new_time: New scheduled time

        Returns:
            New task ID
        """
        # Revoke the old task
        self.celery.control.revoke(task_id, terminate=True)

        # Note: In a real implementation, you'd retrieve the original task details
        # from the database and create a new scheduled task
        # This is a simplified version

        return f"rescheduled_{task_id}"

    def cancel_scheduled_post(self, task_id: str) -> bool:
        """Cancel a scheduled post

        Args:
            task_id: Task ID to cancel

        Returns:
            Success status
        """
        try:
            self.celery.control.revoke(task_id, terminate=True)
            return True
        except Exception as e:
            print(f"Error canceling task {task_id}: {e}")
            return False

    def get_schedule_recommendations(
        self,
        platform: str,
        content_type: str,
        target_reach: int,
        historical_data: Optional[pd.DataFrame] = None,
    ) -> List[Dict]:
        """Get recommended posting schedule for maximum reach

        Args:
            platform: Social media platform
            content_type: Type of content
            target_reach: Desired reach
            historical_data: Historical performance data

        Returns:
            List of recommended posting times with expected reach
        """
        recommendations = []

        # Analyze best performing times
        if historical_data is not None and not historical_data.empty:
            # Group by hour and day
            performance = (
                historical_data.groupby(
                    [
                        historical_data["posted_at"].dt.dayofweek,
                        historical_data["posted_at"].dt.hour,
                    ]
                )
                .agg({"impressions": "mean", "engagement_rate": "mean"})
                .reset_index()
            )

            # Get top 5 times
            top_times = performance.nlargest(5, "impressions")

            for _, row in top_times.iterrows():
                day_names = [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ]

                recommendations.append(
                    {
                        "day_of_week": day_names[int(row["posted_at"])],
                        "hour": int(row["posted_at_1"]),
                        "expected_reach": int(row["impressions"]),
                        "expected_engagement_rate": float(row["engagement_rate"]),
                        "confidence": "high" if len(historical_data) > 50 else "medium",
                    }
                )

        # If no historical data, provide industry defaults
        if not recommendations:
            default_schedules = {
                "instagram": [
                    {"day": "Wednesday", "hour": 11, "reach_multiplier": 1.2},
                    {"day": "Friday", "hour": 10, "reach_multiplier": 1.15},
                    {"day": "Tuesday", "hour": 14, "reach_multiplier": 1.1},
                ],
                "linkedin": [
                    {"day": "Tuesday", "hour": 10, "reach_multiplier": 1.3},
                    {"day": "Wednesday", "hour": 12, "reach_multiplier": 1.25},
                    {"day": "Thursday", "hour": 9, "reach_multiplier": 1.2},
                ],
                "twitter": [
                    {"day": "Wednesday", "hour": 9, "reach_multiplier": 1.2},
                    {"day": "Friday", "hour": 12, "reach_multiplier": 1.15},
                    {"day": "Monday", "hour": 15, "reach_multiplier": 1.1},
                ],
            }

            schedule = default_schedules.get(platform.lower(), [])

            for slot in schedule:
                recommendations.append(
                    {
                        "day_of_week": slot["day"],
                        "hour": slot["hour"],
                        "expected_reach": int(target_reach * slot["reach_multiplier"]),
                        "expected_engagement_rate": 0.035,  # 3.5% industry average
                        "confidence": "low",
                    }
                )

        return recommendations


# Celery tasks
@celery_app.task(name="tasks.publish_content")
def publish_content_task(content_id: str, platform: str, user_id: str, account_id: str):
    """Celery task to publish content to social media"""
    from src.publishers.social_publisher import SocialPublisher

    publisher = SocialPublisher()

    try:
        result = publisher.publish(
            content_id=content_id,
            platform=platform,
            user_id=user_id,
            account_id=account_id,
        )
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@celery_app.task(name="tasks.analyze_performance")
def analyze_performance_task(post_id: str, platform: str):
    """Celery task to analyze post performance"""
    # This would fetch metrics from the platform and update the database
    return {"post_id": post_id, "status": "analyzed"}


@celery_app.task(name="tasks.generate_report")
def generate_report_task(user_id: str, date_range: Dict):
    """Celery task to generate performance reports"""
    return {"user_id": user_id, "status": "report_generated"}
