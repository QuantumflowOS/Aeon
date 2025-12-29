class ResearchAgent:
    """
    Observes system behavior and extracts insights.
    """

    def analyze(self, protocols):
        report = []

        for p in protocols:
            report.append({
                "protocol": p.name,
                "reward": round(p.reward, 3),
                "executions": p.executions
            })

        return {
            "hypothesis": "Reward-weighted protocol selection converges",
            "data": report
        }
