from typing import Any, Dict
from abc import ABC, abstractmethod

class IRiskAnalyzer(ABC):
    @abstractmethod
    def analyze(self, package: Any) -> Dict[str, float]:
        """Returns risk components mapping to a float score (0.0 to 1.0)"""
        pass

class TrustAnalyzer(IRiskAnalyzer):
    def analyze(self, package: Any) -> Dict[str, float]:
        # If it has a valid signature, risk is lower
        return {"trust_risk": 0.1 if getattr(package, "signature", None) else 0.8}

class PermissionAnalyzer(IRiskAnalyzer):
    def analyze(self, package: Any) -> Dict[str, float]:
        perms = getattr(package, "permissions", [])
        risk = min(1.0, len(perms) * 0.1) # Naive: more perms = higher risk
        if "fs.write" in perms:
            risk += 0.5
        return {"permission_risk": min(1.0, risk)}

class BehaviorAnalyzer(IRiskAnalyzer):
    def analyze(self, package: Any) -> Dict[str, float]:
        return {"behavior_risk": 0.2} # Stub
        
class PolicyAnalyzer(IRiskAnalyzer):
    def analyze(self, package: Any) -> Dict[str, float]:
        return {"policy_risk": 0.1} # Stub
