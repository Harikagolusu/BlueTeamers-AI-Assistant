import cProfile
import tracemalloc
import time
from typing import Dict, Any
from app.observability.interfaces.i_profiling import IProfiler

class StandardProfiler(IProfiler):
    def __init__(self):
        self._pr = cProfile.Profile()
        self._start_time = 0

    def start(self) -> None:
        tracemalloc.start()
        self._start_time = time.perf_counter()
        self._pr.enable()

    def stop(self) -> Dict[str, Any]:
        self._pr.disable()
        duration = time.perf_counter() - self._start_time
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # NOTE: Dump cProfile stats to string could be done via pstats
        # Stubbing the complex dict mapping for brevity
        return {
            "duration_sec": duration,
            "memory_current_bytes": current,
            "memory_peak_bytes": peak,
            "cpu_profiling_enabled": True
        }
