from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

from src.scheduler.auto_scheduler import AutoScheduler
from src.models.database import get_db

router = APIRouter()


# Request models
class SchedulePostRequest(BaseModel):
    content_id: str
    platform: str
    user_id: str
    account_id: str
    scheduled_time: Optional[datetime] = None
    use_optimal_timing: bool = True
    audience_timezone: str = "UTC"


class ScheduleCampaignRequest(BaseModel):
    campaign_id: str
    content_items: List[Dict]
    start_date: datetime
    frequency: str = "daily"
    optimal_timing: bool = True


class RescheduleRequest(BaseModel):
    task_id: str
    new_time: datetime


# Endpoints
@router.post("/schedule/post")
async def schedule_post(request: SchedulePostRequest):
    """Schedule a single post"""
    try:
        scheduler = AutoScheduler()

        if request.use_optimal_timing and not request.scheduled_time:
            # Find optimal time
            optimal_time = scheduler.find_optimal_time(
                platform=request.platform,
                audience_timezone=request.audience_timezone,
            )
            scheduled_time = optimal_time
        else:
            scheduled_time = request.scheduled_time or datetime.utcnow()

        task_id = scheduler.schedule_post(
            content_id=request.content_id,
            platform=request.platform,
            scheduled_time=scheduled_time,
            user_id=request.user_id,
            account_id=request.account_id,
        )

        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "scheduled_time": scheduled_time.isoformat(),
                "platform": request.platform,
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/schedule/campaign")
async def schedule_campaign(request: ScheduleCampaignRequest):
    """Schedule multiple posts as a campaign"""
    try:
        scheduler = AutoScheduler()

        task_ids = scheduler.schedule_campaign(
            campaign_id=request.campaign_id,
            content_items=request.content_items,
            start_date=request.start_date,
            frequency=request.frequency,
            optimal_timing=request.optimal_timing,
        )

        return {
            "success": True,
            "data": {
                "campaign_id": request.campaign_id,
                "scheduled_posts": len(task_ids),
                "task_ids": task_ids,
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reschedule")
async def reschedule_post(request: RescheduleRequest):
    """Reschedule an existing post"""
    try:
        scheduler = AutoScheduler()

        new_task_id = scheduler.reschedule_post(
            task_id=request.task_id, new_time=request.new_time
        )

        return {
            "success": True,
            "data": {
                "old_task_id": request.task_id,
                "new_task_id": new_task_id,
                "new_scheduled_time": request.new_time.isoformat(),
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/cancel/{task_id}")
async def cancel_scheduled_post(task_id: str):
    """Cancel a scheduled post"""
    try:
        scheduler = AutoScheduler()

        success = scheduler.cancel_scheduled_post(task_id)

        if success:
            return {"success": True, "message": "Post canceled successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to cancel post")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommendations")
async def get_schedule_recommendations(
    platform: str,
    content_type: str,
    target_reach: int = 10000,
):
    """Get recommended posting schedule"""
    try:
        scheduler = AutoScheduler()

        recommendations = scheduler.get_schedule_recommendations(
            platform=platform, content_type=content_type, target_reach=target_reach
        )

        return {"success": True, "data": recommendations}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/optimal-time")
async def get_optimal_time(
    platform: str, audience_timezone: str = "UTC", content_type: Optional[str] = None
):
    """Get optimal posting time for a platform"""
    try:
        scheduler = AutoScheduler()

        optimal_time = scheduler.find_optimal_time(
            platform=platform,
            audience_timezone=audience_timezone,
            content_type=content_type,
        )

        return {
            "success": True,
            "data": {
                "platform": platform,
                "optimal_time": optimal_time.isoformat(),
                "timezone": audience_timezone,
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
