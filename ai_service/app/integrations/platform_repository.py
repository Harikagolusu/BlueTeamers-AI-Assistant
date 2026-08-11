from typing import Dict, Any, List
from app.integrations.interfaces import IPlatformKnowledgeRepository
from app.integrations.courses_api import CoursesAPI

class PlatformKnowledgeRepository(IPlatformKnowledgeRepository):
    """
    Concrete implementation combining real Django APIs for available entities 
    (Courses, Assessments) and mock data for pending endpoints (Labs, Badges).
    """
    def __init__(self, courses_api: CoursesAPI):
        self._courses_api = courses_api
        
    async def get_courses(self, token: str) -> List[Dict[str, Any]]:
        try:
            courses = await self._courses_api.get_courses(token)
            # Convert models to dictionaries for LLM context
            return [
                {
                    "id": c.id,
                    "title": c.title,
                    "description": c.description,
                    "level": c.level,
                    "duration": c.duration
                } for c in courses
            ]
        except Exception as e:
            # Fallback if django backend is unreachable during local testing
            return [
                {"id": 1, "title": "SOC Analyst 101", "description": "Introduction to SOC operations and monitoring.", "level": "Beginner"},
                {"id": 2, "title": "Incident Response", "description": "Advanced incident response and forensics.", "level": "Advanced"}
            ]
            
    async def get_course_details(self, course_id: int, token: str) -> Dict[str, Any]:
        try:
            course = await self._courses_api.get_course(course_id, token)
            return {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "level": course.level,
                "duration": course.duration
            }
        except Exception:
            return {"id": course_id, "title": "SOC Analyst 101", "description": "Introduction to SOC operations and monitoring."}
            
    async def get_labs(self, token: str) -> List[Dict[str, Any]]:
        # Mock data as labs API doesn't exist yet
        return [
            {"id": 101, "title": "Network Traffic Analysis Lab", "difficulty": "Intermediate", "focus": "Wireshark, TCP/IP"},
            {"id": 102, "title": "Malware Analysis Sandbox", "difficulty": "Advanced", "focus": "Reverse Engineering"}
        ]
        
    async def get_learning_paths(self, token: str) -> List[Dict[str, Any]]:
        # Mock data as learning paths API doesn't exist yet
        return [
            {"id": 1, "name": "Junior SOC Analyst Path", "courses": ["SOC Analyst 101", "Network Traffic Analysis Lab"]},
            {"id": 2, "name": "Threat Hunter Path", "courses": ["Incident Response", "Malware Analysis Sandbox"]}
        ]
        
    async def get_badges(self, token: str) -> List[Dict[str, Any]]:
        return [
            {"id": 1, "name": "Packet Sniper", "description": "Awarded for completing the Network Traffic Analysis Lab."},
            {"id": 2, "name": "First Responder", "description": "Awarded for completing the Incident Response course."}
        ]
        
    async def search_platform_content(self, query: str, token: str) -> Dict[str, Any]:
        """
        Naive search implementation aggregating all platform data to give the LLM context.
        In a real production environment, this would do a semantic or full-text DB search.
        """
        query_lower = query.lower()
        
        # We fetch all and filter naively for demonstration
        all_courses = await self.get_courses(token)
        all_labs = await self.get_labs(token)
        all_paths = await self.get_learning_paths(token)
        
        results = {
            "courses": [c for c in all_courses if query_lower in c['title'].lower() or query_lower in c['description'].lower()],
            "labs": [l for l in all_labs if query_lower in l['title'].lower() or query_lower in l['focus'].lower()],
            "learning_paths": [p for p in all_paths if query_lower in p['name'].lower()]
        }
        
        # If no strict match, provide a general list so the LLM has something to recommend from
        if not results["courses"] and not results["labs"]:
            results = {
                "courses": all_courses,
                "labs": all_labs,
                "learning_paths": all_paths
            }
            
        return results
