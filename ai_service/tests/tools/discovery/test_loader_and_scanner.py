import pytest
from app.tools.discovery.loader.module_loader import ModuleLoader
from app.tools.discovery.scanner.class_scanner import ClassScanner
from app.tools.discovery.exceptions.exceptions import ToolLoadingError

def test_loader_success():
    loader = ModuleLoader()
    # Loading a standard library module just to test it works
    modules = loader.load_packages(["json"], excluded=[])
    assert len(modules) >= 1
    assert modules[0].__name__ == "json"

def test_loader_failure():
    loader = ModuleLoader()
    with pytest.raises(ToolLoadingError):
        loader.load_packages(["non_existent_package_123"], excluded=[])

def test_scanner_with_no_tools():
    import json
    scanner = ClassScanner()
    classes = scanner.scan_classes([json])
    assert len(classes) == 0
