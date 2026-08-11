from typing import Dict, Optional, List
from app.prompts.models import PromptVersion

class PromptRegistry:
    """
    In-memory registry for prompt versions.
    """
    def __init__(self):
        # Dict[prompt_name, Dict[version, PromptVersion]]
        self._prompts: Dict[str, Dict[str, PromptVersion]] = {}

    def register(self, prompt: PromptVersion) -> None:
        if prompt.name not in self._prompts:
            self._prompts[prompt.name] = {}
        self._prompts[prompt.name][prompt.version] = prompt

    def get(self, name: str, version: Optional[str] = None) -> Optional[PromptVersion]:
        if name not in self._prompts:
            return None
            
        versions = self._prompts[name]
        if not versions:
            return None
            
        if version:
            return versions.get(version)
            
        # Return latest version based on string sorting for simplicity
        latest_version = sorted(versions.keys())[-1]
        return versions[latest_version]
        
    def list_prompts(self) -> List[str]:
        return list(self._prompts.keys())
