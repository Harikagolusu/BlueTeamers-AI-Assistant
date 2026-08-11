import pytest
from unittest.mock import Mock
from app.tools.discovery.registration.registration_service import RegistrationService
from app.tools.discovery.exceptions.exceptions import ToolRegistrationError
from app.tools.interfaces.registry import IToolRegistry

def test_registration_success():
    mock_registry = Mock(spec=IToolRegistry)
    service = RegistrationService(mock_registry)
    mock_tool = Mock()
    mock_tool.name = "test_tool"
    
    service.register(mock_tool)
    mock_registry.register_tool.assert_called_once_with(mock_tool)

def test_registration_failure():
    mock_registry = Mock(spec=IToolRegistry)
    mock_registry.register_tool.side_effect = Exception("Registry error")
    service = RegistrationService(mock_registry)
    
    mock_tool = Mock()
    mock_tool.name = "test_tool"
    
    with pytest.raises(ToolRegistrationError):
        service.register(mock_tool)
