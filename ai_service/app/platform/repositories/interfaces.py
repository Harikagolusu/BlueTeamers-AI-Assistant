from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform.models import Course, Lab, LearningPath, Assessment, Certificate, Badge, Progress, UserProfile, Purchase

class IPlatformRepository(ABC):
    @abstractmethod
    async def get_user_profile(self, token: str) -> Optional[UserProfile]:
        pass

    @abstractmethod
    async def get_purchases(self, token: str) -> List[Purchase]:
        pass

    @abstractmethod
    async def get_courses(self, token: str) -> List[Course]:
        pass

    @abstractmethod
    async def get_enrolled_courses(self, token: str) -> List[Course]:
        """Courses the user has paid for (derived from purchases + catalog)."""
        pass

    @abstractmethod
    async def get_course(self, slug: str, token: str) -> Optional[Course]:
        pass
        
    @abstractmethod
    async def get_labs(self, course_slug: str, token: str) -> List[Lab]:
        pass
        
    @abstractmethod
    async def get_learning_paths(self, token: str) -> List[LearningPath]:
        pass
        
    @abstractmethod
    async def get_assessments(self, course_slug: str, token: str) -> List[Assessment]:
        pass
        
    @abstractmethod
    async def get_certificates(self, token: str) -> List[Certificate]:
        pass
        
    @abstractmethod
    async def get_badges(self, token: str) -> List[Badge]:
        pass
        
    @abstractmethod
    async def get_progress(self, course_slug: str, token: str) -> Optional[Progress]:
        pass
        
    @abstractmethod
    async def search(self, query: str, token: str) -> List[Course]:
        pass
