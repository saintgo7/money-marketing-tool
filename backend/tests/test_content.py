import pytest
from unittest.mock import Mock, patch
from src.ai.content_generator import ContentGenerator


@pytest.mark.asyncio
async def test_generate_social_content():
    """Test social content generation"""
    generator = ContentGenerator()

    # Mock the Anthropic API call
    with patch.object(generator.anthropic.messages, 'create') as mock_create:
        mock_create.return_value = Mock(
            content=[Mock(text="Test content\n\nHASHTAGS:\n#test #marketing")]
        )

        result = await generator.generate_social_content(
            topic="Marketing tips",
            platforms=["instagram"],
            tone="professional",
            brand_voice="helpful",
        )

        assert "instagram" in result
        assert "content" in result["instagram"]


@pytest.mark.asyncio
async def test_generate_email_campaign():
    """Test email campaign generation"""
    generator = ContentGenerator()

    with patch.object(generator.anthropic.messages, 'create') as mock_create:
        mock_create.return_value = Mock(
            content=[Mock(text="Email content")]
        )

        result = await generator.generate_email_campaign(
            campaign_type="promotional",
            subject_variants=3,
        )

        assert result["campaign_type"] == "promotional"
        assert "content" in result
