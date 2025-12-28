class ProtocolManager:
    def __init__(self):
        self.protocols = []

    def register(self, protocol):
        self.protocols.append(protocol)

    def best(self, context):
        matches = [p for p in self.protocols if p.matches(context)]
        return max(matches, key=lambda p: p.reward) if matches else None
