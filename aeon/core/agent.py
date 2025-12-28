class Agent:
    def __init__(self, context, protocol_manager, memory):
        self.context = context
        self.pm = protocol_manager
        self.memory = memory

    def run(self):
        protocol = self.pm.best(self.context)
        if protocol:
            response = protocol.execute(self.context)
            self.memory.store(self.context)
            return response
        return "No protocol matched."
