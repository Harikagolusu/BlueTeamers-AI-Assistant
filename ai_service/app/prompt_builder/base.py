from abc import ABC, abstractmethod
from app.prompt_builder.schemas import PromptRequest, PromptResponse, HealthResponse

class BasePromptBuilder(ABC):
    @abstractmethod
    def build_prompt(self, request: PromptRequest) -> PromptResponse:
        pass
        
    @abstractmethod
    def health_check(self) -> HealthResponse:
        pass
