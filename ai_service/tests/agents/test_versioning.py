import pytest
from app.agents.versioning.compatibility_resolver import CompatibilityResolver

def test_compatibility_resolver():
    resolver = CompatibilityResolver()
    
    # Strict
    assert resolver.check_compatibility("1.0.0", "1.0.0") == True
    assert resolver.check_compatibility("1.0.0", "1.1.0") == False
    
    # Min version
    assert resolver.check_compatibility(">=1.0.0", "1.5.0") == True
    assert resolver.check_compatibility(">=1.0.0", "0.9.0") == False
