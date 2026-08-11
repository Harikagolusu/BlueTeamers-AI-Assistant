from app.runtime.interfaces.accounting import ITokenAccountant, ICostCalculator
from app.runtime.models.context import TokenUsage, CostAggregation
from app.runtime.context_manager import RuntimeContextManager

class TokenAccountant(ITokenAccountant):
    def add_usage(self, usage: TokenUsage) -> None:
        try:
            ctx = RuntimeContextManager.get()
            current = ctx.token_usage
            new_usage = TokenUsage(
                input_tokens=current.input_tokens + usage.input_tokens,
                output_tokens=current.output_tokens + usage.output_tokens,
                cached_tokens=current.cached_tokens + usage.cached_tokens,
                embedding_tokens=current.embedding_tokens + usage.embedding_tokens,
                tool_tokens=current.tool_tokens + usage.tool_tokens
            )
            RuntimeContextManager.update(token_usage=new_usage)
        except LookupError:
            pass

    def get_current_usage(self) -> TokenUsage:
        try:
            return RuntimeContextManager.get().token_usage
        except LookupError:
            return TokenUsage()

class ConfigurableCostCalculator(ICostCalculator):
    def __init__(self):
        # Configurable pricing per 1k tokens
        self.pricing = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
            "text-embedding-ada-002": {"input": 0.0001, "output": 0.0}
        }
        
    def calculate_cost(self, usage: TokenUsage, provider: str, model: str) -> CostAggregation:
        rates = self.pricing.get(model, {"input": 0.0, "output": 0.0})
        llm_cost = (usage.input_tokens / 1000.0 * rates["input"]) + (usage.output_tokens / 1000.0 * rates["output"])
        embedding_cost = (usage.embedding_tokens / 1000.0 * self.pricing.get("text-embedding-ada-002")["input"])
        
        cost = CostAggregation(
            llm_cost=llm_cost,
            embedding_cost=embedding_cost,
            tool_cost=0.0
        )
        
        try:
            ctx = RuntimeContextManager.get()
            current = ctx.cost
            new_cost = CostAggregation(
                llm_cost=current.llm_cost + cost.llm_cost,
                embedding_cost=current.embedding_cost + cost.embedding_cost,
                tool_cost=current.tool_cost + cost.tool_cost
            )
            RuntimeContextManager.update(cost=new_cost)
        except LookupError:
            pass
            
        return cost

class RuntimeAccountingService:
    """Facade for tracking tokens and costs."""
    def __init__(self, accountant: ITokenAccountant, cost_calculator: ICostCalculator):
        self.accountant = accountant
        self.cost_calculator = cost_calculator
