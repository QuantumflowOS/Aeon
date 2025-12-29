def network_issue(ctx):
    return "network" in ctx.intent.lower()

def resolve_network(ctx):
    return "Running diagnostics, checking routing, escalating if needed."
