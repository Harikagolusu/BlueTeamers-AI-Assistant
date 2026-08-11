import asyncio, sys
sys.path.insert(0, "/home/harika/BlueTeamers-AI-Assistant/ai_service")

from app.chat.bootstrap import _build_intent_service

queries = [
    "Suggest SOC courses",
    "What courses do I have?",
    "What courses am I enrolled in?",
    "Show my enrolled courses",
    "What is my progress?",
    "Resume my current course",
    "What certificates do I have?",
    "Which assessment should I take next?",
    "Show my learning progress",
    "Recommend my next course",
    "Explain SIEM",
    "Explain MITRE ATT&CK",
    "Explain Windows Event Logs",
    "Explain IOC",
    "Explain Sigma Rules",
    "Explain SOC Analyst workflow",
    "What is a SYN Flood?",
    "Hello",
    "Tell me a joke",
    "What is Python?",
]

async def main():
    svc = _build_intent_service()
    for q in queries:
        res = await svc.analyze_intent(q, {})
        primary = res.primary_intent
        print(f"{q!r:42} -> intent={primary.type.value:<22} conf={primary.confidence:.2f} route={res.route_recommendation.engine if res.route_recommendation else None}")

asyncio.run(main())
