import os
import ast
from pathlib import Path

def get_base_path():
    return Path(os.path.dirname(__file__)).parent.parent.parent / "app" / "tools"

def test_rule_1_domain_isolation():
    """Domain layer must not import from Application, Infrastructure, or Implementations."""
    domain_path = get_base_path() / "domain"
    if not domain_path.exists(): return
    for py_file in domain_path.rglob("*.py"):
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                assert "app.tools.infrastructure" not in module, f"Domain leak in {py_file}"
                assert "app.tools.implementations" not in module, f"Domain leak in {py_file}"
                assert "app.tools.application" not in module, f"Domain leak in {py_file}"

def test_rule_2_no_manual_service_instantiation():
    """Tools must not instantiate services directly (Service())."""
    impl_path = get_base_path() / "implementations"
    if not impl_path.exists(): return
    for py_file in impl_path.rglob("*.py"):
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name.endswith("Service"):
                    assert False, f"Manual service instantiation found in {py_file}: {func_name}()"

def test_rule_3_basetool_inheritance():
    """Every class in implementations should inherit from BaseTool."""
    impl_path = get_base_path() / "implementations"
    if not impl_path.exists(): return
    for py_file in impl_path.rglob("*.py"):
        if py_file.name == "__init__.py": continue
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
                if bases: # If it's a class with bases, it should be a tool
                    assert "BaseTool" in bases, f"Class {node.name} in {py_file} does not inherit BaseTool"

def test_rule_4_tool_decorator_usage():
    """Every tool class must use the @tool decorator."""
    impl_path = get_base_path() / "implementations"
    if not impl_path.exists(): return
    for py_file in impl_path.rglob("*.py"):
        if py_file.name == "__init__.py": continue
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                decorators = [d.func.id for d in node.decorator_list if isinstance(d, ast.Call) and isinstance(d.func, ast.Name)]
                decorators += [d.id for d in node.decorator_list if isinstance(d, ast.Name)]
                assert "tool" in decorators, f"Class {node.name} in {py_file} missing @tool decorator"

def test_rule_5_no_circular_dependencies():
    """Basic check to ensure application doesn't import implementations."""
    app_path = get_base_path() / "application"
    if not app_path.exists(): return
    for py_file in app_path.rglob("*.py"):
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                assert "app.tools.implementations" not in module, f"Circular dep in {py_file}"

def test_rule_6_application_depends_on_interfaces():
    """Application services should implement interfaces (naming convention check)."""
    app_path = get_base_path() / "application"
    if not app_path.exists(): return
    for py_file in app_path.rglob("*.py"):
        if "interfaces" in str(py_file) or py_file.name == "__init__.py": continue
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name.endswith("Service"):
                bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
                assert any(b.startswith("I") and b.endswith("Service") for b in bases), f"Service {node.name} does not implement an I*Service interface"

def test_rule_7_infrastructure_not_imported_by_domain():
    """Redundant to rule 1 but requested explicitly."""
    test_rule_1_domain_isolation()

def test_rule_8_discovery_compatibility():
    """Ensures discovery metadata models are structurally sound."""
    from app.tools.domain.models.tool_metadata import ToolMetadata
    assert "name" in ToolMetadata.model_fields
    assert "description" in ToolMetadata.model_fields

def test_rule_9_no_stix_in_domain():
    """Domain layer must not import or contain STIX format references. Only MitreProvider should know about STIX."""
    domain_path = get_base_path() / "domain"
    if not domain_path.exists(): return
    for py_file in domain_path.rglob("*.py"):
        content = py_file.read_text(encoding="utf-8").lower()
        assert "stix" not in content, f"STIX format leaked into domain layer in {py_file}"
