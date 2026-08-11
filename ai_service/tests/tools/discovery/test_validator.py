import pytest
from app.tools.discovery.validators.tool_validator import ToolValidator
from app.tools.discovery.metadata.models import ToolMetadata
from app.tools.discovery.exceptions.exceptions import DuplicateToolError, ToolValidationError

def test_validator_success():
    validator = ToolValidator()
    metadata = ToolMetadata(name="valid_tool", description="desc")
    # Should not raise
    validator.validate(metadata, set(["other_tool"]))

def test_validator_duplicate_name():
    validator = ToolValidator()
    metadata = ToolMetadata(name="existing_tool", description="desc")
    with pytest.raises(DuplicateToolError):
        validator.validate(metadata, set(["existing_tool"]))

def test_validator_duplicate_alias():
    validator = ToolValidator()
    metadata = ToolMetadata(name="new_tool", description="desc", aliases=["taken_alias"])
    with pytest.raises(DuplicateToolError):
        validator.validate(metadata, set(["taken_alias"]))

def test_validator_invalid_name():
    validator = ToolValidator()
    metadata = ToolMetadata(name="invalid-name!", description="desc")
    with pytest.raises(ToolValidationError):
        validator.validate(metadata, set())

def test_validator_invalid_timeout():
    validator = ToolValidator()
    metadata = ToolMetadata(name="valid_tool", description="desc", timeout=0)
    with pytest.raises(ToolValidationError):
        validator.validate(metadata, set())
