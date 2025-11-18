from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

from src.ai.content_generator import ContentGenerator
from src.ai.media_generator import MediaGenerator
from src.models.database import get_db

router = APIRouter()


# Request models
class GenerateContentRequest(BaseModel):
    topic: str
    platforms: List[str]
    tone: str = "professional"
    brand_voice: str = "friendly and engaging"
    keywords: Optional[List[str]] = None
    target_audience: Optional[str] = None


class GenerateImageRequest(BaseModel):
    prompt: str
    style: str = "professional"
    aspect_ratio: str = "1:1"
    negative_prompt: Optional[str] = None


class GenerateEmailRequest(BaseModel):
    campaign_type: str
    subject_variants: int = 3
    segment: Optional[str] = None
    product_info: Optional[str] = None
    key_points: Optional[List[str]] = None
    cta: Optional[str] = None


class GenerateAdCopyRequest(BaseModel):
    platform: str
    objective: str
    target_audience: str
    product_name: str
    key_benefits: List[str]
    budget: Optional[str] = None
    variants: int = 3


class OptimizeContentRequest(BaseModel):
    original_content: str
    platform: str
    optimization_goals: List[str]


class GenerateVideoScriptRequest(BaseModel):
    topic: str
    duration: int
    platform: str = "youtube"
    style: str = "educational"


class CreateCarouselRequest(BaseModel):
    slides_content: List[str]
    template: str = "modern"
    brand_colors: Optional[Dict] = None


# Endpoints
@router.post("/generate/social")
async def generate_social_content(request: GenerateContentRequest):
    """Generate AI-powered social media content for multiple platforms"""
    try:
        generator = ContentGenerator()

        result = await generator.generate_social_content(
            topic=request.topic,
            platforms=request.platforms,
            tone=request.tone,
            brand_voice=request.brand_voice,
            keywords=request.keywords,
            target_audience=request.target_audience,
        )

        return {
            "success": True,
            "data": result,
            "generated_at": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/email")
async def generate_email_campaign(request: GenerateEmailRequest):
    """Generate email campaign content"""
    try:
        generator = ContentGenerator()

        result = await generator.generate_email_campaign(
            campaign_type=request.campaign_type,
            subject_variants=request.subject_variants,
            segment=request.segment,
            product_info=request.product_info,
            key_points=request.key_points,
            cta=request.cta,
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/ad-copy")
async def generate_ad_copy(request: GenerateAdCopyRequest):
    """Generate A/B test ad copy variants"""
    try:
        generator = ContentGenerator()

        result = await generator.generate_ad_copy(
            platform=request.platform,
            objective=request.objective,
            target_audience=request.target_audience,
            product_name=request.product_name,
            key_benefits=request.key_benefits,
            budget=request.budget,
            variants=request.variants,
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/image")
async def generate_image(request: GenerateImageRequest):
    """Generate marketing images using AI"""
    try:
        generator = MediaGenerator()

        image_bytes = await generator.generate_image(
            prompt=request.prompt,
            style=request.style,
            aspect_ratio=request.aspect_ratio,
            negative_prompt=request.negative_prompt,
        )

        # In production, upload to S3/CDN and return URL
        import base64

        image_base64 = base64.b64encode(image_bytes).decode()

        return {
            "success": True,
            "data": {
                "image_base64": image_base64,
                "format": "png",
                "generated_at": datetime.utcnow().isoformat(),
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/video-script")
async def generate_video_script(request: GenerateVideoScriptRequest):
    """Generate video script and storyboard"""
    try:
        generator = MediaGenerator()

        result = await generator.generate_video_script(
            topic=request.topic,
            duration=request.duration,
            platform=request.platform,
            style=request.style,
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/carousel")
async def create_carousel(request: CreateCarouselRequest):
    """Create Instagram/LinkedIn carousel images"""
    try:
        generator = MediaGenerator()

        slides = await generator.create_carousel(
            slides_content=request.slides_content,
            template=request.template,
            brand_colors=request.brand_colors,
        )

        # Convert to base64
        import base64

        slides_base64 = [base64.b64encode(slide).decode() for slide in slides]

        return {
            "success": True,
            "data": {"slides": slides_base64, "count": len(slides_base64)},
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize")
async def optimize_content(request: OptimizeContentRequest):
    """Optimize existing content for better performance"""
    try:
        generator = ContentGenerator()

        result = await generator.optimize_content(
            original_content=request.original_content,
            platform=request.platform,
            optimization_goals=request.optimization_goals,
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ideas")
async def generate_content_ideas(
    industry: str,
    target_audience: str,
    content_types: List[str],
    count: int = 10,
    trends: Optional[List[str]] = None,
):
    """Generate content ideas"""
    try:
        generator = ContentGenerator()

        result = await generator.generate_content_ideas(
            industry=industry,
            target_audience=target_audience,
            content_types=content_types,
            count=count,
            trends=trends,
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
