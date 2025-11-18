import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta
import pandas as pd

from src.scheduler.auto_scheduler import AutoScheduler, PostStatus


@pytest.fixture
def scheduler():
    return AutoScheduler()


@pytest.fixture
def sample_historical_data():
    """Create sample historical data for testing"""
    dates = pd.date_range(start='2025-01-01', periods=100, freq='H')
    data = pd.DataFrame({
        'posted_at': dates,
        'impressions': [1000 + i * 10 for i in range(100)],
        'likes': [50 + i for i in range(100)],
        'comments': [10 + i // 2 for i in range(100)],
        'shares': [5 + i // 3 for i in range(100)],
    })
    return data


def test_find_optimal_time_with_historical_data(scheduler, sample_historical_data):
    """Test finding optimal time with historical data"""
    optimal_time = scheduler.find_optimal_time(
        platform='instagram',
        historical_data=sample_historical_data
    )

    assert isinstance(optimal_time, datetime)
    assert optimal_time > datetime.now()


def test_find_optimal_time_without_data(scheduler):
    """Test finding optimal time without historical data"""
    optimal_time = scheduler.find_optimal_time(
        platform='linkedin',
        audience_timezone='America/New_York'
    )

    assert isinstance(optimal_time, datetime)
    assert optimal_time > datetime.now()


def test_schedule_post(scheduler):
    """Test scheduling a post"""
    scheduled_time = datetime.now() + timedelta(hours=1)

    task_id = scheduler.schedule_post(
        content_id='test_content_123',
        platform='instagram',
        scheduled_time=scheduled_time,
        user_id='user_456',
        account_id='account_789'
    )

    assert task_id is not None
    assert isinstance(task_id, str)
    assert 'post_test_content_123' in task_id


def test_schedule_campaign(scheduler):
    """Test scheduling a campaign"""
    content_items = [
        {
            'content_id': f'content_{i}',
            'platform': 'instagram',
            'user_id': 'user_123',
            'account_id': 'account_456',
            'timezone': 'UTC'
        }
        for i in range(5)
    ]

    start_date = datetime.now() + timedelta(days=1)

    task_ids = scheduler.schedule_campaign(
        campaign_id='campaign_789',
        content_items=content_items,
        start_date=start_date,
        frequency='daily'
    )

    assert len(task_ids) == 5
    assert all(isinstance(tid, str) for tid in task_ids)


def test_get_schedule_recommendations(scheduler, sample_historical_data):
    """Test getting schedule recommendations"""
    recommendations = scheduler.get_schedule_recommendations(
        platform='instagram',
        content_type='image',
        target_reach=10000,
        historical_data=sample_historical_data
    )

    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    assert all('day_of_week' in rec for rec in recommendations)
    assert all('hour' in rec for rec in recommendations)


def test_cancel_scheduled_post(scheduler):
    """Test canceling a scheduled post"""
    with patch.object(scheduler.celery.control, 'revoke') as mock_revoke:
        result = scheduler.cancel_scheduled_post('task_123')
        assert result is True
        mock_revoke.assert_called_once()
