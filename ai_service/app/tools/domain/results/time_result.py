from pydantic import Field
from app.tools.domain.results.base_result import BaseResult

class TimeResult(BaseResult):
    current_time: str = Field(..., description="ISO 8601 formatted time string")
    timezone: str = Field(..., description="Timezone used")
