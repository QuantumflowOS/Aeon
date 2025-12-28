import json

class Memory:
    def __init__(self):
        self.sessions = []

    def store(self, context):
        self.sessions.append(context.to_dict())

    def save(self, path):
        with open(path, "w") as f:
            json.dump(self.sessions, f, indent=2)

    def load(self, path):
        with open(path) as f:
            self.sessions = json.load(f)
