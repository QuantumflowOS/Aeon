# aeon/core/agent.py
from .semantic_memory import SemanticMemory
from .protocols import ProtocolManager
from .cognition import CognitionEngine
import logging

class Agent:
    """
    AEON Agent: stores context, executes protocols, and leverages semantic memory.
    """
    def __init__(self, context=None, protocol_manager=None, semantic=None, memory=None):
        self.context = context or {}
        self.protocol_manager = protocol_manager or ProtocolManager()
        self.semantic = semantic or SemanticMemory()
        self.memory = memory  # episodic memory if provided
        self.subgoal_history = []
        self.cognition = CognitionEngine()
        
    def update_context(self, new_context: dict):
        """Update agent's context with new information."""
        if isinstance(self.context, dict):
            self.context.update(new_context)
        else:
            # If context is an object, update its attributes
            for key, value in new_context.items():
                setattr(self.context, key, value)
        
        # Store in memory if available
        if self.memory:
            self.memory.add_semantic({"context_update": new_context})
        
        return {"status": "context updated", "context": self.context}

    def plan_goal(self, goal: str):
        """Use semantic memory to generate subgoals related to the main goal."""
        related = self.semantic.query(goal)
        subgoals = [item["concept"] for item in related if item.get("concept") != goal]
        subgoals.append(goal)
        return subgoals

    def run_goal(self, goal: str):
        """Execute goal by generating subgoals and running them."""
        subgoals = self.plan_goal(goal)
        results = []

        for subgoal in subgoals:
            self.semantic.store({"subgoal": subgoal})
            result = {
                "step": subgoal, 
                "result": "Default support engaged.", 
                "reward": None
            }
            results.append(result)
            self.subgoal_history.append(subgoal)

        return {
            "goal": goal,
            "steps": results,
            "self_improvement": self.protocol_manager.get_protocols()
        }
    
    def run(self):
        """
        Main agent execution loop.
        1. Analyze context using cognition engine
        2. Select best protocol
        3. Execute protocol
        4. Store experience in memory
        """
        # Get cognitive assessment
        thought = self.cognition.think(self.context)
        logging.info(f"Agent thought: {thought}")
        
        # Select best protocol based on context
        protocol = self.protocol_manager.best(self.context)
        
        if protocol:
            action = protocol.execute(self.context)
            
            # Store episodic memory
            if self.memory:
                self.memory.add_episodic(self.context, action)
            
            return {
                "thought": thought,
                "protocol": protocol.name,
                "action": action,
                "reward": protocol.reward
            }
        else:
            # No matching protocol
            default_action = "No specific protocol matched. Maintaining baseline behavior."
            
            if self.memory:
                self.memory.add_episodic(self.context, default_action)
            
            return {
                "thought": thought,
                "protocol": "default",
                "action": default_action,
                "reward": None
        }
