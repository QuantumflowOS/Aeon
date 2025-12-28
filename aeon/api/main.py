from fastapi import FastAPI
from aeon.api.routes import router

app = FastAPI(
    title="AEON Conscious Context Engine",
    description="Autonomous reasoning & protocol-based AI system",
    version="0.1.0",
)

app.include_router(router)
