import httpx
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from typing import List, Dict, Optional
import base64
import replicate

from src.config import settings


class MediaGenerator:
    """AI-powered media generation for marketing content"""

    def __init__(self):
        self.replicate_client = replicate if settings.replicate_api_token else None

    async def generate_image(
        self,
        prompt: str,
        style: str = "professional",
        aspect_ratio: str = "1:1",
        negative_prompt: Optional[str] = None,
    ) -> bytes:
        """Generate marketing images using Stable Diffusion XL

        Args:
            prompt: Image description
            style: Visual style (professional, minimalist, bold, creative, etc.)
            aspect_ratio: Image ratio (1:1, 16:9, 4:5, 9:16)
            negative_prompt: What to avoid in the image

        Returns:
            Image bytes
        """
        if not self.replicate_client or not settings.replicate_api_token:
            raise ValueError("Replicate API token not configured")

        # Map aspect ratios to dimensions
        dimensions = {
            "1:1": "1024x1024",
            "16:9": "1344x768",
            "4:5": "896x1088",
            "9:16": "768x1344",
            "3:2": "1152x832",
        }

        size = dimensions.get(aspect_ratio, "1024x1024")

        # Enhance prompt with style
        style_prompts = {
            "professional": "professional photography, high quality, sharp focus, studio lighting",
            "minimalist": "minimalist design, clean, simple, modern aesthetic",
            "bold": "bold colors, high contrast, eye-catching, dramatic",
            "creative": "artistic, creative, unique perspective, innovative",
            "vintage": "vintage style, retro aesthetic, nostalgic feeling",
            "modern": "modern design, sleek, contemporary, cutting-edge",
        }

        style_enhancement = style_prompts.get(style, "professional, high quality")
        enhanced_prompt = f"{prompt}, {style_enhancement}, 4K, detailed"

        # Default negative prompt
        default_negative = "low quality, blurry, pixelated, watermark, text, logo, amateur"
        final_negative = f"{default_negative}, {negative_prompt}" if negative_prompt else default_negative

        try:
            # Use SDXL via Replicate
            output = replicate.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={
                    "prompt": enhanced_prompt,
                    "negative_prompt": final_negative,
                    "width": int(size.split("x")[0]),
                    "height": int(size.split("x")[1]),
                    "num_outputs": 1,
                    "scheduler": "K_EULER",
                    "num_inference_steps": 50,
                    "guidance_scale": 7.5,
                }
            )

            # Download the generated image
            if output and len(output) > 0:
                async with httpx.AsyncClient() as client:
                    response = await client.get(output[0])
                    return response.content
            else:
                raise Exception("No image generated")

        except Exception as e:
            raise Exception(f"Image generation failed: {str(e)}")

    async def generate_video_script(
        self,
        topic: str,
        duration: int,  # in seconds
        platform: str = "youtube",
        style: str = "educational"
    ) -> Dict:
        """Generate video script and storyboard

        Args:
            topic: Video topic
            duration: Target duration in seconds
            platform: Target platform (youtube, tiktok, instagram, etc.)
            style: Video style (educational, entertaining, promotional)

        Returns:
            Dict with script, scenes, and production notes
        """
        from anthropic import Anthropic

        client = Anthropic(api_key=settings.anthropic_api_key)

        prompt = f"""Create a detailed video script for a {duration}-second {style} video about: {topic}

Platform: {platform}
Duration: {duration} seconds

Provide:
1. Hook (first 3-5 seconds) - Must grab attention immediately
2. Scene-by-scene breakdown with:
   - Timestamp
   - Visual description
   - Voiceover/dialogue
   - Text overlays
   - Background music suggestions
3. Call-to-action
4. Production notes and tips
5. Suggested B-roll footage

Format for maximum engagement on {platform}.
"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "topic": topic,
            "duration": duration,
            "platform": platform,
            "script": message.content[0].text,
        }

    async def create_carousel(
        self,
        slides_content: List[str],
        template: str = "modern",
        brand_colors: Optional[Dict] = None,
    ) -> List[bytes]:
        """Create Instagram/LinkedIn carousel images

        Args:
            slides_content: List of text content for each slide
            template: Visual template style
            brand_colors: Dict with 'primary' and 'secondary' color hex codes

        Returns:
            List of image bytes for each slide
        """
        brand_colors = brand_colors or {
            "primary": "#4F46E5",  # Indigo
            "secondary": "#EC4899",  # Pink
            "background": "#FFFFFF",
            "text": "#1F2937",
        }

        slides = []

        for idx, content in enumerate(slides_content, 1):
            slide_image = await self._create_slide(
                content=content,
                slide_number=idx,
                total_slides=len(slides_content),
                template=template,
                colors=brand_colors,
            )
            slides.append(slide_image)

        return slides

    async def _create_slide(
        self,
        content: str,
        slide_number: int,
        total_slides: int,
        template: str,
        colors: Dict,
    ) -> bytes:
        """Create a single carousel slide"""

        # Create image (Instagram carousel size: 1080x1080)
        width, height = 1080, 1080
        img = Image.new("RGB", (width, height), colors["background"])
        draw = ImageDraw.Draw(img)

        # Add decorative elements based on template
        if template == "modern":
            # Add gradient or accent shapes
            draw.rectangle([(0, 0), (width, 100)], fill=colors["primary"])

        # Add content text (simplified - in production, use proper text wrapping)
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Add slide content
        text_y = 200
        # Wrap text (simplified version)
        max_chars_per_line = 25
        words = content.split()
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            if len(" ".join(current_line)) > max_chars_per_line:
                lines.append(" ".join(current_line[:-1]))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))

        for line in lines[:8]:  # Max 8 lines
            bbox = draw.textbbox((0, 0), line, font=font_small)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, text_y), line, fill=colors["text"], font=font_small)
            text_y += 60

        # Add slide number
        slide_text = f"{slide_number}/{total_slides}"
        bbox = draw.textbbox((0, 0), slide_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        draw.text(
            ((width - text_width) // 2, height - 80),
            slide_text,
            fill=colors["primary"],
            font=font_small
        )

        # Convert to bytes
        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        return img_bytes.getvalue()

    async def create_thumbnail(
        self,
        title: str,
        background_image: Optional[bytes] = None,
        style: str = "youtube"
    ) -> bytes:
        """Create video thumbnail

        Args:
            title: Video title text
            background_image: Optional background image
            style: Thumbnail style (youtube, tiktok, etc.)

        Returns:
            Thumbnail image bytes
        """
        # YouTube thumbnail size: 1280x720
        width, height = 1280, 720

        if background_image:
            img = Image.open(BytesIO(background_image))
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            # Darken for text readability
            img = img.point(lambda p: p * 0.6)
        else:
            # Create gradient background
            img = Image.new("RGB", (width, height), "#1F2937")

        draw = ImageDraw.Draw(img)

        # Add title text
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        except:
            font = ImageFont.load_default()

        # Wrap title
        max_chars = 20
        words = title.split()
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            if len(" ".join(current_line)) > max_chars:
                lines.append(" ".join(current_line[:-1]))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))

        # Center text
        text_y = height // 2 - (len(lines) * 40)
        for line in lines[:3]:  # Max 3 lines
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2

            # Add text shadow
            draw.text((x + 3, text_y + 3), line, fill="#000000", font=font)
            # Add main text
            draw.text((x, text_y), line, fill="#FFFFFF", font=font)

            text_y += 90

        # Convert to bytes
        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG", quality=95)
        return img_bytes.getvalue()

    async def generate_logo_variations(
        self,
        company_name: str,
        industry: str,
        style_preferences: List[str]
    ) -> List[str]:
        """Generate logo design prompts for various styles

        Args:
            company_name: Company name
            industry: Business industry
            style_preferences: List of style preferences

        Returns:
            List of detailed prompts for logo generation
        """
        prompts = []

        styles = {
            "modern": "clean lines, minimalist, contemporary, geometric shapes",
            "professional": "corporate, trustworthy, established, sophisticated",
            "playful": "fun, energetic, vibrant colors, dynamic shapes",
            "elegant": "refined, luxurious, premium, timeless",
            "tech": "innovative, digital, futuristic, cutting-edge",
        }

        for style in style_preferences:
            style_desc = styles.get(style, "modern professional")

            prompt = f"""Professional logo design for '{company_name}', a {industry} company.
Style: {style_desc}
Requirements: vector-style, clean, scalable, memorable, unique
Colors: corporate colors appropriate for {industry}
Format: logo mark with text, suitable for business cards and websites
Professional graphic design, award-winning, trending on Dribbble"""

            prompts.append(prompt)

        return prompts
