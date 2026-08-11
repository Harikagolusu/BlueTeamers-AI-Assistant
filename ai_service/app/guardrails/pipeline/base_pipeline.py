import asyncio
import logging
from typing import List
from app.guardrails.domain.models.context import GuardrailContext
from app.guardrails.domain.interfaces.group_interface import IPolicyGroup
from app.guardrails.domain.interfaces.pipeline_interface import IGuardrailPipeline
from app.guardrails.domain.models.enums import PolicyAction
from app.guardrails.exceptions.guardrail_exceptions import PolicyViolationError
from app.guardrails.pipeline.result_aggregator import ResultAggregator

logger = logging.getLogger(__name__)

class BasePipeline(IGuardrailPipeline):
    def __init__(self, name: str):
        self.name = name
        self._groups: List[IPolicyGroup] = []

    def add_group(self, group: IPolicyGroup) -> None:
        self._groups.append(group)
        # Sort groups by priority ascending (1 = Critical, 4 = Low)
        self._groups.sort(key=lambda g: g.priority)

    async def execute(self, context: GuardrailContext) -> GuardrailContext:
        logger.info(f"Executing {self.name} Pipeline for request {context.request_id}")
        aggregator = ResultAggregator(context.is_audit_mode)
        
        for group in self._groups:
            logger.debug(f"Executing group: {group.name} (Priority: {group.priority.name})")
            
            # Execute all policies in the group in parallel
            results = await group.evaluate_all(context)
            
            # Aggregate results
            for policy, result in zip(group.policies, results):
                aggregator.add_result(policy, result)
            
            # Fail fast if BLOCK was issued (and not audit mode)
            if aggregator.should_block():
                logger.warning(f"Pipeline {self.name} blocked at group {group.name}.")
                raise PolicyViolationError(
                    f"Request blocked by guardrails: {aggregator.get_block_reasons()}"
                )

        # Apply any text modifications from ALLOW/WARN results
        modified_context = aggregator.apply_modifications(context)
        return modified_context
