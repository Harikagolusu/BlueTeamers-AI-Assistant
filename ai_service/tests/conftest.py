"""Shared pytest fixtures."""
import pytest

from app.security.rate_limit import _limiter


@pytest.fixture(autouse=True)
def _reset_global_state():
    """Reset in-process limiter state before every test.

    The chat rate limiter is a module-global fixed-window counter. Without a
    reset, requests from one test bleed into the next (all TestClient calls
    share one peer IP), producing spurious 429s later in the suite.
    """
    _limiter.clear()
    yield
    _limiter.clear()