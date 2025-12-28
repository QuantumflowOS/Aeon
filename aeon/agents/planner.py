class PlannerAgent:
    """
    Breaks a high-level goal into executable steps.
    """

    def plan(self, goal: str):
        # Simple deterministic planner (LLM can replace later)
        steps = []

        if "focus" in goal.lower():
            steps = [
                "Reduce distractions",
                "Create task structure",
                "Execute focused work block"
            ]
        elif "feel better" in goal.lower():
            steps = [
                "Acknowledge emotion",
                "Provide emotional support",
                "Stabilize mood"
            ]
        else:
            steps = [
                "Understand goal",
                "Choose best protocol",
                "Execute response"
            ]

        return steps
