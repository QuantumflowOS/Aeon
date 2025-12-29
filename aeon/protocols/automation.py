def network_issue(ctx):
    return "network" in ctx.intent.lower()

def resolve_network(ctx):
    return "Running diagnostics, checking routing, escalating if needed."

def crm_ticket(ctx):
    return "ticket" in ctx.intent.lower()

def create_ticket(ctx):
    return "CRM ticket created, priority assigned."
