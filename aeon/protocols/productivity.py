def focused(ctx):
    return ctx.intent.lower() in ["work", "study", "focus"]

def focus_action(ctx):
    return "Focus mode engaged. Distractions minimized."
