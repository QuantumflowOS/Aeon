# tests/test_agent.py
import pytest
from aeon.core.agent import Agent
from aeon.core.context import Context
from aeon.core.protocol import Protocol
from aeon.core.protocol_manager import ProtocolManager
from aeon.core.memory import Memory


def happy_condition(ctx):
    return ctx.emotion == "happy"

def happy_action(ctx):
    return "Spreading joy!"


class TestAgent:
    
    def test_agent_initialization(self):
        """Test basic agent creation"""
        agent = Agent()
        assert agent is not None
        assert isinstance(agent.context, dict)
    
    def test_context_update(self):
        """Test context updating"""
        agent = Agent()
        result = agent.update_context({"emotion": "happy", "intent": "work"})
        assert result["status"] == "context updated"
        assert agent.context["emotion"] == "happy"
    
    def test_protocol_execution(self):
        """Test protocol selection and execution"""
        ctx = Context(emotion="happy", intent="create")
        pm = ProtocolManager()
        memory = Memory()
        
        protocol = Protocol("Happy", happy_condition, happy_action, reward=3.0)
        pm.register(protocol)
        
        agent = Agent(context=ctx, protocol_manager=pm, memory=memory)
        result = agent.run()
        
        assert result["protocol"] == "Happy"
        assert "joy" in result["action"].lower()
    
    def test_goal_execution(self):
        """Test goal-based planning"""
        agent = Agent()
        result = agent.run_goal("test goal")
        
        assert "goal" in result
        assert result["goal"] == "test goal"
        assert "steps" in result


class TestContext:
    
    def test_context_creation(self):
        """Test context initialization"""
        ctx = Context(emotion="neutral", intent="none")
        assert ctx.emotion == "neutral"
        assert ctx.intent == "none"
    
    def test_context_update(self):
        """Test context modification"""
        ctx = Context()
        ctx.update(emotion="happy", intent="work")
        assert ctx.emotion == "happy"
        assert ctx.intent == "work"
    
    def test_context_serialization(self):
        """Test context to dict conversion"""
        ctx = Context(emotion="sad", intent="rest")
        data = ctx.to_dict()
        assert data["emotion"] == "sad"
        assert data["intent"] == "rest"


class TestProtocol:
    
    def test_protocol_matching(self):
        """Test protocol condition matching"""
        ctx = Context(emotion="happy")
        protocol = Protocol("Happy", happy_condition, happy_action)
        assert protocol.matches(ctx) == True
    
    def test_protocol_execution(self):
        """Test protocol action execution"""
        ctx = Context(emotion="happy")
        protocol = Protocol("Happy", happy_condition, happy_action)
        result = protocol.execute(ctx)
        assert protocol.executions == 1
        assert "joy" in result.lower()
    
    def test_reward_update(self):
        """Test reward updating"""
        protocol = Protocol("Test", lambda c: True, lambda c: "action", reward=3.0)
        initial_reward = protocol.reward
        protocol.update_reward(5.0)
        assert protocol.reward != initial_reward
        assert protocol.reward > initial_reward


class TestMemory:
    
    def test_semantic_memory(self):
        """Test semantic memory storage"""
        memory = Memory()
        memory.add_semantic("test concept")
        assert len(memory.semantic) == 1
    
    def test_episodic_memory(self):
        """Test episodic memory storage"""
        memory = Memory()
        ctx = Context(emotion="happy")
        memory.add_episodic(ctx, "test action", "success")
        assert len(memory.episodic) == 1
        assert memory.episodic[0]["action"] == "test action"
    
    def test_memory_dump(self):
        """Test memory serialization"""
        memory = Memory()
        memory.add_semantic("concept")
        data = memory.dump()
        assert "semantic" in data
        assert "episodic" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
