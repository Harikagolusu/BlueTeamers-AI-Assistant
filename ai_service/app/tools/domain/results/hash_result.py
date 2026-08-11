from pydantic import Field
from app.tools.domain.results.base_result import BaseResult

class HashResult(BaseResult):
    hash_value: str = Field(..., description="Computed hash")
    algorithm: str = Field(..., description="Algorithm used")
