# aeon/monitoring/metrics.py
"""
Production-grade monitoring and metrics collection.
"""

import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import json
from pathlib import Path


@dataclass
class Metric:
    """Individual metric data point."""
    name: str
    value: float
    timestamp: float
    tags: Dict[str, str] = None
    
    def to_dict(self):
        return asdict(self)


class MetricsCollector:
    """
    Collects and aggregates system metrics.
    """
    
    def __init__(self, retention_seconds: int = 3600):
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.retention_seconds = retention_seconds
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}
        self.timers: Dict[str, List[float]] = defaultdict(list)
    
    def increment(self, name: str, value: int = 1, tags: Dict = None):
        """Increment a counter."""
        self.counters[name] += value
        self._record(name, self.counters[name], tags)
    
    def gauge(self, name: str, value: float, tags: Dict = None):
        """Set a gauge value."""
        self.gauges[name] = value
        self._record(name, value, tags)
    
    def timing(self, name: str, duration: float, tags: Dict = None):
        """Record a timing."""
        self.timers[name].append(duration)
        self._record(name, duration, tags)
    
    def _record(self, name: str, value: float, tags: Dict = None):
        """Internal: record a metric."""
        metric = Metric(
            name=name,
            value=value,
            timestamp=time.time(),
            tags=tags or {}
        )
        self.metrics[name].append(metric)
    
    def get_metrics(self, name: str, since: float = None) -> List[Metric]:
        """Get metrics for a specific name."""
        metrics = list(self.metrics[name])
        
        if since:
            metrics = [m for m in metrics if m.timestamp >= since]
        
        return metrics
    
    def get_stats(self, name: str, window_seconds: int = 60) -> Dict:
        """Get statistics for a metric."""
        cutoff = time.time() - window_seconds
        recent_metrics = [m for m in self.metrics[name] if m.timestamp >= cutoff]
        
        if not recent_metrics:
            return {}
        
        values = [m.value for m in recent_metrics]
        
        return {
            "count": len(values),
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "latest": values[-1],
            "window_seconds": window_seconds
        }
    
    def export_prometheus(self) -> str:
        """Export metrics in Prometheus format."""
        lines = []
        
        # Counters
        for name, value in self.counters.items():
            lines.append(f"# TYPE aeon_{name} counter")
            lines.append(f"aeon_{name} {value}")
        
        # Gauges
        for name, value in self.gauges.items():
            lines.append(f"# TYPE aeon_{name} gauge")
            lines.append(f"aeon_{name} {value}")
        
        return "\n".join(lines)
    
    def cleanup_old_metrics(self):
        """Remove metrics older than retention period."""
        cutoff = time.time() - self.retention_seconds
        
        for name in list(self.metrics.keys()):
            self.metrics[name] = deque(
                [m for m in self.metrics[name] if m.timestamp >= cutoff],
                maxlen=1000
            )


class PerformanceMonitor:
    """
    Monitor performance of operations using context managers.
    """
    
    def __init__(self, metrics: MetricsCollector):
        self.metrics = metrics
        self.active_operations: Dict[str, float] = {}
    
    def __call__(self, operation_name: str):
        """Use as context manager."""
        return self._OperationTimer(self, operation_name)
    
    class _OperationTimer:
        def __init__(self, monitor: 'PerformanceMonitor', operation_name: str):
            self.monitor = monitor
            self.operation_name = operation_name
            self.start_time = None
        
        def __enter__(self):
            self.start_time = time.time()
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            duration = time.time() - self.start_time
            self.monitor.metrics.timing(
                f"operation_{self.operation_name}",
                duration,
                tags={"success": exc_type is None}
            )
            
            # Track errors
            if exc_type:
                self.monitor.metrics.increment(
                    f"operation_{self.operation_name}_errors",
                    tags={"error_type": exc_type.__name__}
                )


class HealthChecker:
    """
    Performs health checks on system components.
    """
    
    def __init__(self):
        self.checks: Dict[str, callable] = {}
        self.last_results: Dict[str, Dict] = {}
    
    def register_check(self, name: str, check_func: callable):
        """Register a health check function."""
        self.checks[name] = check_func
    
    def run_check(self, name: str) -> Dict:
        """Run a specific health check."""
        if name not in self.checks:
            return {"status": "unknown", "message": "Check not found"}
        
        try:
            result = self.checks[name]()
            self.last_results[name] = {
                "status": "healthy" if result else "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "details": result if isinstance(result, dict) else {}
            }
        except Exception as e:
            self.last_results[name] = {
                "status": "error",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            }
        
        return self.last_results[name]
    
    def run_all_checks(self) -> Dict[str, Dict]:
        """Run all registered health checks."""
        results = {}
        for name in self.checks:
            results[name] = self.run_check(name)
        return results
    
    def is_healthy(self) -> bool:
        """Check if all components are healthy."""
        results = self.run_all_checks()
        return all(r["status"] == "healthy" for r in results.values())


