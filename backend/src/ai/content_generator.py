from anthropic import Anthropic
from typing import List, Dict, Optional
import asyncio
from datetime import datetime

from src.config import settings


class ContentGenerator:
    """AI-powered content generation engine"""

    def __init__(self):
        self.anthropic = Anthropic(api_key=settings.anthropic_api_key)
        self.model = "claude-sonnet-4-20250514"

    async def generate_social_content(
        self,
        topic: str,
        platforms: List[str],
        tone: str = "professional",
        brand_voice: str = "friendly and engaging",
        keywords: List[str] = None,
        target_audience: Optional[str] = None,
    ) -> Dict[str, Dict]:
        """Generate platform-optimized social media content

        Args:
            topic: Content topic or theme
            platforms: List of platforms (instagram, twitter, linkedin, facebook, tiktok)
            tone: Content tone (professional, casual, humorous, inspirational)
            brand_voice: Brand voice description
            keywords: SEO keywords to include
            target_audience: Target audience description

        Returns:
            Dict with platform as key and content details as value
        """
        keywords = keywords or []
        platform_specs = {
            "instagram": {
                "max_length": 2200,
                "hashtag_limit": 30,
                "features": "visual-first, stories, reels, carousel",
                "best_practices": "Use emojis, ask questions, create carousel posts"
            },
            "twitter": {
                "max_length": 280,
                "thread_support": True,
                "features": "threads, polls, real-time",
                "best_practices": "Be concise, use trending hashtags, create threads for longer content"
            },
            "linkedin": {
                "max_length": 3000,
                "professional_tone": True,
                "features": "articles, professional network, B2B",
                "best_practices": "Professional tone, industry insights, tag relevant people"
            },
            "facebook": {
                "max_length": 63206,
                "engagement_focus": True,
                "features": "groups, events, live video, marketplace",
                "best_practices": "Ask questions, create polls, use video content"
            },
            "tiktok": {
                "max_length": 150,
                "trend_focus": True,
                "features": "short video, trending sounds, challenges",
                "best_practices": "Use trending sounds, create challenges, hook in first 3 seconds"
            }
        }

        results = {}

        # Generate content for each platform in parallel
        tasks = []
        for platform in platforms:
            if platform not in platform_specs:
                continue
            task = self._generate_platform_content(
                platform, topic, tone, brand_voice, keywords,
                target_audience, platform_specs[platform]
            )
            tasks.append((platform, task))

        # Wait for all generations
        for platform, task in tasks:
            try:
                content = await task
                results[platform] = content
            except Exception as e:
                results[platform] = {
                    "error": str(e),
                    "status": "failed"
                }

        return results

    async def _generate_platform_content(
        self,
        platform: str,
        topic: str,
        tone: str,
        brand_voice: str,
        keywords: List[str],
        target_audience: Optional[str],
        spec: Dict
    ) -> Dict:
        """Generate content for a specific platform"""

        audience_text = f"\nTarget Audience: {target_audience}" if target_audience else ""
        keywords_text = f"\nKeywords to naturally include: {', '.join(keywords)}" if keywords else ""

        prompt = f"""Create highly engaging {platform} content for the following:

Topic: {topic}
Tone: {tone}
Brand Voice: {brand_voice}{audience_text}{keywords_text}

Platform specifications for {platform}:
- Maximum length: {spec.get('max_length', 1000)} characters
- Platform features: {spec.get('features', 'standard')}
- Best practices: {spec.get('best_practices', 'engage audience')}

Requirements:
1. Create compelling, platform-native content that feels authentic to {platform}
2. Include a strong hook in the first sentence
3. Use appropriate emojis that enhance the message (don't overuse)
4. Include a clear Call-to-Action (CTA)
5. Suggest 5-8 optimal hashtags (relevant, mix of popular and niche)
6. Format the content exactly as it would appear on {platform}

Response format:
CONTENT:
[The actual post content here]

HASHTAGS:
[List hashtags separated by spaces]

BEST_TIME_TO_POST:
[Suggest optimal posting time based on platform and audience]

ENGAGEMENT_TIPS:
[2-3 tips to maximize engagement for this specific post]
"""

        # Call Claude API
        message = self.anthropic.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text

        # Parse the response
        parsed = self._parse_content_response(response_text)
        parsed["platform"] = platform
        parsed["generated_at"] = datetime.utcnow().isoformat()
        parsed["model"] = self.model

        return parsed

    def _parse_content_response(self, response: str) -> Dict:
        """Parse structured content from Claude's response"""
        sections = {
            "content": "",
            "hashtags": [],
            "best_time_to_post": "",
            "engagement_tips": []
        }

        current_section = None
        lines = response.split("\n")

        for line in lines:
            line_upper = line.strip().upper()
            if "CONTENT:" in line_upper:
                current_section = "content"
                continue
            elif "HASHTAGS:" in line_upper:
                current_section = "hashtags"
                continue
            elif "BEST_TIME_TO_POST:" in line_upper or "BEST TIME:" in line_upper:
                current_section = "best_time_to_post"
                continue
            elif "ENGAGEMENT_TIPS:" in line_upper or "ENGAGEMENT TIPS:" in line_upper:
                current_section = "engagement_tips"
                continue

            if current_section and line.strip():
                if current_section == "content":
                    sections["content"] += line + "\n"
                elif current_section == "hashtags":
                    # Extract hashtags
                    hashtags = line.strip().split()
                    sections["hashtags"].extend([h.strip() for h in hashtags if h.startswith("#")])
                elif current_section == "best_time_to_post":
                    sections["best_time_to_post"] += line.strip() + " "
                elif current_section == "engagement_tips":
                    if line.strip().startswith(("-", "•", "*")) or line.strip()[0].isdigit():
                        sections["engagement_tips"].append(line.strip())

        # Clean up
        sections["content"] = sections["content"].strip()
        sections["best_time_to_post"] = sections["best_time_to_post"].strip()

        return sections

    async def generate_email_campaign(
        self,
        campaign_type: str,  # newsletter, promotional, onboarding, re-engagement
        subject_variants: int = 3,
        segment: Optional[str] = None,
        product_info: Optional[str] = None,
        key_points: Optional[List[str]] = None,
        cta: Optional[str] = None,
    ) -> Dict:
        """Generate email campaign content with A/B test variants

        Args:
            campaign_type: Type of email campaign
            subject_variants: Number of subject line variants
            segment: Target segment description
            product_info: Product or service information
            key_points: Key points to cover
            cta: Desired call-to-action

        Returns:
            Dict with subject lines, body content, and variants
        """
        key_points = key_points or []
        segment_text = f"\nTarget Segment: {segment}" if segment else ""
        product_text = f"\nProduct/Service: {product_info}" if product_info else ""
        points_text = f"\nKey Points:\n" + "\n".join(f"- {p}" for p in key_points) if key_points else ""
        cta_text = f"\nDesired CTA: {cta}" if cta else ""

        prompt = f"""Create a high-converting {campaign_type} email campaign.

{segment_text}{product_text}{points_text}{cta_text}

Requirements:
1. Generate {subject_variants} different subject line variants for A/B testing
2. Create engaging email body with:
   - Compelling opening that grabs attention
   - Clear value proposition
   - Scannable format with headers and bullet points
   - Strong, clear CTA
   - Personalization placeholders (e.g., {{{{first_name}}}})
3. Suggest preview text (50-100 chars)
4. Provide recommendations for images/visuals
5. Include best practices for this campaign type

Response format:
SUBJECT_LINES:
1. [Subject variant 1]
2. [Subject variant 2]
3. [Subject variant 3]

PREVIEW_TEXT:
[Preview text]

EMAIL_BODY:
[Full email HTML/text content]

IMAGE_SUGGESTIONS:
[Suggested images or visuals]

BEST_PRACTICES:
[Campaign-specific tips]
"""

        message = self.anthropic.messages.create(
            model=self.model,
            max_tokens=3000,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )

        response = message.content[0].text

        return {
            "campaign_type": campaign_type,
            "content": response,
            "generated_at": datetime.utcnow().isoformat(),
            "model": self.model
        }

    async def generate_ad_copy(
        self,
        platform: str,  # google, facebook, instagram, linkedin, twitter
        objective: str,  # awareness, consideration, conversion
        target_audience: str,
        product_name: str,
        key_benefits: List[str],
        budget: Optional[str] = None,
        variants: int = 3
    ) -> List[Dict]:
        """Generate multiple ad copy variants for A/B testing

        Args:
            platform: Advertising platform
            objective: Campaign objective
            target_audience: Detailed audience description
            product_name: Product or service name
            key_benefits: List of key benefits
            budget: Budget range
            variants: Number of variants to generate

        Returns:
            List of ad copy variants with headlines, descriptions, and CTAs
        """
        budget_text = f"\nBudget: {budget}" if budget else ""
        benefits_text = "\n".join(f"- {b}" for b in key_benefits)

        prompt = f"""Create {variants} high-performing ad copy variants for {platform} advertising.

Platform: {platform}
Objective: {objective}
Product: {product_name}
Target Audience: {target_audience}{budget_text}

Key Benefits:
{benefits_text}

For each variant, provide:
1. Headline (attention-grabbing, benefit-driven)
2. Description/Body text
3. Call-to-Action
4. Suggested image/visual concept
5. Why this variant might perform well

Optimize for {platform}'s ad format and {objective} objective.
"""

        message = self.anthropic.messages.create(
            model=self.model,
            max_tokens=2500,
            temperature=0.8,  # Higher temp for creative variety
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "platform": platform,
            "objective": objective,
            "variants": message.content[0].text,
            "generated_at": datetime.utcnow().isoformat(),
            "count": variants
        }

    async def generate_content_ideas(
        self,
        industry: str,
        target_audience: str,
        content_types: List[str],  # blog, video, infographic, podcast, etc.
        count: int = 10,
        trends: Optional[List[str]] = None
    ) -> List[Dict]:
        """Generate content ideas based on industry and trends

        Args:
            industry: Business industry
            target_audience: Target audience description
            content_types: Types of content to generate ideas for
            count: Number of ideas to generate
            trends: Current trends to incorporate

        Returns:
            List of content ideas with titles, descriptions, and formats
        """
        trends_text = f"\nCurrent Trends: {', '.join(trends)}" if trends else ""

        prompt = f"""Generate {count} creative, engaging content ideas for a {industry} business.

Target Audience: {target_audience}
Content Types: {', '.join(content_types)}{trends_text}

For each idea, provide:
1. Catchy title
2. Brief description (2-3 sentences)
3. Content format/type
4. Key takeaways for the audience
5. Estimated engagement potential (High/Medium/Low)
6. Suggested platforms for distribution

Make ideas actionable, trending, and valuable to the target audience.
"""

        message = self.anthropic.messages.create(
            model=self.model,
            max_tokens=3000,
            temperature=0.9,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "industry": industry,
            "ideas": message.content[0].text,
            "generated_at": datetime.utcnow().isoformat(),
            "count": count
        }

    async def optimize_content(
        self,
        original_content: str,
        platform: str,
        optimization_goals: List[str]  # engagement, seo, conversions, reach
    ) -> Dict:
        """Optimize existing content for better performance

        Args:
            original_content: Original content to optimize
            platform: Target platform
            optimization_goals: Goals to optimize for

        Returns:
            Optimized content with explanations
        """
        goals_text = ", ".join(optimization_goals)

        prompt = f"""Optimize the following content for {platform} to improve {goals_text}.

Original Content:
{original_content}

Provide:
1. Optimized version of the content
2. Specific changes made and why
3. Expected improvement in {goals_text}
4. Additional recommendations

Make concrete improvements while maintaining the original message.
"""

        message = self.anthropic.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.5,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "original": original_content,
            "optimized": message.content[0].text,
            "platform": platform,
            "goals": optimization_goals,
            "generated_at": datetime.utcnow().isoformat()
        }
