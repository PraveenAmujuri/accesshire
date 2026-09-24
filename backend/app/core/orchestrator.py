import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("accesshire.orchestrator")

class CentralOrchestrator:
    """
    Central Orchestrator & Supervisor Component:
    - Coordinates execution of multi-agent tasks
    - Passes structured state between agents
    - Monitors agent outputs and validates structured Pydantic responses
    - Implements retries and controlled fallback heuristics
    - Logs telemetry for system observability
    """

    def __init__(self):
        self.logger = logger

    async def execute_task_with_resilience(
        self,
        task_name: str,
        agent_callable,
        state_payload: Dict[str, Any],
        max_retries: int = 2,
        fallback_handler: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Executes an agent task with error trapping, retries, and fallback to ensure
        one failed LLM call does not crash the interview session.
        """
        self.logger.info("CentralOrchestrator: Dispatching task '%s'", task_name)
        attempts = 0
        while attempts <= max_retries:
            try:
                attempts += 1
                result = await agent_callable(state_payload)
                self.logger.info("CentralOrchestrator: Task '%s' completed successfully.", task_name)
                return result
            except Exception as exc:
                self.logger.error(
                    "CentralOrchestrator: Error executing '%s' (Attempt %d/%d): %s",
                    task_name, attempts, max_retries + 1, exc
                )
                if attempts > max_retries:
                    if fallback_handler:
                        self.logger.warning("CentralOrchestrator: Triggering fallback handler for '%s'", task_name)
                        return await fallback_handler(state_payload)
                    raise exc

orchestrator = CentralOrchestrator()
