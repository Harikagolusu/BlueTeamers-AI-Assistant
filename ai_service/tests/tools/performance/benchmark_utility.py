import time
import asyncio
from app.tools.application.utility.utility_application_service import UtilityApplicationService
from app.tools.domain.schemas.calculator_schema import CalculatorSchema

async def benchmark():
    service = UtilityApplicationService()
    await service.initialize()
    schema = CalculatorSchema(expression="100 * 45 / 2 + 5")
    
    start = time.perf_counter()
    for _ in range(1000):
        await service.calculate(schema)
    end = time.perf_counter()
    
    print(f"Benchmark completed 1000 iterations in {(end - start) * 1000:.2f} ms")
    print(f"Average time per execution: {(end - start) * 1000 / 1000:.4f} ms")

if __name__ == "__main__":
    asyncio.run(benchmark())
