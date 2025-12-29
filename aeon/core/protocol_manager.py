# aeon/core/protocol_manager.py

class ProtocolManager:
    """
    Manages a collection of protocols and selects the best one for a given context.
    """
    
    def __init__(self):
        self.protocols = []
    
    def register(self, protocol):
        """Register a new protocol."""
        if protocol not in self.protocols:
            self.protocols.append(protocol)
    
    def best(self, context):
        """
        Find the best matching protocol for the given context.
        Returns the protocol with highest reward among those that match.
        """
        matches = [p for p in self.protocols if p.matches(context)]
        
        if not matches:
            return None
        
        # Return protocol with highest reward
        return max(matches, key=lambda p: p.reward)
    
    def get_protocols(self):
        """
        Return all protocols as a list of dicts for serialization.
        """
        return [
            {
                "name": p.name,
                "reward": p.reward,
                "executions": p.executions
            }
            for p in self.protocols
        ]
    
    def get_protocol_by_name(self, name):
        """Get a specific protocol by name."""
        for protocol in self.protocols:
            if protocol.name == name:
                return protocol
        return None
    
    def remove_protocol(self, name):
        """Remove a protocol by name."""
        self.protocols = [p for p in self.protocols if p.name != name]
    
    def __len__(self):
        """Return number of registered protocols."""
        return len(self.protocols)
    
    def __repr__(self):
        return f"ProtocolManager({len(self.protocols)} protocols)"
