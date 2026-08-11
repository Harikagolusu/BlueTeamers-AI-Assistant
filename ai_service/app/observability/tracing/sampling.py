from abc import ABC, abstractmethod
import random

class ISampler(ABC):
    @abstractmethod
    def should_sample(self, trace_id: str) -> bool: pass

class AlwaysOnSampler(ISampler):
    def should_sample(self, trace_id: str) -> bool: return True

class PercentageSampler(ISampler):
    def __init__(self, probability: float = 0.1):
        self._probability = probability

    def should_sample(self, trace_id: str) -> bool:
        return random.random() < self._probability
