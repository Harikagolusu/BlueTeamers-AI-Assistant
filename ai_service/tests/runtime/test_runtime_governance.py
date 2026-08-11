import pytest
import asyncio
from app.runtime.services.governance_service import SlidingWindowRateLimiter, DailyQuotaManager

@pytest.mark.asyncio
async def test_rate_limiter():
    limiter = SlidingWindowRateLimiter(requests_per_minute=2)
    user_id = "test_user"
    endpoint = "chat"
    
    assert await limiter.check_limit(user_id, endpoint) is True
    assert await limiter.check_limit(user_id, endpoint) is True
    assert await limiter.check_limit(user_id, endpoint) is False # 3rd request blocked

@pytest.mark.asyncio
async def test_quota_manager():
    manager = DailyQuotaManager(daily_token_limit=100)
    user_id = "test_user"
    
    assert await manager.check_quota(user_id) is True
    
    await manager.increment_usage(user_id, 90)
    assert await manager.check_quota(user_id) is True
    
    await manager.increment_usage(user_id, 15)
    assert await manager.check_quota(user_id) is False
