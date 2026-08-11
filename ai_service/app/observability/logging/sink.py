import asyncio
from app.observability.interfaces.i_logging import ILogSink
import sys

class AsyncStdoutSink(ILogSink):
    async def write(self, formatted_log: str) -> None:
        # Offload IO to event loop without blocking CPU
        await asyncio.to_thread(self._sync_write, formatted_log)

    def _sync_write(self, line: str):
        sys.stdout.write(line + "\n")
        sys.stdout.flush()
