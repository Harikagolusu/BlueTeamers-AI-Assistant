import os

def generate_reports():
    output_dir = r"C:\Users\golus\.gemini\antigravity-ide\brain\1834cd97-87ac-487d-8f8c-4d5f0f39422f"
    
    report_hist = """# Execution History Report

## Architecture
The `IExecutionHistoryRepository` interface abstracts persistence. Currently implemented by `InMemoryExecutionHistoryRepository`.

## Append-Only Logging
All transitions defined in `ExecutionState` are persisted to history alongside their metadata and context IDs.
"""

    report_queue = """# Execution Queue Report

## Execution Queues
The `ExecutionScheduler` orchestrates tasks across multiple virtual queues (Priority Queue for standard flows, Dead Letter Queue for terminal failures).
"""

    report_replay = """# Replay System Report

## Overview
The `ExecutionReplayManager` extracts the original invocation payload from `IExecutionHistoryRepository` and explicitly injects it back through the `PlatformAgentOrchestrator` -> `WorkflowBuilder` flow.

## Immutability Guarantee
Replaying a workflow spawns a completely new `trace_id` and `execution_id`, guaranteeing production history is never mutated.
"""

    with open(os.path.join(output_dir, "execution_history_report.md"), "w") as f:
        f.write(report_hist)
    with open(os.path.join(output_dir, "execution_queue_report.md"), "w") as f:
        f.write(report_queue)
    with open(os.path.join(output_dir, "replay_system_report.md"), "w") as f:
        f.write(report_replay)
        
    print("Generated history and replay reports.")

if __name__ == "__main__":
    generate_reports()
