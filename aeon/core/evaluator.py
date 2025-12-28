class Evaluator:
    """
    Analyzes protocol performance over time.
    """

    def evaluate(self, protocol):
        if protocol.executions < 3:
            return "insufficient_data"

        if protocol.reward >= 4:
            return "excellent"

        if protocol.reward >= 2:
            return "acceptable"

        return "poor"
