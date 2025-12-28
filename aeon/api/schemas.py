from pydantic import BaseModel
from typing import Optional, Dict, Any


class ContextUpdate(BaseModel):
    emotion: Optional[str] = None
    intent: Optional[str] = None
    environment: Optional[str] = None


class AgentResponse(BaseModel):
    thought: str
    action: str


class SessionSnapshot(BaseModel):
    context: Dict[str, Any]
