from abc import ABC, abstractmethod
from typing import Any

class ISignatureValidator(ABC):
    @abstractmethod
    def validate_signature(self, package: Any) -> bool: pass

class ICertificateValidator(ABC):
    @abstractmethod
    def validate_certificate(self, certificate_id: str) -> bool: pass

class ITrustValidator(ABC):
    @abstractmethod
    def validate_trust(self, package: Any) -> bool: pass

class ITrustManager(ABC):
    @abstractmethod
    def is_trusted(self, entity_id: str) -> bool: pass
