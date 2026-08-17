from typing import Dict, Any, Optional, Tuple
from app.prompts.registry import PromptRegistry
from app.prompts.models import PromptVersion

class PromptManager:
    """
    Manages prompt composition, inheritance, overrides, and rendering.
    """
    def __init__(self, registry: PromptRegistry):
        self.registry = registry

    def _resolve_inheritance(self, prompt: PromptVersion) -> PromptVersion:
        """
        Resolves inheritance by merging parent prompt content.
        Child overrides parent.
        """
        if not prompt.parent_id:
            return prompt
            
        # Assuming parent_id format is "name:version" or "name"
        parts = prompt.parent_id.split(":")
        parent_name = parts[0]
        parent_version = parts[1] if len(parts) > 1 else None
        
        parent = self.registry.get(parent_name, parent_version)
        if not parent:
            raise ValueError(f"Parent prompt {prompt.parent_id} not found.")
            
        # Merge logic: child overrides if provided, else use parent
        system_prompt = prompt.system_prompt if prompt.system_prompt else parent.system_prompt
        user_prompt = prompt.user_prompt if prompt.user_prompt else parent.user_prompt
        
        # Merge variables
        variables = list(set(parent.variables + prompt.variables))
        
        return PromptVersion(
            id=prompt.id,
            name=prompt.name,
            version=prompt.version,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            variables=variables,
            parent_id=parent.parent_id, # Recursive could go here
            metadata={**parent.metadata, **prompt.metadata}
        )

    def render(self, name: str, version: Optional[str] = None, **kwargs) -> Tuple[str, str]:
        """
        Renders the prompt by name/version and format variables.
        Returns (system_prompt, user_prompt)
        """
        prompt = self.registry.get(name, version)
        if not prompt:
            raise ValueError(f"Prompt {name} (version: {version}) not found in registry.")
            
        resolved = self._resolve_inheritance(prompt)
        
        try:
            system_formatted = resolved.system_prompt.format(**kwargs)
        except KeyError:
            # For loose formatting if not all kwargs provided
            system_formatted = resolved.system_prompt
            
        try:
            user_formatted = resolved.user_prompt.format(**kwargs)
        except KeyError:
            user_formatted = resolved.user_prompt
            
        return system_formatted, user_formatted
