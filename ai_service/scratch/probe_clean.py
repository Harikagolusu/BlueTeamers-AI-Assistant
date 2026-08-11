import json
import urllib.request


def probe(q, stream=False):
    payload = json.dumps({"message": q, "stream": stream}).encode()
    req = urllib.request.Request(
        "http://localhost:8001/api/chat/",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        body = r.read().decode()
    print(f"=== {q!r} ===")
    print(body[:600])
    print()


probe("hello")
probe("what is siem", stream=True)
probe("what is soc")
probe("what is phishing")
probe("recommend me some courses as beginner")
