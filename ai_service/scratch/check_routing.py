import asyncio
import sys

sys.path.insert(0, "/home/harika/BlueTeamers-AI-Assistant/ai_service")


async def main():
    from app.chat.bootstrap import _build_intent_service
    from app.chat.routing.agents import AgentCatalog
    from app.chat.routing.query_router import QueryRouter

    intent_service = _build_intent_service()
    router = QueryRouter(intent_service, AgentCatalog())
    queries = [
        "What courses do I have?",
        "Suggest a course for me",
        "Create a learning plan for threat hunting",
        "What is MITRE ATT&CK?",
        "Build me a study plan for the SOC certification",
        "hello",
        "what is a SIEM?",
    ]
    for q in queries:
        analysis = await router.analyze_intent(q, {})
        decision = router.classify(q, analysis)
        print(
            f"{q!r:55} -> agent={decision.agent_id:22} engine={decision.engine:14} "
            f"llm_required={decision.llm_required} intent={decision.intent}"
        )


asyncio.run(main())
