import pytest
from app.observability.profiling.profiler import StandardProfiler
import time

def test_standard_profiler():
    profiler = StandardProfiler()
    profiler.start()
    time.sleep(0.01) # Simulate work
    stats = profiler.stop()
    
    assert "duration_sec" in stats
    assert stats["duration_sec"] > 0
    assert "memory_current_bytes" in stats
