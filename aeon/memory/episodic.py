import json
from datetime import datetime

class EpisodicMemory:
    def __init__(self):
        self.events = []

    def store(self, context, result):
        self.events.append({
            "timestamp": datetime.utcnow().isoformat(),
            "context": context.to_dict(),
            "result": result
        })

    def dump(self, path):
        with open(path, "w") as f:
            json.dump(self.events, f, indent=2)
