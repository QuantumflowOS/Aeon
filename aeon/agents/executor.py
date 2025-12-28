class ExecutorAgent:
    """
    Executes one step using AEON protocols.
    """

    def __init__(self, agent):
        self.agent = agent

    def execute_step(self, step: str):
        # For now, execution == normal agent run
        return self.agent.run()
