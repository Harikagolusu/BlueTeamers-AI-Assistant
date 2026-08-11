import pytest

from app.prompt_builder.schemas import PromptRequest
from app.prompt_builder.service import PromptBuilderService
from app.prompt_builder.exceptions import TemplateNotFoundException
from app.context.schemas import ContextDocument, ContextChunk

@pytest.fixture
def service():
    return PromptBuilderService()

@pytest.fixture
def dummy_context():
    return ContextDocument(
        chunks=[ContextChunk(id="c1", text="Firewalls block traffic.", score=0.9, metadata={})],
        estimated_tokens=4,
        formatted_text="--- SOURCE: Lesson 1 ---\nFirewalls block traffic."
    )

def test_template_selection_and_construction(service, dummy_context):
    req = PromptRequest(
        query="What do firewalls do?",
        context=dummy_context,
        template_name="concise"
    )
    res = service.build_prompt(req)
    
    assert res.template_used == "concise"
    assert "Firewalls block traffic" in res.payload.user
    assert "What do firewalls do?" in res.payload.user
    assert "CRITICAL RULES" in res.payload.system
    assert "brief, concise answer" in res.payload.user

def test_missing_context(service):
    empty_context = ContextDocument(chunks=[], estimated_tokens=0, formatted_text="")
    req = PromptRequest(
        query="Explain?",
        context=empty_context,
        template_name="default_rag"
    )
    res = service.build_prompt(req)
    
    assert "No context retrieved." in res.payload.user

def test_invalid_template(service, dummy_context):
    req = PromptRequest(
        query="Q",
        context=dummy_context,
        template_name="nonexistent"
    )
    with pytest.raises(TemplateNotFoundException):
        service.build_prompt(req)

def test_token_estimation_and_warning(service, dummy_context, caplog):
    # Force max tokens very low to trigger warning
    service.max_prompt_tokens = 10
    
    req = PromptRequest(query="Q", context=dummy_context)
    res = service.build_prompt(req)
    
    assert res.estimated_tokens > 10
    assert "Prompt exceeds max tokens limits" in caplog.text

def test_health_check(service):
    h = service.health_check()
    assert h.template_status == "healthy"
