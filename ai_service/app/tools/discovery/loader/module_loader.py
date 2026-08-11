import importlib
import pkgutil
import sys
from typing import List, Any
from app.tools.discovery.interfaces.discovery_interfaces import IModuleLoader
from app.tools.discovery.exceptions.exceptions import ToolLoadingError

class ModuleLoader(IModuleLoader):
    """
    Recursively finds and dynamically imports all Python modules safely.
    """
    def load_packages(self, packages: List[str], excluded: List[str]) -> List[Any]:
        loaded_modules = []
        for pkg_name in packages:
            try:
                # Import the root package first
                pkg = importlib.import_module(pkg_name)
                loaded_modules.append(pkg)
                
                # If it's a package (has __path__), walk it
                if hasattr(pkg, '__path__'):
                    for _, name, is_pkg in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + '.'):
                        if any(name.startswith(ex) for ex in excluded):
                            continue
                        try:
                            module = importlib.import_module(name)
                            loaded_modules.append(module)
                        except Exception as e:
                            raise ToolLoadingError(f"Failed to load submodule {name}: {e}")
            except Exception as e:
                raise ToolLoadingError(f"Failed to load package {pkg_name}: {e}")
                
        return loaded_modules
