import pytest
from unittest.mock import AsyncMock, MagicMock
from app.security.middleware.pipeline import SecurityMiddlewarePipeline
from app.security.context.context_provider import ContextProvider
from app.security.context.security_context import SecurityContext

class MockRequest:
    def __init__(self, token=None, req_perm=None):
        self.token = token
        self.required_permission = req_perm

@pytest.mark.asyncio
async def test_middleware_pipeline():
    auth = MagicMock()
    auth.validate_request.return_value = {"principal": "user", "claims": {"roles": ["user"]}}
    
    ctx_provider = ContextProvider()
    
    authz = MagicMock()
    authz.authorize.return_value = True
    
    pep = MagicMock()
    gov = MagicMock()
    
    pipeline = SecurityMiddlewarePipeline(auth, ctx_provider, authz, pep, gov)
    
    req = MockRequest(token="jwt.token", req_perm="read")
    
    async def next_handler(r):
        assert ctx_provider.get_context().principal == "user"
        return "SUCCESS"
        
    res = await pipeline.execute(req, next_handler)
    assert res == "SUCCESS"
    
    authz.authorize.assert_called_once()
    pep.enforce.assert_called_once()
    gov.enforce_governance.assert_called_once()
