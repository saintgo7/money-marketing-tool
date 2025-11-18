import pytest
from unittest.mock import Mock, patch
from src.utils.email import EmailService


@pytest.fixture
def email_service():
    return EmailService()


def test_send_welcome_email(email_service):
    """Test sending welcome email"""
    with patch.object(email_service, 'send_email') as mock_send:
        mock_send.return_value = True

        result = email_service.send_welcome_email(
            to_email='test@example.com',
            name='Test User'
        )

        assert result is True
        mock_send.assert_called_once()
        call_args = mock_send.call_args
        assert 'test@example.com' in str(call_args)
        assert '환영합니다' in str(call_args)


def test_send_post_published_notification(email_service):
    """Test sending post published notification"""
    with patch.object(email_service, 'send_email') as mock_send:
        mock_send.return_value = True

        result = email_service.send_post_published_notification(
            to_email='test@example.com',
            platform='Instagram',
            content_preview='Test post content'
        )

        assert result is True
        assert mock_send.called


def test_send_weekly_report(email_service):
    """Test sending weekly report"""
    stats = {
        'posts': 10,
        'reach': '50K',
        'engagement': '2K',
        'engagement_rate': 4.2
    }

    with patch.object(email_service, 'send_email') as mock_send:
        mock_send.return_value = True

        result = email_service.send_weekly_report(
            to_email='test@example.com',
            name='Test User',
            stats=stats
        )

        assert result is True
        assert mock_send.called


def test_send_password_reset(email_service):
    """Test sending password reset email"""
    with patch.object(email_service, 'send_email') as mock_send:
        mock_send.return_value = True

        result = email_service.send_password_reset(
            to_email='test@example.com',
            reset_token='test_token_123'
        )

        assert result is True
        call_args = mock_send.call_args
        assert 'test_token_123' in str(call_args)
