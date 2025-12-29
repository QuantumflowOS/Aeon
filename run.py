#!/usr/bin/env python3
"""
AEON Main Entry Point
Provides multiple ways to run the system
"""

import sys
import argparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def run_api(host="127.0.0.1", port=8000):
    """Start the FastAPI server"""
    import uvicorn
    from aeon.api.main import app
    
    print(f"🚀 Starting AEON API server on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)


def run_streamlit():
    """Start the Streamlit dashboard"""
    import os
    import subprocess
    
    print("🎨 Starting AEON Streamlit Dashboard")
    subprocess.run(["streamlit", "run", "app.py"])


def run_gui():
    """Start the Tkinter GUI"""
    import tkinter as tk
    from aeon.gui import AEONGUI
    
    print("🖥️  Starting AEON GUI")
    root = tk.Tk()
    app = AEONGUI(root)
    root.mainloop()


def run_demo():
    """Run a simple demonstration"""
    from aeon.core.agent import Agent
    from aeon.core.context import Context
    from aeon.core.protocol import Protocol
    from aeon.core.protocol_manager import ProtocolManager
    from aeon.core.memory import Memory
    from aeon.protocols.emotional import happy, sad, create, comfort
    from aeon.protocols.productivity import focused, focus_action
    
    print("🤖 Running AEON Demo\n")
    
    # Setup
    ctx = Context(emotion="happy", intent="create")
    pm = ProtocolManager()
    memory = Memory()
    
    # Register protocols
    pm.register(Protocol("Happy", happy, create, 3.0))
    pm.register(Protocol("Sad", sad, comfort, 2.0))
    pm.register(Protocol("Focus", focused, focus_action, 3.0))
    
    # Create agent
    agent = Agent(context=ctx, protocol_manager=pm, memory=memory)
    
    # Run scenarios
    print("Scenario 1: Happy & Creative")
    print("-" * 40)
    ctx.update(emotion="happy", intent="create")
    result = agent.run()
    print(f"Thought: {result['thought']}")
    print(f"Protocol: {result['protocol']}")
    print(f"Action: {result['action']}\n")
    
    print("Scenario 2: Sad & Need Comfort")
    print("-" * 40)
    ctx.update(emotion="sad", intent="talk")
    result = agent.run()
    print(f"Thought: {result['thought']}")
    print(f"Protocol: {result['protocol']}")
    print(f"Action: {result['action']}\n")
    
    print("Scenario 3: Focused & Productive")
    print("-" * 40)
    ctx.update(emotion="neutral", intent="work")
    result = agent.run()
    print(f"Thought: {result['thought']}")
    print(f"Protocol: {result['protocol']}")
    print(f"Action: {result['action']}\n")
    
    print("Memory Summary:")
    print("-" * 40)
    mem_data = memory.dump()
    print(f"Episodic memories: {len(mem_data['episodic'])}")
    for i, event in enumerate(mem_data['episodic'], 1):
        print(f"  {i}. Context: {event['context']}")
        print(f"     Action: {event['action']}")


def main():
    parser = argparse.ArgumentParser(
        description="AEON - Autonomous Evolving Orchestration Network"
    )
    parser.add_argument(
        'mode',
        choices=['api', 'streamlit', 'gui', 'demo'],
        help='Run mode: api (REST server), streamlit (web dashboard), gui (desktop), demo (showcase)'
    )
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='API server host (default: 127.0.0.1)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='API server port (default: 8000)'
    )
    
    args = parser.parse_args()
    
    try:
        if args.mode == 'api':
            run_api(args.host, args.port)
        elif args.mode == 'streamlit':
            run_streamlit()
        elif args.mode == 'gui':
            run_gui()
        elif args.mode == 'demo':
            run_demo()
    except KeyboardInterrupt:
        print("\n👋 AEON shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")
        logging.exception("Fatal error")
        sys.exit(1)


if __name__ == "__main__":
    main()
