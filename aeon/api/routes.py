# aeon/api/routes.py
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from aeon.core.agent import Agent
from aeon.core.context import Context
from aeon.core.protocol import Protocol
from aeon.core.protocol_manager import ProtocolManager
from aeon.core.semantic_memory import SemanticMemory
from aeon.core.memory import Memory
from aeon.protocols.emotional import happy, sad, create, comfort
from aeon.protocols.productivity import focused, focus_action

router = APIRouter()

# Initialize global components
context = Context()
protocol_manager = ProtocolManager()
semantic_memory = SemanticMemory()
memory = Memory()

# Register default protocols
protocol_manager.register(Protocol("Happy", happy, create, 3.0))
protocol_manager.register(Protocol("Sad", sad, comfort, 2.0))
protocol_manager.register(Protocol("Focus", focused, focus_action, 3.0))

# Initialize agent
agent = Agent(
    context=context,
    protocol_manager=protocol_manager,
    semantic=semantic_memory,
    memory=memory
)


class ContextUpdateRequest(BaseModel):
    emotion: str = None
    intent: str = None
    environment: str = None


class GoalRequest(BaseModel):
    goal: str


@router.post("/context/update")
async def update_context(request: ContextUpdateRequest):
    """
    Update agent context from JSON body and store automatically in memory.
    """
    try:
        data = request.dict(exclude_none=True)
        
        # Update context object
        context.update(**data)
        
        # Update agent's context reference
        result = agent.update_context(data)
        
        return {
            "status": "success",
            "message": "Context updated successfully",
            "context": context.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/agent/run")
async def run_agent():
    """
    Execute the agent's main loop with current context.
    """
    try:
        result = agent.run()
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agent/goal")
async def run_goal(request: GoalRequest):
    """
    Execute a goal using semantic memory and protocols.
    """
    try:
        result = agent.run_goal(request.goal)
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/memory")
async def get_memory():
    """
    Retrieve all memory entries (semantic and episodic).
    """
    try:
        mem_data = agent.memory.dump() if agent.memory else {}
        semantic_data = agent.semantic.all_memory() if hasattr(agent.semantic, 'all_memory') else []
        
        return {
            "status": "success",
            "memory": {
                "semantic": semantic_data,
                "episodic": mem_data.get("episodic", []),
                "internal_semantic": mem_data.get("semantic", [])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/system/health")
async def system_health():
    """
    Get system health and statistics.
    """
    try:
        protocols = agent.protocol_manager.protocols
        
        # Handle both dict and list protocol storage
        if isinstance(protocols, dict):
            protocol_count = len(protocols)
            protocol_list = [
                {
                    "name": name,
                    "reward": data.get("reward", 0),
                    "executions": data.get("executions", 0)
                }
                for name, data in protocols.items()
            ]
        else:
            protocol_count = len(protocols)
            protocol_list = [
                {
                    "name": p.name,
                    "reward": p.reward,
                    "executions": p.executions
                }
                for p in protocols
            ]
        
        return {
            "status": "healthy",
            "protocols": protocol_list,
            "protocol_count": protocol_count,
            "context": context.to_dict(),
            "memory_items": len(agent.memory.episodic) if agent.memory else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/protocols")
async def get_protocols():
    """
    List all registered protocols.
    """
    try:
        protocols = agent.protocol_manager.protocols
        
        if isinstance(protocols, dict):
            protocol_list = [
                {
                    "name": name,
                    "reward": data.get("reward", 0),
                    "executions": data.get("executions", 0)
                }
                for name, data in protocols.items()
            ]
        else:
            protocol_list = [
                {
                    "name": p.name,
                    "reward": p.reward,
                    "executions": p.executions
                }
                for p in protocols
            ]
        
        return {
            "status": "success",
            "protocols": protocol_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))                "executions": p.executions
            }
            for p in pm.protocols
        ]
    }
