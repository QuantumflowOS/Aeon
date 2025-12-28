import tkinter as tk
from tkinter import messagebox
from aeon.core.context import Context
from aeon.core.protocol import Protocol
from aeon.core.protocol_manager import ProtocolManager
from aeon.core.memory import Memory
from aeon.core.agent import Agent
from aeon.protocols.emotional import happy, sad, create, comfort
from aeon.protocols.productivity import focused, focus_action

class AEONGUI:
    def __init__(self, root):
        self.context = Context()
        self.pm = ProtocolManager()
        self.memory = Memory()

        self.pm.register(Protocol("Happy", happy, create, 3))
        self.pm.register(Protocol("Sad", sad, comfort, 2))
        self.pm.register(Protocol("Focus", focused, focus_action, 3))

        self.agent = Agent(self.context, self.pm, self.memory)

        root.title("ÆON")
        self.e = tk.Entry(root); self.e.pack()
        self.i = tk.Entry(root); self.i.pack()
        self.b = tk.Button(root, text="Run", command=self.run); self.b.pack()
        self.t = tk.Text(root, height=6); self.t.pack()

    def run(self):
        self.context.update(
            emotion=self.e.get(),
            intent=self.i.get()
        )
        r = self.agent.run()
        self.t.delete(1.0, tk.END)
        self.t.insert(tk.END, r)
