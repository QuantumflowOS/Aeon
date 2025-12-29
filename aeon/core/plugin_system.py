# aeon/core/plugin_system.py
"""
Plugin system for extending AEON functionality.
Allows loading custom protocols, memory backends, and cognitive engines.
"""

import importlib
import inspect
import logging
from pathlib import Path
from typing import Dict, List, Type, Any, Callable
from abc import ABC, abstractmethod


class Plugin(ABC):
    """Base class for all plugins."""
    
    name: str = "base_plugin"
    version: str = "0.1.0"
    description: str = "Base plugin"
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]):
        """Initialize the plugin with configuration."""
        pass
    
    @abstractmethod
    def cleanup(self):
        """Cleanup when plugin is unloaded."""
        pass


class ProtocolPlugin(Plugin):
    """Plugin for custom protocols."""
    
    @abstractmethod
    def get_protocols(self) -> List:
        """Return list of Protocol instances."""
        pass


class MemoryPlugin(Plugin):
    """Plugin for custom memory backends."""
    
    @abstractmethod
    def store(self, data: Any):
        """Store data in memory."""
        pass
    
    @abstractmethod
    def retrieve(self, query: Any) -> List:
        """Retrieve data from memory."""
        pass


class CognitivePlugin(Plugin):
    """Plugin for custom cognitive engines."""
    
    @abstractmethod
    def think(self, context: Any) -> str:
        """Process context and return thought."""
        pass


class PluginManager:
    """
    Manages plugin lifecycle: discovery, loading, initialization, and cleanup.
    """
    
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.loaded_plugins: Dict[str, Plugin] = {}
        self.plugin_types: Dict[str, Type[Plugin]] = {
            "protocol": ProtocolPlugin,
            "memory": MemoryPlugin,
            "cognitive": CognitivePlugin
        }
        
        # Create plugin directory if it doesn't exist
        self.plugin_dir.mkdir(parents=True, exist_ok=True)
        logging.info(f"Plugin manager initialized. Directory: {self.plugin_dir}")
    
    def discover_plugins(self) -> List[str]:
        """Discover available plugins in plugin directory."""
        plugins = []
        
        for py_file in self.plugin_dir.glob("*.py"):
            if py_file.name.startswith("_"):
                continue
            plugins.append(py_file.stem)
        
        logging.info(f"Discovered {len(plugins)} plugins: {plugins}")
        return plugins
    
    def load_plugin(self, plugin_name: str, config: Dict[str, Any] = None) -> Plugin:
        """Load and initialize a plugin."""
        if plugin_name in self.loaded_plugins:
            logging.warning(f"Plugin {plugin_name} already loaded")
            return self.loaded_plugins[plugin_name]
        
        try:
            # Import plugin module
            module_path = f"{self.plugin_dir.name}.{plugin_name}"
            module = importlib.import_module(module_path)
            
            # Find plugin class
            plugin_class = None
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, Plugin) and obj != Plugin and not inspect.isabstract(obj):
                    plugin_class = obj
                    break
            
            if not plugin_class:
                raise ValueError(f"No valid plugin class found in {plugin_name}")
            
            # Instantiate and initialize
            plugin = plugin_class()
            plugin.initialize(config or {})
            
            self.loaded_plugins[plugin_name] = plugin
            logging.info(f"✅ Loaded plugin: {plugin.name} v{plugin.version}")
            return plugin
            
        except Exception as e:
            logging.error(f"❌ Failed to load plugin {plugin_name}: {e}")
            raise
    
    def unload_plugin(self, plugin_name: str):
        """Unload a plugin and cleanup."""
        if plugin_name not in self.loaded_plugins:
            logging.warning(f"Plugin {plugin_name} not loaded")
            return
        
        plugin = self.loaded_plugins[plugin_name]
        plugin.cleanup()
        del self.loaded_plugins[plugin_name]
        logging.info(f"Unloaded plugin: {plugin_name}")
    
    def get_plugin(self, plugin_name: str) -> Plugin:
        """Get a loaded plugin."""
        return self.loaded_plugins.get(plugin_name)
    
    def list_plugins(self) -> Dict[str, Dict[str, str]]:
        """List all loaded plugins with their info."""
        return {
            name: {
                "name": plugin.name,
                "version": plugin.version,
                "description": plugin.description,
                "type": type(plugin).__name__
            }
            for name, plugin in self.loaded_plugins.items()
        }
    
    def reload_plugin(self, plugin_name: str, config: Dict[str, Any] = None):
        """Reload a plugin (useful for development)."""
        if plugin_name in self.loaded_plugins:
            self.unload_plugin(plugin_name)
        return self.load_plugin(plugin_name, config)
    
    def cleanup_all(self):
        """Cleanup all plugins."""
        for plugin_name in list(self.loaded_plugins.keys()):
            self.unload_plugin(plugin_name)


