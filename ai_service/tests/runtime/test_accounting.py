import pytest
from app.runtime.services.accounting_service import TokenAccountant, ConfigurableCostCalculator
from app.runtime.models.context import TokenUsage
from app.runtime.context_manager import RuntimeContextManager

def test_token_accountant_and_cost_calculator():
    accountant = TokenAccountant()
    calculator = ConfigurableCostCalculator()
    
    with RuntimeContextManager.lifecycle(trace_id="test"):
        accountant.add_usage(TokenUsage(input_tokens=1000, output_tokens=500))
        accountant.add_usage(TokenUsage(input_tokens=500, output_tokens=500))
        
        usage = accountant.get_current_usage()
        assert usage.input_tokens == 1500
        assert usage.output_tokens == 1000
        assert usage.total_tokens == 2500
        
        cost = calculator.calculate_cost(usage, "openai", "gpt-4")
        # gpt-4: input 0.03/1k, output 0.06/1k
        # 1.5 * 0.03 = 0.045
        # 1.0 * 0.06 = 0.06
        # Total = 0.105
        assert round(cost.llm_cost, 4) == 0.105
        
        ctx = RuntimeContextManager.get()
        assert round(ctx.cost.llm_cost, 4) == 0.105
