from abc import ABC, abstractmethod
from app.tools.domain.schemas.calculator_schema import CalculatorSchema
from app.tools.domain.results.calculator_result import CalculatorResult
from app.tools.domain.schemas.hash_schema import HashSchema
from app.tools.domain.results.hash_result import HashResult
from app.tools.domain.schemas.time_schema import TimeSchema
from app.tools.domain.results.time_result import TimeResult

class IUtilityService(ABC):
    """
    Application interface for utility orchestration.
    """
    @abstractmethod
    async def calculate(self, schema: CalculatorSchema) -> CalculatorResult:
        pass

    @abstractmethod
    async def hash_data(self, schema: HashSchema) -> HashResult:
        pass

    @abstractmethod
    async def get_time(self, schema: TimeSchema) -> TimeResult:
        pass
