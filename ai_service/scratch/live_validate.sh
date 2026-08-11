#!/bin/bash
B=http://127.0.0.1:8001
check() {
  local desc="$1"; local payload="$2"
  local out code
  out=$(curl -s -X POST $B/api/v1/chat -H "Content-Type: application/json" -d "$payload")
  code=$(curl -s -o /dev/null -w "%{http_code}" -X POST $B/api/v1/chat -H "Content-Type: application/json" -d "$payload")
  echo "### $desc [HTTP $code]"
  echo "$out" | head -c 600
  echo; echo
}
check "RAG: Explain SIEM" '{"query":"Explain SIEM"}'
check "PLATFORM: What courses do I have?" '{"query":"What courses do I have?"}'
check "PLATFORM: What is my progress?" '{"query":"What is my progress?"}'
check "GENERAL: Tell me a joke" '{"query":"Tell me a joke"}'
check "GENERAL: What is Python?" '{"query":"What is Python?"}'
check "RAG: How do firewalls work?" '{"query":"How do firewalls work?"}'
check "RAG: sigma rule example" '{"query":"sigma rule example"}'
check "RAG: T1059" '{"query":"T1059"}'
