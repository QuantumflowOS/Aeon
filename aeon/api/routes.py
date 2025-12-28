from fastapi import APIRouter
from aeon.core.context import Context
from aeon.core.protocol_manager import ProtocolManager
from aeon.core.protocol import Protocol
from aeon.core.memory import Memory
from aeon.core.agent import Agent

from aeon.protocols.emotional import happy, sad, create, comfort
from aeon.protocols.productivity import focused, focus_action
from aeon.api.schemas import ContextUpdate, AgentResponse

router = APIRouter()

# --- GLOBAL SINGLETONS (intentional for now) ---
context = Context()
memory = Memory()
pm = ProtocolManager()

pm.register(Protocol("Happy", happy, create, 3))
pm.register(Protocol("Sad", sad, comfort, 2))
pm.register(Protocol("Focus", focused, focus_action, 3))

agent = Agent(context, pm, memory)

# -------- ROUTES --------

@router.post("/context/update")
def update_context(update: ContextUpdate):
    context.update(
        emotion=update.emotion,
        intent=update.intent,
        environment=update.environment
    )
    return {"status": "context updated", "context": context.to_dict()}


@router.post("/agent/run", response_model=AgentResponse)
def run_agent():
    result = agent.run()

    thought, action = result.split("🤖 Action:")
    return {
        "thought": thought.replace("🧠 Thought:", "").strip(),
        "action": action.strip()
    }


@router.get("/memory")
def get_memory():
    return {"sessions": memory.sessions}
