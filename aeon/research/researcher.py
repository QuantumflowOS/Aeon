class ResearchAgent:
    def analyze(self, protocols):
        """
        Analyze protocols and return statistics and detailed report.
        """
        if not protocols:
            return {
                "mean_reward": 0,
                "variance": 0,
                "protocol_count": 0,
                "hypothesis": "Insufficient data",
                "data": []
            }
        
        # Calculate statistics
        mean_reward = sum(p.reward for p in protocols) / len(protocols)
        variance = sum((p.reward - mean_reward)**2 for p in protocols) / len(protocols)
        
        # Build detailed report
        report = []
        for p in protocols:
            report.append({
                "protocol": p.name,
                "reward": round(p.reward, 3),
                "executions": p.executions
            })

        return {
            "mean_reward": round(mean_reward, 3),
            "variance": round(variance, 3),
            "protocol_count": len(protocols),
            "hypothesis": "Reward-weighted protocol selection converges",
            "data": report
        }
