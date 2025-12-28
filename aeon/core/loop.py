import time
from aeon.agents.planner import PlannerAgent
from aeon.agents.executor import ExecutorAgent
from aeon.agents.reflector import ReflectorAgent


class AutonomousLoop:
    def __init__(self, agent, protocol_manager):
        self.agent = agent
        self.pm = protocol_manager
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent(agent)
        self.reflector = ReflectorAgent()

    def run_goal(self, goal: str, delay=1):
        steps = self.planner.plan(goal)
        results = []

        for step in steps:
            result = self.executor.execute_step(step)
            protocol = self.pm.best(self.agent.context)

            success = "No protocol" not in result
            self.reflector.reflect(protocol, success)

            results.append({
                "step": step,
                "result": result,
                "reward": protocol.reward if protocol else None
            })

            time.sleep(delay)

        return results
