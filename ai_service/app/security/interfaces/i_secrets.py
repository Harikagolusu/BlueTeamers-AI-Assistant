from abc import ABC, abstractmethod
from typing import Any

class ISecretProvider(ABC):
    @abstractmethod
    def get_secret(self, secret_id: str) -> str: pass
    @abstractmethod
    def set_secret(self, secret_id: str, value: str) -> None: pass

class ISecretVault(ABC):
    @abstractmethod
    def retrieve(self, secret_id: str) -> str: pass
    @abstractmethod
    def store(self, secret_id: str, value: str) -> None: pass

class ISecretRotationManager(ABC):
    @abstractmethod
    def rotate_secret(self, secret_id: str) -> None: pass
    @abstractmethod
    def schedule_rotation(self, secret_id: str, cron: str) -> None: pass
