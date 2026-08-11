from typing import List, Dict, Any

class ComplianceStandard:
    name: str
    controls: List[str]

class SOC2(ComplianceStandard):
    name = "SOC2"
    controls = ["Access Control", "Audit Logging", "Encryption at Rest", "Encryption in Transit"]

class ISO27001(ComplianceStandard):
    name = "ISO27001"
    controls = ["A.9 Access Control", "A.12 Operations Security", "A.10 Cryptography"]

class GDPR(ComplianceStandard):
    name = "GDPR"
    controls = ["Right to Access", "Right to Erasure", "Data Minimization"]

class HIPAA(ComplianceStandard):
    name = "HIPAA"
    controls = ["PHI Encryption", "Access Auditing", "Unique User Identification"]

STANDARDS = {
    "SOC2": SOC2,
    "ISO27001": ISO27001,
    "GDPR": GDPR,
    "HIPAA": HIPAA
}
