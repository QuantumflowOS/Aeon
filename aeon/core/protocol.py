import logging

class Protocol:
    def __init__(self, name, trigger, action, reward=0):
        self.name = name
        self.trigger = trigger
        self.action = action
        self.reward = reward
        self.executions = 0

    def matches(self, context):
        try:
            return self.trigger(context)
        except Exception as e:
            logging.error(f"Trigger error ({self.name}): {e}")
            return False

    def execute(self, context):
        self.executions += 1
        return self.action(context)

    def update_reward(self, score):
        self.reward = (self.reward * 0.7) + (score * 0.3)
