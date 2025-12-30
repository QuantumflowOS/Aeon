from aeon.core.registry import AEONRegistry
from aeon.api.main import app

def boot():
    registry = AEONRegistry()
    return registry, app

if __name__ == "__main__":
    registry, _ = boot()
    print("AEON platform booted.")
