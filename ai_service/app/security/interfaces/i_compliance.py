from abc import ABC, abstractmethod
from typing import Dict, Any

class IComplianceService(ABC):
    @abstractmethod
    def generate_report(self, standard: str) -> Dict[str, Any]: pass
