from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

class AggregationStrategy(str, Enum):
    MERGE = "MERGE"
    PRIORITIZE = "PRIORITIZE"
    FIRST_SUCCESS = "FIRST_SUCCESS"
    CONSENSUS = "CONSENSUS"
    APPEND = "APPEND"
    CUSTOM = "CUSTOM"

class AggregationPolicy(BaseModel):
    strategy: AggregationStrategy = AggregationStrategy.MERGE
    custom_logic_id: Optional[str] = None
