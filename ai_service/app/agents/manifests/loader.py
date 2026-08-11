import yaml
import os
import logging
from pydantic import ValidationError
from app.agents.manifests.models import AgentManifest

logger = logging.getLogger(__name__)

class ManifestLoader:
    """
    Utility to load Agent Manifests from YAML files.
    """
    @staticmethod
    def load_from_file(file_path: str) -> AgentManifest:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Manifest not found at {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        try:
            return AgentManifest(**data)
        except ValidationError as e:
            logger.error(f"Manifest validation failed for {file_path}: {e}")
            raise ValueError(f"Invalid manifest format in {file_path}. Missing or invalid fields.") from e

    @staticmethod
    def load_all_from_directory(directory_path: str) -> dict[str, AgentManifest]:
        manifests = {}
        if not os.path.exists(directory_path):
            return manifests
            
        for filename in os.listdir(directory_path):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                file_path = os.path.join(directory_path, filename)
                try:
                    manifest = ManifestLoader.load_from_file(file_path)
                    manifests[manifest.name] = manifest
                except Exception as e:
                    logger.error(f"Failed to load manifest {filename}: {e}")
        return manifests
