import random

def happy(ctx): return ctx.emotion.lower() in ["happy", "excited"]
def sad(ctx): return ctx.emotion.lower() in ["sad", "down"]

def create(ctx):
    return random.choice([
        "Creative energy detected.",
        "Let’s build something meaningful."
    ])

def comfort(ctx):
    return random.choice([
        "It’s okay to feel this way.",
        "I’m here with you."
    ])
