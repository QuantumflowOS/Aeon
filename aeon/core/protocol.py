# aeon/core/protocol.py

class Protocol:
    """
    A protocol represents a behavioral pattern with:
    - condition: function that checks if protocol applies
    - action: function that executes the protocol
    - reward: performance metric (updated over time)
    - executions: number of times this protocol has been run
    """
    
    def __init__(self, name, condition, action, reward=3.0):
        self.name = name
        self.condition = condition
        self.action = action
        self.reward = float(reward)
        self.executions = 0
    
    def matches(self, context):
        """Check if this protocol applies to the given context."""
        try:
            return self.condition(context)
        except Exception:
            return False
    
    def execute(self, context):
        """Execute the protocol action."""
        self.executions += 1
        try:
            return self.action(context)
        except Exception as e:
            return f"Protocol execution failed: {str(e)}"
    
    def update_reward(self, score):
        """Update reward using exponential moving average."""
        alpha = 0.3  # learning rate
        self.reward = alpha * score + (1 - alpha) * self.reward
    
    def __repr__(self):
        return f"Protocol({self.name}, reward={self.reward:.2f}, execs={self.executions})"
