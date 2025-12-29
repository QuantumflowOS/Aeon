# ÆEON - Autonomous Evolving Orchestration Network

A conscious context engine for adaptive agent behavior with self-improvement capabilities.

## Features

- **Context-Aware Agents**: Responds intelligently based on emotional state, intent, and environment
- **Protocol System**: Modular behavior patterns with reward-based selection
- **Semantic Memory**: Vector-based memory for storing and querying concepts
- **Self-Improvement**: Evolutionary algorithms that adapt protocols over time
- **Multiple Interfaces**: REST API, Streamlit dashboard, and Tkinter GUI
- **LLM Integration**: Optional OpenAI integration for advanced reasoning

## Project Structure

```
aeon/
├── core/               # Core engine components
│   ├── agent.py       # Main agent logic
│   ├── context.py     # Context management
│   ├── protocol.py    # Protocol class definition
│   ├── protocol_manager.py  # Protocol selection
│   ├── protocols.py   # Simple protocol manager
│   ├── memory.py      # Memory systems
│   ├── semantic_memory.py   # Vector-based memory
│   ├── cognition.py   # Reasoning engine
│   └── __init__.py
├── api/               # FastAPI REST interface
│   ├── main.py       # API entry point
│   ├── routes.py     # Endpoint definitions
│   ├── schemas.py    # Pydantic models
│   └── __init__.py
├── protocols/         # Protocol library
│   ├── emotional.py  # Emotion-based protocols
│   ├── productivity.py  # Focus/work protocols
│   ├── automation.py # Task automation
│   └── __init__.py
├── learning/          # Self-improvement components
│   ├── evaluator.py  # Protocol performance analysis
│   ├── evolution.py  # Protocol mutation
│   ├── improver.py   # Self-improvement orchestrator
│   ├── researcher.py # Analytics
│   ├── reflector.py  # Outcome evaluation
│   └── __init__.py
└── distributed/       # Multi-agent systems
    ├── registry.py   # Central coordination
    ├── distributed.py # Node synchronization
    └── concurrency.py # Threading support
```

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Run the API Server

```bash
cd aeon
uvicorn api.main:app --reload
```

API will be available at `http://localhost:8000`

### 2. Run the Streamlit Dashboard

```bash
streamlit run app.py
```

### 3. Use the Tkinter GUI

```bash
python -m aeon.gui
```

## API Usage

### Update Context

```bash
curl -X POST http://localhost:8000/context/update \
  -H "Content-Type: application/json" \
  -d '{"emotion": "happy", "intent": "create"}'
```

### Execute Goal

```bash
curl -X POST http://localhost:8000/agent/goal \
  -H "Content-Type: application/json" \
  -d '{"goal": "organize workspace"}'
```

### View Memory

```bash
curl http://localhost:8000/memory
```

## Configuration

### OpenAI Integration (Optional)

Set environment variable for LLM-powered cognition:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Without this, AEON uses rule-based fallback reasoning.

## Core Concepts

### Context
The agent's awareness of the current situation (emotion, intent, environment)

### Protocols
Behavior patterns that match contexts and execute actions. Each has:
- **Condition**: When to activate
- **Action**: What to do
- **Reward**: Performance metric (0-5)

### Memory
- **Semantic**: Conceptual knowledge stored as vectors
- **Episodic**: Experience records (context → action → result)

### Self-Improvement
Protocols evolve based on performance:
- High performers get reinforced (reward × 1.1)
- Low performers get penalized (reward × 0.8)
- Poor protocols generate mutations

## Development

### Adding New Protocols

```python
# aeon/protocols/custom.py

def my_condition(ctx):
    return ctx.intent == "custom_task"

def my_action(ctx):
    return "Executing custom behavior"

# Register in agent
from aeon.core.protocol import Protocol
protocol = Protocol("Custom", my_condition, my_action, reward=3.0)
agent.protocol_manager.register(protocol)
```

### Running Tests

```bash
pytest tests/
```

## Architecture

AEON uses a multi-layered architecture:

1. **Context Layer**: Captures user state
2. **Cognition Layer**: Reasons about context (LLM or rule-based)
3. **Protocol Layer**: Selects and executes behaviors
4. **Memory Layer**: Stores experiences and knowledge
5. **Learning Layer**: Evolves protocols over time

## License

MIT License - See LICENSE file

## Contributing

Contributions welcome! Please open an issue or submit a PR.

## Roadmap

- [ ] FAISS integration for semantic memory
- [ ] Reinforcement learning for protocol optimization
- [ ] Multi-agent coordination
- [ ] Web-based admin dashboard
- [ ] Plugin system for custom protocols
- [ ] Distributed deployment support
