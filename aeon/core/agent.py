from aeon.memory.episodic import EpisodicMemory
from aeon.memory.semantic import SemanticMemory

class Agent:
    def __init__(self, context, protocol_manager):
        self.context = context
        self.pm = protocol_manager
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()

    def run(self):
        protocol = self.pm.best(self.context)
        if protocol:
            action = protocol.execute(self.context)
        else:
            action = "Default support engaged."

        self.episodic.store(self.context, action)
        self.semantic.add(action)

        return action
