import urllib.request


def check(name, url):
    try:
        r = urllib.request.urlopen(url, timeout=8)
        print(f"{name} -> HTTP {r.status}")
    except Exception as e:
        print(f"{name} -> FAIL: {e}")


check("frontend 5173", "http://localhost:5173/")
check("django 8000", "http://localhost:8000/")
check("ai-service 8001", "http://localhost:8001/docs")