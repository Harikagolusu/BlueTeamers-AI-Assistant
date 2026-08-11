from pydantic import Field
from app.tools.domain.results.base_result import BaseResult

class CalculatorResult(BaseResult):
    result: float = Field(..., description="Evaluated result")
