from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime, timedelta

from src.models.database import get_db, Post, Analytics, Platform
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter()


@router.get("/overview")
async def get_analytics_overview(
    user_id: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    platform: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get analytics overview for a user"""
    try:
        # Default to last 30 days
        if not start_date:
            start = datetime.utcnow() - timedelta(days=30)
        else:
            start = datetime.fromisoformat(start_date)

        if not end_date:
            end = datetime.utcnow()
        else:
            end = datetime.fromisoformat(end_date)

        # Build query
        query = db.query(Post).filter(Post.published_at.between(start, end))

        if platform:
            # Filter by platform through social_account relationship
            query = query.join(Post.social_account).filter(
                Post.social_account.has(platform=platform)
            )

        # Calculate metrics
        posts = query.all()

        total_posts = len(posts)
        total_impressions = sum(p.impressions or 0 for p in posts)
        total_reach = sum(p.reach or 0 for p in posts)
        total_likes = sum(p.likes or 0 for p in posts)
        total_comments = sum(p.comments or 0 for p in posts)
        total_shares = sum(p.shares or 0 for p in posts)
        total_engagement = total_likes + total_comments + total_shares

        avg_engagement_rate = (
            sum(p.engagement_rate or 0 for p in posts) / total_posts
            if total_posts > 0
            else 0
        )

        return {
            "success": True,
            "data": {
                "period": {"start": start.isoformat(), "end": end.isoformat()},
                "summary": {
                    "total_posts": total_posts,
                    "total_impressions": total_impressions,
                    "total_reach": total_reach,
                    "total_engagement": total_engagement,
                    "avg_engagement_rate": round(avg_engagement_rate * 100, 2),
                },
                "breakdown": {
                    "likes": total_likes,
                    "comments": total_comments,
                    "shares": total_shares,
                },
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/platform-performance")
async def get_platform_performance(
    user_id: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get performance metrics by platform"""
    try:
        if not start_date:
            start = datetime.utcnow() - timedelta(days=30)
        else:
            start = datetime.fromisoformat(start_date)

        if not end_date:
            end = datetime.utcnow()
        else:
            end = datetime.fromisoformat(end_date)

        # Query analytics by platform
        analytics = (
            db.query(Analytics)
            .filter(
                Analytics.user_id == user_id, Analytics.date.between(start, end)
            )
            .all()
        )

        # Group by platform
        platform_data = {}

        for record in analytics:
            platform = record.platform.value if record.platform else "unknown"

            if platform not in platform_data:
                platform_data[platform] = {
                    "platform": platform,
                    "posts": 0,
                    "impressions": 0,
                    "reach": 0,
                    "engagement": 0,
                    "avg_engagement_rate": 0,
                }

            platform_data[platform]["posts"] += record.total_posts
            platform_data[platform]["impressions"] += record.total_impressions
            platform_data[platform]["reach"] += record.total_reach
            platform_data[platform]["engagement"] += record.total_engagement

        # Calculate averages
        for platform in platform_data:
            if platform_data[platform]["posts"] > 0:
                platform_data[platform]["avg_engagement_rate"] = round(
                    platform_data[platform]["engagement"]
                    / platform_data[platform]["impressions"]
                    * 100,
                    2,
                )

        return {"success": True, "data": list(platform_data.values())}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/top-posts")
async def get_top_performing_posts(
    user_id: int,
    limit: int = 10,
    metric: str = "engagement_rate",  # engagement_rate, impressions, reach
    platform: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get top performing posts"""
    try:
        query = db.query(Post).filter(Post.published_at.isnot(None))

        if platform:
            query = query.join(Post.social_account).filter(
                Post.social_account.has(platform=platform)
            )

        # Order by metric
        if metric == "engagement_rate":
            query = query.order_by(Post.engagement_rate.desc())
        elif metric == "impressions":
            query = query.order_by(Post.impressions.desc())
        elif metric == "reach":
            query = query.order_by(Post.reach.desc())

        posts = query.limit(limit).all()

        result = []
        for post in posts:
            result.append(
                {
                    "post_id": post.id,
                    "platform": post.social_account.platform.value,
                    "content_preview": post.content.text_content[:100]
                    if post.content.text_content
                    else "",
                    "published_at": post.published_at.isoformat(),
                    "metrics": {
                        "impressions": post.impressions,
                        "reach": post.reach,
                        "likes": post.likes,
                        "comments": post.comments,
                        "shares": post.shares,
                        "engagement_rate": round(post.engagement_rate * 100, 2),
                    },
                }
            )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends")
async def get_performance_trends(
    user_id: int,
    days: int = 30,
    platform: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get performance trends over time"""
    try:
        start_date = datetime.utcnow() - timedelta(days=days)

        query = db.query(Analytics).filter(
            Analytics.user_id == user_id, Analytics.date >= start_date
        )

        if platform:
            query = query.filter(Analytics.platform == platform)

        analytics = query.order_by(Analytics.date).all()

        # Format data for time series
        trends = []
        for record in analytics:
            trends.append(
                {
                    "date": record.date.isoformat(),
                    "posts": record.total_posts,
                    "impressions": record.total_impressions,
                    "reach": record.total_reach,
                    "engagement": record.total_engagement,
                    "engagement_rate": round(record.avg_engagement_rate * 100, 2),
                }
            )

        return {"success": True, "data": trends}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights")
async def get_ai_insights(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Get AI-powered insights and recommendations"""
    try:
        from src.ai.content_generator import ContentGenerator

        # Fetch recent performance data
        start_date = datetime.utcnow() - timedelta(days=30)
        posts = (
            db.query(Post)
            .filter(Post.published_at >= start_date, Post.published_at.isnot(None))
            .all()
        )

        # Analyze patterns
        insights = []

        # Best performing content type
        if posts:
            content_types = {}
            for post in posts:
                ct = post.content.content_type
                if ct not in content_types:
                    content_types[ct] = {
                        "count": 0,
                        "total_engagement": 0,
                        "avg_engagement": 0,
                    }

                content_types[ct]["count"] += 1
                content_types[ct]["total_engagement"] += (
                    post.likes + post.comments + post.shares
                )

            # Calculate averages
            for ct in content_types:
                if content_types[ct]["count"] > 0:
                    content_types[ct]["avg_engagement"] = (
                        content_types[ct]["total_engagement"]
                        / content_types[ct]["count"]
                    )

            # Find best performing
            best_type = max(content_types, key=lambda x: content_types[x]["avg_engagement"])

            insights.append(
                {
                    "type": "content_type",
                    "title": "Best Performing Content Type",
                    "description": f"{best_type.title()} posts generate {round(content_types[best_type]['avg_engagement'])} average engagement",
                    "recommendation": f"Consider creating more {best_type} content to maximize engagement",
                    "priority": "high",
                }
            )

            # Posting frequency insight
            posts_per_week = len(posts) / 4.3  # Approximate weeks in 30 days

            if posts_per_week < 3:
                insights.append(
                    {
                        "type": "frequency",
                        "title": "Posting Frequency",
                        "description": f"You're posting {round(posts_per_week, 1)} times per week",
                        "recommendation": "Increase posting frequency to 5-7 times per week for better reach",
                        "priority": "medium",
                    }
                )

            # Engagement rate insight
            avg_engagement_rate = sum(p.engagement_rate for p in posts) / len(posts)

            if avg_engagement_rate < 0.03:  # Less than 3%
                insights.append(
                    {
                        "type": "engagement",
                        "title": "Engagement Rate Below Average",
                        "description": f"Current engagement rate: {round(avg_engagement_rate * 100, 2)}%",
                        "recommendation": "Use more engaging CTAs, ask questions, and post at optimal times",
                        "priority": "high",
                    }
                )

        return {"success": True, "data": insights}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
