from app.agents.models.agent_package import AgentPackage, AgentManifest
from app.agents.models.metadata import PackageMetadata
from app.agents.templates.registry import TemplateRegistry

def setup_default_templates(registry: TemplateRegistry) -> None:
    """Pre-fills the registry with basic organizational templates"""
    
    # Security Agent Template
    security_package = AgentPackage(
        manifest=AgentManifest(
            id="template-security-agent",
            name="Security Agent",
            version="1.0.0",
            capabilities=["security", "mitre", "yara"],
            skills=["ioc_analysis", "threat_hunting"]
        ),
        metadata=PackageMetadata(
            author="Enterprise AI Platform",
            category="Security"
        )
    )
    
    # Research Agent Template
    research_package = AgentPackage(
        manifest=AgentManifest(
            id="template-research-agent",
            name="Research Agent",
            version="1.0.0",
            capabilities=["search", "summarization", "analysis"],
            skills=["web_search", "document_summary"]
        ),
        metadata=PackageMetadata(
            author="Enterprise AI Platform",
            category="Research"
        )
    )

    registry.register_template("security-agent", security_package)
    registry.register_template("research-agent", research_package)
