import os

def generate_reports():
    output_dir = r"C:\Users\golus\.gemini\antigravity-ide\brain\1834cd97-87ac-487d-8f8c-4d5f0f39422f"
    
    report2 = """# Execution State Machine Design

## Overview
The `ExecutionState` enumeration has been extended in `app/platform/platform_agent_orchestrator/models.py`.

## Supported States
- **PENDING** (Legacy)
- **CREATED**: Execution request instantiated.
- **READY**: Execution validated and ready for scheduler.
- **QUEUED**: Execution enqueued in `ExecutionScheduler`.
- **RUNNING**: Execution is actively being processed by a worker.
- **WAITING**: Execution is blocked on a dependency or asynchronous tool.
- **RETRYING**: Execution encountered a transient failure and is being retried.
- **PARTIAL_SUCCESS**: Execution completed with some failed sub-tasks.
- **COMPLETED**: Execution succeeded fully.
- **FAILED**: Execution encountered a terminal failure.
- **CANCELLED**: Execution was explicitly cancelled.
- **SKIPPED**: Execution was bypassed (e.g. cache hit).

## Integration
This state machine is used across all `ExecutionContext` instances and tracked by the `ExecutionHistoryRepository`.
"""
    with open(os.path.join(output_dir, "execution_state_machine_design.md"), "w") as f:
        f.write(report2)
        
    print("Generated execution state machine design.")

if __name__ == "__main__":
    generate_reports()
