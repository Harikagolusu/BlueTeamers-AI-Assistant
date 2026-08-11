import uuid
import asyncio
from typing import Optional
from app.observability.interfaces.i_tracing import ITracer, ISpan, ITraceExporter
from app.observability.context.context_provider import ObservabilityContextProvider
from app.observability.tracing.spans import LocalSpan
from app.observability.tracing.sampling import ISampler

class ObservabilityTracer(ITracer):
    def __init__(
        self, 
        context_provider: ObservabilityContextProvider, 
        exporter: ITraceExporter,
        sampler: ISampler
    ):
        self._context_provider = context_provider
        self._exporter = exporter
        self._sampler = sampler

    def start_span(self, name: str, parent_id: Optional[str] = None) -> ISpan:
        ctx = self._context_provider.get_context()
        span_id = str(uuid.uuid4())
        
        sampled = self._sampler.should_sample(ctx.trace_id)
        
        def on_span_end(span):
            if sampled:
                # Dispatch async trace export
                try:
                    loop = asyncio.get_running_loop()
                    loop.create_task(self._exporter.export([span]))
                except RuntimeError:
                    asyncio.run(self._exporter.export([span]))

        return LocalSpan(
            name=name,
            trace_id=ctx.trace_id,
            span_id=span_id,
            parent_id=parent_id or ctx.parent_span_id,
            on_end=on_span_end
        )
