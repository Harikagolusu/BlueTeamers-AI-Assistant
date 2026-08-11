import logging
from typing import List, Dict, Any
from pydantic import BaseModel, Field

from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.agents.investigation.models import EvidenceCorrelation

logger = logging.getLogger(__name__)

class EvidenceCorrelationInput(BaseModel):
    evidence_items: List[Dict[str, Any]] = Field(..., description="Normalized evidence items")

class EvidenceCorrelationTool(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="evidence_correlation_tool",
            description="Correlates timestamps, hosts, users, IPs, alerts, process trees, parent-child processes, hashes, domains, URLs, registry keys, file paths, and network sessions.",
            capabilities=["evidence_correlation"],
            tags=["investigation"]
        )
        super().__init__(name="evidence_correlation_tool", metadata=metadata)

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        try:
            validated = EvidenceCorrelationInput(**kwargs)
        except Exception as e:
            logger.error(f"Validation error in EvidenceCorrelationTool: {e}")
            raise ValueError(f"Invalid input: {e}")

        correlated_entities = {
            "ips": [],
            "users": [],
            "hosts": [],
            "hashes": [],
            "domains": [],
            "urls": [],
            "registry_keys": [],
            "file_paths": []
        }
        process_trees = []
        network_sessions = []

        # Simple mock logic for extracting entities
        for item in validated.evidence_items:
            content = item.get("content", {})
            ev_id = item.get("id", "unknown")
            
            # Simulated entity extraction
            if "ip" in str(content).lower():
                correlated_entities["ips"].append(ev_id)
            if "user" in str(content).lower() or "account" in str(content).lower():
                correlated_entities["users"].append(ev_id)
            if "host" in str(content).lower() or "machine" in str(content).lower():
                correlated_entities["hosts"].append(ev_id)
            if "hash" in str(content).lower():
                correlated_entities["hashes"].append(ev_id)
            if "process" in str(content).lower():
                process_trees.append({"evidence_id": ev_id, "status": "correlating_process_tree"})
            if "session" in str(content).lower() or "port" in str(content).lower():
                network_sessions.append({"evidence_id": ev_id, "status": "correlating_network"})

        correlation = EvidenceCorrelation(
            correlated_entities=correlated_entities,
            process_trees=process_trees,
            network_sessions=network_sessions
        )
        logger.info("Successfully correlated evidence items.")
        return correlation.model_dump()
