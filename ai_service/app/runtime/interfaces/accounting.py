from abc import ABC, abstractmethod
from app.runtime.models.context import TokenUsage, CostAggregation

class ITokenAccountant(ABC):
    @abstractmethod
    def add_usage(self, usage: TokenUsage) -> None:
        pass
        
    @abstractmethod
    def get_current_usage(self) -> TokenUsage:
        pass

class ICostCalculator(ABC):
    @abstractmethod
    def calculate_cost(self, usage: TokenUsage, provider: str, model: str) -> CostAggregation:
        pass
