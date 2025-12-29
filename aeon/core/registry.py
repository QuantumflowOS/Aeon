class AEONRegistry:
    """
    Central nervous system of AEON.
    Tracks agents, protocols, memory, metrics.
    """

    def __init__(self):
        self.agents = {}
        self.protocols = {}
        self.metrics = {
            "goals_completed": 0,
            "protocol_mutations": 0,
            "learning_cycles": 0
        }

    # ----- AGENTS -----
    def register_agent(self, name, agent):
        self.agents[name] = agent

    # ----- PROTOCOLS -----
    def register_protocol(self, protocol):
        self.protocols[protocol.name] = protocol

    def all_protocols(self):
        return list(self.protocols.values())

    # ----- METRICS -----
    def record_goal(self):
        self.metrics["goals_completed"] += 1

    def record_learning(self):
        self.metrics["learning_cycles"] += 1

    def record_mutation(self):
        self.metrics["protocol_mutations"] += 1
