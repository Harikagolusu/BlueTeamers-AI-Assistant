import asyncio, sys
sys.path.insert(0, "/home/harika/BlueTeamers-AI-Assistant/ai_service")
from app.chat.bootstrap import _build_intent_service

queries = [
    "T1059", "What is MITRE T1059?", "Explain T1059",
    "SIEM vs SOC", "How do firewalls work?",
    "What is command and control?",
    "Windows event log IDs", "sigma rule example",
    "show me a detection rule", "phishing detection",
    "what is a SOC analyst?", "can you summarize my week?",
    "how to write a sigma rule",
    "recommend a detection engineering course",
]
async def main():
    svc = _build_intent_service()
    for q in queries:
        res = await svc.analyze_intent(q, {})
        p = res.primary_intent
        print(f"{q!r:40} -> {p.type.value:<20} conf={p.confidence:.2f} route={res.route_recommendation.engine if res.route_recommendation else None}")
asyncio.run(main())
