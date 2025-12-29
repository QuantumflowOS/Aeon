class AEONNode:
    def __init__(self, node_id, registry):
        self.node_id = node_id
        self.registry = registry

    def sync(self, other_node):
        self.registry.protocols.update(other_node.registry.protocols)
