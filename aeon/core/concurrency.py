import threading

class AgentThread(threading.Thread):
    def __init__(self, name, agent, goal):
        super().__init__()
        self.name = name
        self.agent = agent
        self.goal = goal
        self.result = None

    def run(self):
        self.result = self.agent.run()
