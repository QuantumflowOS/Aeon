# aeon/gui.py
import tkinter as tk
from tkinter import messagebox, scrolledtext
from aeon.core.context import Context
from aeon.core.protocol import Protocol
from aeon.core.protocol_manager import ProtocolManager
from aeon.core.memory import Memory
from aeon.core.agent import Agent
from aeon.protocols.emotional import happy, sad, create, comfort
from aeon.protocols.productivity import focused, focus_action


class AEONGUI:
    def __init__(self, root):
        self.root = root
        
        # Initialize components
        self.context = Context()
        self.pm = ProtocolManager()
        self.memory = Memory()

        # Register protocols
        self.pm.register(Protocol("Happy", happy, create, 3))
        self.pm.register(Protocol("Sad", sad, comfort, 2))
        self.pm.register(Protocol("Focus", focused, focus_action, 3))

        # Create agent
        self.agent = Agent(self.context, self.pm, memory=self.memory)

        # Setup GUI
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        self.root.title("ÆEON Control Panel")
        self.root.geometry("600x500")
        
        # Emotion input
        tk.Label(self.root, text="Emotion:", font=("Arial", 12)).pack(pady=(10, 0))
        self.emotion_entry = tk.Entry(self.root, font=("Arial", 11), width=40)
        self.emotion_entry.pack(pady=5)
        self.emotion_entry.insert(0, "neutral")
        
        # Intent input
        tk.Label(self.root, text="Intent:", font=("Arial", 12)).pack(pady=(10, 0))
        self.intent_entry = tk.Entry(self.root, font=("Arial", 11), width=40)
        self.intent_entry.pack(pady=5)
        self.intent_entry.insert(0, "none")
        
        # Environment input
        tk.Label(self.root, text="Environment:", font=("Arial", 12)).pack(pady=(10, 0))
        self.env_entry = tk.Entry(self.root, font=("Arial", 11), width=40)
        self.env_entry.pack(pady=5)
        self.env_entry.insert(0, "default")
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)
        
        # Run button
        self.run_button = tk.Button(
            button_frame, 
            text="Run Agent", 
            command=self.run,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5
        )
        self.run_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        self.clear_button = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_output,
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            padx=20,
            pady=5
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Memory button
        self.memory_button = tk.Button(
            button_frame,
            text="View Memory",
            command=self.show_memory,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=5
        )
        self.memory_button.pack(side=tk.LEFT, padx=5)
        
        # Output text area
        tk.Label(self.root, text="Output:", font=("Arial", 12)).pack(pady=(10, 0))
        self.output_text = scrolledtext.ScrolledText(
            self.root,
            height=12,
            width=70,
            font=("Courier", 10),
            wrap=tk.WORD
        )
        self.output_text.pack(pady=5, padx=10)

    def run(self):
        """Run the agent with current context"""
        # Update context
        emotion = self.emotion_entry.get()
        intent = self.intent_entry.get()
        environment = self.env_entry.get()
        
        self.context.update(
            emotion=emotion,
            intent=intent,
            environment=environment
        )
        
        # Run agent
        result = self.agent.run()
        
        # Display result
        self.output_text.insert(tk.END, "=" * 60 + "\n")
        self.output_text.insert(tk.END, f"Context: {self.context.to_dict()}\n")
        self.output_text.insert(tk.END, "-" * 60 + "\n")
        self.output_text.insert(tk.END, f"Thought: {result.get('thought', 'N/A')}\n")
        self.output_text.insert(tk.END, f"Protocol: {result.get('protocol', 'N/A')}\n")
        self.output_text.insert(tk.END, f"Action: {result.get('action', 'N/A')}\n")
        self.output_text.insert(tk.END, f"Reward: {result.get('reward', 'N/A')}\n")
        self.output_text.insert(tk.END, "=" * 60 + "\n\n")
        
        # Auto-scroll to bottom
        self.output_text.see(tk.END)
    
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
    
    def show_memory(self):
        """Show memory in a popup window"""
        mem_data = self.memory.dump()
        
        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title("Memory Viewer")
        popup.geometry("500x400")
        
        # Create text widget
        text = scrolledtext.ScrolledText(popup, width=60, height=20, font=("Courier", 9))
        text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Display semantic memory
        text.insert(tk.END, "=== SEMANTIC MEMORY ===\n\n")
        for item in mem_data.get('semantic', []):
            text.insert(tk.END, f"• {item['item']}\n")
            text.insert(tk.END, f"  Time: {item['timestamp']}\n\n")
        
        # Display episodic memory
        text.insert(tk.END, "\n=== EPISODIC MEMORY ===\n\n")
        for event in mem_data.get('episodic', []):
            text.insert(tk.END, f"Context: {event['context']}\n")
            text.insert(tk.END, f"Action: {event['action']}\n")
            text.insert(tk.END, f"Time: {event['timestamp']}\n")
            text.insert(tk.END, "-" * 50 + "\n\n")
        
        text.config(state=tk.DISABLED)


def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = AEONGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
