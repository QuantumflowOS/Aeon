from aeon.core.cognition import CognitionEngine

class Agent:
    def __init__(self, context, protocol_manager, memory):
        self.context = context
        self.pm = protocol_manager
        self.memory = memory
        self.cognition = CognitionEngine()

    def run(self):
        thought = self.cognition.think(self.context)

        protocol = self.pm.best(self.context)
        if protocol:
            response = protocol.execute(self.context)
        else:
            response = "No protocol matched. Default support engaged."

        self.memory.store(self.context)

        return f"""🧠 Thought:
{thought}

🤖 Action:
{response}
"""
