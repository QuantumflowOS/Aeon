import logging

class Context:
    def __init__(self, emotion="neutral", intent="none", environment="default"):
        self.emotion = emotion
        self.intent = intent
        self.environment = environment
        logging.info(f"Context initialized: {self.to_dict()}")

    def update(self, emotion=None, intent=None, environment=None):
        if emotion: self.emotion = emotion
        if intent: self.intent = intent
        if environment: self.environment = environment
        logging.info(f"Context updated: {self.to_dict()}")

    def to_dict(self):
        return {
            "emotion": self.emotion,
            "intent": self.intent,
            "environment": self.environment
        }

    def from_dict(self, d):
        self.emotion = d.get("emotion", self.emotion)
        self.intent = d.get("intent", self.intent)
        self.environment = d.get("environment", self.environment)
