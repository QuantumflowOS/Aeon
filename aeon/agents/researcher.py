class ResearchAgent:
    def analyze(self, protocols):
        return {
            "mean_reward": sum(p.reward for p in protocols) / len(protocols),
            "variance": sum((p.reward - 3)**2 for p in protocols),
            "protocol_count": len(protocols)
        }

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