class AuditLogger:
    """
    Logs important system events for audit trail.
    """
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.audit_file = self.log_dir / "audit.jsonl"
        self.logger = logging.getLogger("aeon.audit")
    
    def log_event(self, event_type: str, details: Dict, user: str = None):
        """Log an audit event."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "details": details,
            "user": user
        }
        
        # Write to JSONL file
        with open(self.audit_file, 'a') as f:
            f.write(json.dumps(event) + "\n")
        
        # Also log to standard logging
        self.logger.info(f"AUDIT: {event_type}", extra=event)
    
    def log_context_update(self, old_context: Dict, new_context: Dict, user: str = None):
        """Log context updates."""
        self.log_event(
            "context_update",
            {"old": old_context, "new": new_context},
            user
        )
    
    def log_protocol_execution(self, protocol_name: str, reward: float, user: str = None):
        """Log protocol execution."""
        self.log_event(
            "protocol_execution",
            {"protocol": protocol_name, "reward": reward},
            user
        )
    
    def log_system_change(self, change_type: str, details: Dict, user: str = None):
        """Log system configuration changes."""
        self.log_event(
            "system_change",
            {"change_type": change_type, **details},
            user
        )
    
    def get_recent_events(self, n: int = 100, event_type: str = None) -> List[Dict]:
        """Get recent audit events."""
        events = []
        
        if self.audit_file.exists():
            with open(self.audit_file, 'r') as f:
                for line in f:
                    try:
                        event = json.loads(line)
                        if event_type is None or event.get("event_type") == event_type:
                            events.append(event)
                    except json.JSONDecodeError:
                        continue
        
        return events[-n:]


class AlertManager:
    """
    Manages alerts based on metric thresholds.
    """
    
    def __init__(self, metrics: MetricsCollector):
        self.metrics = metrics
        self.thresholds: Dict[str, Dict] = {}
        self.alert_handlers: List[callable] = []
        self.active_alerts: Dict[str, Dict] = {}
    
    def set_threshold(self, metric_name: str, threshold: float, 
                     condition: str = "greater", duration: int = 60):
        """Set an alert threshold for a metric."""
        self.thresholds[metric_name] = {
            "threshold": threshold,
            "condition": condition,
            "duration": duration
        }
    
    def register_handler(self, handler: callable):
        """Register an alert handler function."""
        self.alert_handlers.append(handler)
    
    def check_alerts(self):
        """Check all metrics against thresholds."""
        current_time = time.time()
        
        for metric_name, config in self.thresholds.items():
            stats = self.metrics.get_stats(metric_name, window_seconds=config["duration"])
            
            if not stats:
                continue
            
            value = stats["mean"]
            threshold = config["threshold"]
            condition = config["condition"]
            
            # Check condition
            triggered = False
            if condition == "greater" and value > threshold:
                triggered = True
            elif condition == "less" and value < threshold:
                triggered = True
            elif condition == "equal" and abs(value - threshold) < 0.01:
                triggered = True
            
            # Handle alert
            if triggered and metric_name not in self.active_alerts:
                alert = {
                    "metric": metric_name,
                    "value": value,
                    "threshold": threshold,
                    "condition": condition,
                    "timestamp": current_time
                }
                self.active_alerts[metric_name] = alert
                self._trigger_alert(alert)
            
            elif not triggered and metric_name in self.active_alerts:
                # Alert resolved
                self._resolve_alert(metric_name)
    
    def _trigger_alert(self, alert: Dict):
        """Trigger an alert."""
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                logging.error(f"Alert handler error: {e}")
    
    def _resolve_alert(self, metric_name: str):
        """Resolve an active alert."""
        alert = self.active_alerts.pop(metric_name)
        logging.info(f"Alert resolved: {metric_name}")


# Global instances
metrics_collector = MetricsCollector()
performance_monitor = PerformanceMonitor(metrics_collector)
health_checker = HealthChecker()
audit_logger = AuditLogger()
alert_manager = AlertManager(metrics_collector)
