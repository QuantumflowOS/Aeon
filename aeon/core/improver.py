from aeon.core.evaluator import Evaluator
import logging
from aeon.core.evolution import ProtocolEvolution

self.evolver = ProtocolEvolution()
mutants = self.evolver.evolve(self.pm.protocols)
for m in mutants:
    self.pm.register(m)

class SelfImprover:
    """
    Modifies system behavior based on evaluation.
    """

    def __init__(self, protocol_manager):
        self.pm = protocol_manager
        self.evaluator = Evaluator()

    def improve(self):
        report = []

        for protocol in self.pm.protocols:
            status = self.evaluator.evaluate(protocol)

            if status == "poor":
                # Penalize underperforming protocols
                protocol.reward *= 0.8
                logging.warning(f"Protocol degraded: {protocol.name}")

            elif status == "excellent":
                # Reinforce strong protocols
                protocol.reward *= 1.1
                logging.info(f"Protocol reinforced: {protocol.name}")

            report.append({
                "protocol": protocol.name,
                "status": status,
                "reward": round(protocol.reward, 2),
                "executions": protocol.executions
            })

        return report
