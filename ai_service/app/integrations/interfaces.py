from abc import ABC, abstractmethod
from typing import Dict, Any, List

class IPlatformKnowledgeRepository(ABC):
    """
    Interface for querying the platform catalog (courses, labs, learning paths, badges, etc.).
    Ensures that LLM interactions are grounded in actual platform data.
    """
    
    @abstractmethod
    async def get_courses(self, token: str) -> List[Dict[str, Any]]:
        pass
        
    @abstractmethod
    async def get_course_details(self, course_id: int, token: str) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    async def get_labs(self, token: str) -> List[Dict[str, Any]]:
        pass
        
    @abstractmethod
    async def get_learning_paths(self, token: str) -> List[Dict[str, Any]]:
        pass
        
    @abstractmethod
    async def get_badges(self, token: str) -> List[Dict[str, Any]]:
        pass
        
    @abstractmethod
    async def search_platform_content(self, query: str, token: str) -> Dict[str, Any]:
        """
        Aggregate search method that returns relevant courses, labs, and paths matching the query.
        """
        pass
