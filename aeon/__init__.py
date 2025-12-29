# aeon/__init__.py
"""
AEON - Autonomous Evolving Orchestration Network
A conscious context engine for adaptive agent behavior.
"""

__version__ = "0.1.0"

# ============================================
# aeon/core/__init__.py
"""Core AEON components"""

from .agent import Agent
from .context import Context
from .protocol import Protocol
from .protocol_manager import ProtocolManager
from .memory import Memory, SemanticMemory
from .cognition import CognitionEngine

__all__ = [
    'Agent',
    'Context',
    'Protocol',
    'ProtocolManager',
    'Memory',
    'SemanticMemory',
    'CognitionEngine'
]

# ============================================
# aeon/api/__init__.py
"""AEON API components"""

from .main import app

__all__ = ['app']

# ============================================
# aeon/protocols/__init__.py
"""Protocol library for AEON agents"""

from . import emotional
from . import productivity
from . import automation

__all__ = ['emotional', 'productivity', 'automation']

# ============================================
# aeon/learning/__init__.py
"""Learning and self-improvement components"""

from .evaluator import Evaluator
from .evolution import ProtocolEvolution
from .improver import SelfImprover
from .researcher import ResearchAgent
from .reflector import ReflectorAgent

__all__ = [
    'Evaluator',
    'ProtocolEvolution',
    'SelfImprover',
    'ResearchAgent',
    'ReflectorAgent'
]