# ============================================
# Example Plugin Implementations
# ============================================

# plugins/weather_protocol.py
"""
Example: Weather-aware protocol plugin
"""

class WeatherProtocol(ProtocolPlugin):
    name = "weather_protocol"
    version = "1.0.0"
    description = "Adapts behavior based on weather conditions"
    
    def __init__(self):
        self.protocols = []
    
    def initialize(self, config: Dict[str, Any]):
        from aeon.core.protocol import Protocol
        
        # Rainy day protocol
        def rainy_condition(ctx):
            return hasattr(ctx, 'weather') and 'rain' in ctx.weather.lower()
        
        def rainy_action(ctx):
            return "It's rainy! Suggesting indoor activities and cozy atmosphere."
        
        # Sunny day protocol
        def sunny_condition(ctx):
            return hasattr(ctx, 'weather') and 'sunny' in ctx.weather.lower()
        
        def sunny_action(ctx):
            return "Beautiful sunny day! Encouraging outdoor activities."
        
        self.protocols = [
            Protocol("RainyDay", rainy_condition, rainy_action, reward=3.5),
            Protocol("SunnyDay", sunny_condition, sunny_action, reward=4.0)
        ]
        
        logging.info("Weather protocols initialized")
    
    def get_protocols(self) -> List:
        return self.protocols
    
    def cleanup(self):
        self.protocols = []


# plugins/redis_memory.py
"""
Example: Redis-backed memory plugin
"""

class RedisMemory(MemoryPlugin):
    name = "redis_memory"
    version = "1.0.0"
    description = "Redis-backed persistent memory"
    
    def __init__(self):
        self.client = None
    
    def initialize(self, config: Dict[str, Any]):
        try:
            import redis
            host = config.get("host", "localhost")
            port = config.get("port", 6379)
            self.client = redis.Redis(host=host, port=port, decode_responses=True)
            self.client.ping()
            logging.info(f"Connected to Redis at {host}:{port}")
        except Exception as e:
            logging.error(f"Failed to connect to Redis: {e}")
            self.client = None
    
    def store(self, data: Any):
        if not self.client:
            return
        
        import json
        from datetime import datetime
        
        key = f"memory:{datetime.utcnow().isoformat()}"
        self.client.set(key, json.dumps(data))
        self.client.expire(key, 86400)  # 24 hour TTL
    
    def retrieve(self, query: Any) -> List:
        if not self.client:
            return []
        
        import json
        keys = self.client.keys("memory:*")
        results = []
        
        for key in keys[-10:]:  # Last 10 items
            data = self.client.get(key)
            if data:
                results.append(json.loads(data))
        
        return results
    
    def cleanup(self):
        if self.client:
            self.client.close()


# plugins/gpt4_cognition.py
"""
Example: GPT-4 cognitive plugin
"""

class GPT4Cognition(CognitivePlugin):
    name = "gpt4_cognition"
    version = "1.0.0"
    description = "GPT-4 powered cognitive reasoning"
    
    def __init__(self):
        self.client = None
    
    def initialize(self, config: Dict[str, Any]):
        try:
            from openai import OpenAI
            api_key = config.get("api_key")
            self.client = OpenAI(api_key=api_key)
            logging.info("GPT-4 cognitive engine initialized")
        except Exception as e:
            logging.error(f"Failed to initialize GPT-4: {e}")
    
    def think(self, context: Any) -> str:
        if not self.client:
            return "Cognition engine not available"
        
        prompt = f"""
        Analyze this context and provide reasoning:
        Emotion: {getattr(context, 'emotion', 'unknown')}
        Intent: {getattr(context, 'intent', 'unknown')}
        Environment: {getattr(context, 'environment', 'unknown')}
        
        What's the best approach to support this user?
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"GPT-4 error: {e}")
            return "Error in cognitive processing"
    
    def cleanup(self):
        self.client = None
