import logging
import uuid
from typing import List, Dict, Any
from pydantic import BaseModel, Field

from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.agents.investigation.models import Evidence, EvidenceCollection

logger = logging.getLogger(__name__)

class EvidenceCollectionInput(BaseModel):
    raw_evidence: List[Dict[str, Any]] = Field(..., description="List of raw evidence dictionaries")

class EvidenceCollectionTool(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="evidence_collection_tool",
            description="Normalizes uploaded evidence and organizes artifacts.",
            capabilities=["evidence_normalization"],
            tags=["investigation"]
        )
        super().__init__(name="evidence_collection_tool", metadata=metadata)

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        try:
            validated_input = EvidenceCollectionInput(**kwargs)
        except Exception as e:
            logger.error(f"Validation error in EvidenceCollectionTool: {e}")
            raise ValueError(f"Invalid input: {e}")

        items = []
        for raw in validated_input.raw_evidence:
            ev_id = str(uuid.uuid4())
            ev_type = raw.get("type", "unknown")
            source = raw.get("source", "unknown")
            timestamp = raw.get("timestamp", None)
            
            raw_content = raw.get("content", raw)
            if not isinstance(raw_content, dict):
                raw_content = {"data": raw_content}
            
            evidence = Evidence(
                id=ev_id,
                type=ev_type,
                source=source,
                content=raw_content,
                timestamp=timestamp
            )
            items.append(evidence)

        collection = EvidenceCollection(items=items, total_count=len(items))
        logger.info(f"Normalized {collection.total_count} evidence items.")
        return collection.model_dump()
