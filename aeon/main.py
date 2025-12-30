from fastapi import FastAPI
from aeon.api.routes import router

app = FastAPI(
    title="AEON Conscious Context Engine",
    description="Autonomous reasoning & protocol-based AI system",
    version="0.1.0",
)

app.include_router(router)

from aeon.core.registry import AEONRegistry
from aeon.api.main import app

def boot():
    registry = AEONRegistry()
    return registry, app

if __name__ == "__main__":
    registry, _ = boot()
    print("AEON platform booted.")
