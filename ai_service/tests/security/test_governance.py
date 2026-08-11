import pytest
from app.security.governance.quotas import QuotaManager
from app.security.governance.budgets import BudgetManager

def test_governance_quotas():
    quotas = QuotaManager()
    quotas.set_quota("tenant-1", "tokens", 1000)
    
    assert quotas.check_quota("tenant-1", "tokens", 500) == True
    quotas.consume_quota("tenant-1", "tokens", 500)
    
    assert quotas.check_quota("tenant-1", "tokens", 600) == False
    
    with pytest.raises(ValueError):
        quotas.consume_quota("tenant-1", "tokens", 600)

def test_governance_budgets():
    budgets = BudgetManager()
    budgets.set_budget("tenant-1", 50.0)
    
    budgets.consume_budget("tenant-1", 10.0)
    assert budgets.check_budget("tenant-1", 45.0) == False
