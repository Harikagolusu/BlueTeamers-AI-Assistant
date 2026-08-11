import asyncio
from app.observability.interfaces.i_logging import ILogger, ILogFormatter, ILogSink
from app.observability.context.context_provider import ObservabilityContextProvider

class ObservabilityLogger(ILogger):
    def __init__(self, formatter: ILogFormatter, sink: ILogSink, context_provider: ObservabilityContextProvider):
        self._formatter = formatter
        self._sink = sink
        self._context_provider = context_provider

    def _log(self, level: str, message: str, **kwargs) -> None:
        ctx = self._context_provider.get_context()
        log_ctx = {
            "correlation_id": ctx.correlation_id,
            "trace_id": ctx.trace_id,
            "tenant": ctx.tenant,
            "user": ctx.user,
            "metadata": kwargs
        }
        formatted = self._formatter.format(level, message, log_ctx)
        
        # Fire and forget async log write
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._sink.write(formatted))
        except RuntimeError:
            # If no event loop (e.g. sync contexts or tests), fallback to sync run
            asyncio.run(self._sink.write(formatted))

    def trace(self, message: str, **kwargs) -> None: self._log("TRACE", message, **kwargs)
    def debug(self, message: str, **kwargs) -> None: self._log("DEBUG", message, **kwargs)
    def info(self, message: str, **kwargs) -> None: self._log("INFO", message, **kwargs)
    def warning(self, message: str, **kwargs) -> None: self._log("WARNING", message, **kwargs)
    def error(self, message: str, **kwargs) -> None: self._log("ERROR", message, **kwargs)
    def critical(self, message: str, **kwargs) -> None: self._log("CRITICAL", message, **kwargs)
