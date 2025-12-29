import importlib
import pkgutil

def load_protocols(package, registry):
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package.__name__}.{module_name}")
        for obj in module.__dict__.values():
            if hasattr(obj, "__aeon_protocol__"):
                registry.register_protocol(obj)
