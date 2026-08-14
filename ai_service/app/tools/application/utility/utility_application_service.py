import hashlib
import ast
import operator
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

# AST-based safe evaluator: only arithmetic on numbers plus a small allow-list
# of pure math functions. Never falls back to builtin eval()/exec(), so user
# input cannot reach arbitrary Python.
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}
_ALLOWED_MATH = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "log2": math.log2,
    "exp": math.exp,
    "abs": abs,
    "ceil": math.ceil,
    "floor": math.floor,
    "pow": math.pow,
    "min": min,
    "max": max,
}


def _eval_ast(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError("Only numeric constants are allowed")
    if isinstance(node, ast.BinOp):
        op = _BIN_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        try:
            return op(_eval_ast(node.left), _eval_ast(node.right))
        except ZeroDivisionError:
            raise ValueError("Division by zero is not allowed")
    if isinstance(node, ast.UnaryOp):
        op = _UNARY_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return op(_eval_ast(node.operand))
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only math.* functions are allowed")
        fn = _ALLOWED_MATH.get(node.func.id)
        if fn is None:
            raise ValueError(f"Function {node.func.id} not allowed")
        args = [_eval_ast(a) for a in node.args]
        if node.keywords:
            raise ValueError("Keyword arguments are not allowed")
        try:
            return float(fn(*args))
        except TypeError:
            raise ValueError(f"Invalid arguments for {node.func.id}")
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

class UtilityApplicationService(BaseService, IUtilityService):
    async def _on_initialize(self) -> None:
        self._logger.info("Initializing UtilityApplicationService")

    async def calculate(self, schema: CalculatorSchema) -> CalculatorResult:
        try:
            tree = ast.parse(schema.expression, mode="eval")
            result = _eval_ast(tree)
            if not math.isfinite(result):
                raise ValueError("Result is not a finite number")
            return CalculatorResult(result=result)
        except SyntaxError:
            raise ValueError("Invalid mathematical expression")
        except ValueError as e:
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
