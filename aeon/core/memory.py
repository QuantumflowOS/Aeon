# aeon/core/memory.py

from datetime import datetime

class Memory:
    """
    Combined memory system with semantic and episodic components.
    """
    
    def __init__(self):
        self.semantic = []  # conceptual knowledge
        self.episodic = []  # experience records
    
    def add_semantic(self, item):
        """Add a semantic memory item."""
        self.semantic.append({
            "timestamp": datetime.utcnow().isoformat(),
            "item": item
        })
    
    def add_episodic(self, context, action, result=None):
        """Add an episodic memory (experience)."""
        self.episodic.append({
            "timestamp": datetime.utcnow().isoformat(),
            "context": {
                "emotion": getattr(context, 'emotion', 'unknown'),
                "intent": getattr(context, 'intent', 'unknown'),
                "environment": getattr(context, 'environment', 'unknown')
            },
            "action": action,
            "result": result
        })
    
    def get_semantic(self):
        """Return all semantic memories."""
        return self.semantic
    
    def get_episodic(self):
        """Return all episodic memories."""
        return self.episodic
    
    def dump(self):
        """Return all memory as JSON-serializable dict."""
        return {
            "semantic": self.semantic,
            "episodic": self.episodic
        }


class SemanticMemory:
    """
    Standalone semantic memory for backward compatibility.
    """
    def __init__(self):
        self.data = []

    def add(self, item):
        """Add a new memory item with timestamp."""
        self.data.append({
            "timestamp": datetime.utcnow().isoformat(),
            "item": item
        })

    def dump(self):
        """Return JSON-serializable representation."""
        return self.data
