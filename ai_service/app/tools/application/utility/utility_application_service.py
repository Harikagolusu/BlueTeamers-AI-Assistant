import hashlib
from datetime import datetime
try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo
import math
from app.tools.application.interfaces.i_utility_service import IUtilityService
from app.tools.infrastructure.base.base_service import BaseService
from app.tools.domain.schemas.calculator_schema import CalculatorSchema
from app.tools.domain.results.calculator_result import CalculatorResult
from app.tools.domain.schemas.hash_schema import HashSchema
from app.tools.domain.results.hash_result import HashResult
from app.tools.domain.schemas.time_schema import TimeSchema
from app.tools.domain.results.time_result import TimeResult

class UtilityApplicationService(BaseService, IUtilityService):
    async def _on_initialize(self) -> None:
        self._logger.info("Initializing UtilityApplicationService")

    async def calculate(self, schema: CalculatorSchema) -> CalculatorResult:
        try:
            allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
            code = compile(schema.expression, "<string>", "eval")
            for name in code.co_names:
                if name not in allowed_names:
                    raise NameError(f"Use of {name} not allowed")
            result = eval(code, {"__builtins__": {}}, allowed_names)
            return CalculatorResult(result=float(result))
        except Exception as e:
            raise ValueError(f"Invalid mathematical expression: {e}")

    async def hash_data(self, schema: HashSchema) -> HashResult:
        algo = schema.algorithm.lower()
        if algo not in hashlib.algorithms_available:
            raise ValueError(f"Algorithm {algo} not supported.")
        h = hashlib.new(algo)
        h.update(schema.data.encode('utf-8'))
        return HashResult(hash_value=h.hexdigest(), algorithm=algo)

    async def get_time(self, schema: TimeSchema) -> TimeResult:
        try:
            tz = zoneinfo.ZoneInfo(schema.timezone)
        except zoneinfo.ZoneInfoNotFoundError:
            raise ValueError(f"Unknown timezone: {schema.timezone}")
        
        current_time = datetime.now(tz).isoformat()
        return TimeResult(current_time=current_time, timezone=schema.timezone)
