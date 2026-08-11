# Extension Guide: Adding a New Tool

Follow these 6 strict steps to add a new tool to the Enterprise Tool Library. This process guarantees adherence to the Clean Architecture boundaries and automatic test coverage.

## 1. Create Schema and Result (Domain Layer)

Define the input constraints and the output model in the `domain` layer.

```python
# app/tools/domain/schemas/example_schemas.py
from pydantic import Field
from app.tools.domain.schemas.base_schema import BaseSchema

class ExampleSchema(BaseSchema):
    input_text: str = Field(..., max_length=500, description="Input string")

# app/tools/domain/results/example_results.py
from pydantic import Field
from app.tools.domain.results.base_result import BaseResult

class ExampleResult(BaseResult):
    processed_text: str = Field(..., description="The output text")
```

## 2. Add Application Service Method (Application Layer)

Define the orchestration method in the relevant interface, then implement it in the service.

```python
# app/tools/application/interfaces/i_example_service.py
from abc import ABC, abstractmethod

class IExampleService(ABC):
    @abstractmethod
    async def process_example(self, schema: ExampleSchema) -> ExampleResult:
        pass

# app/tools/application/example/example_application_service.py
class ExampleApplicationService(BaseService, IExampleService):
    async def process_example(self, schema: ExampleSchema) -> ExampleResult:
        # Orchestration logic here...
        return ExampleResult(processed_text=schema.input_text.upper())
```

## 3. Implement the Tool (Implementations Layer)

Create the thin entry point decorated with `@tool`.

```python
# app/tools/implementations/example/example_tool.py
from app.tools.discovery.decorators.tool_decorator import tool
from app.tools.domain.base_tool import BaseTool

@tool(
    name="example_tool",
    description="Processes an example string",
    category=ToolCategory.UTILITY
)
class ExampleTool(BaseTool):
    def __init__(self, service: IExampleService):
        super().__init__()
        self._service = service
        
    async def execute(self, request: ToolRequest) -> ToolResponse:
        try:
            schema = ValidationService.validate_schema(ExampleSchema, request.arguments)
            result = await self._service.process_example(schema)
            return ResponseBuilder.success(result)
        except Exception as e:
            return ResponseBuilder.system_error(str(e))
```

## 4. Register Provider (If Needed)

If your tool calls external APIs or databases, create an `IExampleProvider`, build the concrete class, and register it in the corresponding `ProviderFactory`.

## 5. Run Contract Tests

You do not need to write boilerplate tests for your tool. Simply execute the test suite; your new tool will be dynamically discovered and rigorously tested against the enterprise contract automatically.

```powershell
$env:PYTHONPATH="."
pytest tests/tools/contracts/test_tool_contract.py -v
```

Ensure you write specific failure scenario unit tests for your Application Service in `tests/tools/implementations/test_failure_scenarios.py`.
