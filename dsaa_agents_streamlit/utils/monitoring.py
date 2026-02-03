"""
Monitoring and logging utilities for DSAA Agents application.
Provides structured logging, metrics tracking, and alerting hooks.
"""

import logging
import json
import time
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional
import streamlit as st

# Configure logging
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Structured JSON logger
class JSONFormatter(logging.Formatter):
    """Format log records as JSON for easy parsing."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if hasattr(record, "extra_data"):
            log_obj["data"] = record.extra_data
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)


def setup_logging(name: str = "dsaa_agents", level: int = logging.INFO) -> logging.Logger:
    """
    Set up structured logging with both file and console handlers.

    Args:
        name: Logger name
        level: Logging level

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # File handler (JSON format)
    file_handler = logging.FileHandler(LOG_DIR / f"{name}.log")
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)

    # Console handler (simple format)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(console_handler)

    return logger


# Global logger instance
logger = setup_logging()


class MetricsTracker:
    """Track application metrics and usage statistics."""

    def __init__(self):
        self.metrics_file = LOG_DIR / "metrics.jsonl"

    def track(self, event: str, data: Optional[dict] = None):
        """
        Track a metric event.

        Args:
            event: Event name (e.g., "page_view", "diagram_rendered")
            data: Additional event data
        """
        metric = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "data": data or {},
            "session_id": self._get_session_id(),
        }

        # Append to metrics file
        with open(self.metrics_file, "a") as f:
            f.write(json.dumps(metric) + "\n")

        logger.info(f"Metric tracked: {event}", extra={"extra_data": data})

    def _get_session_id(self) -> str:
        """Get or create session ID from Streamlit session state."""
        if "session_id" not in st.session_state:
            import uuid
            st.session_state.session_id = str(uuid.uuid4())[:8]
        return st.session_state.session_id

    def get_metrics_summary(self) -> dict:
        """Get summary of tracked metrics."""
        if not self.metrics_file.exists():
            return {"total_events": 0, "events_by_type": {}}

        events_by_type = {}
        total = 0

        with open(self.metrics_file, "r") as f:
            for line in f:
                try:
                    metric = json.loads(line.strip())
                    event = metric.get("event", "unknown")
                    events_by_type[event] = events_by_type.get(event, 0) + 1
                    total += 1
                except json.JSONDecodeError:
                    continue

        return {
            "total_events": total,
            "events_by_type": events_by_type,
        }


# Global metrics tracker
metrics = MetricsTracker()


def track_time(event_name: str):
    """
    Decorator to track execution time of functions.

    Args:
        event_name: Name for the timing event
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            metrics.track(f"{event_name}_duration", {"duration_ms": round(duration * 1000, 2)})
            return result
        return wrapper
    return decorator


def log_page_view(page_name: str):
    """Log a page view event."""
    metrics.track("page_view", {"page": page_name})


def log_diagram_render(diagram_type: str, filters: Optional[dict] = None):
    """Log a diagram render event."""
    metrics.track("diagram_rendered", {
        "diagram_type": diagram_type,
        "filters": filters,
    })


def log_diagram_export(diagram_type: str, format: str):
    """Log a diagram export event."""
    metrics.track("diagram_exported", {
        "diagram_type": diagram_type,
        "format": format,
    })


def log_error(error: Exception, context: Optional[dict] = None):
    """Log an error event."""
    logger.error(
        f"Error: {str(error)}",
        exc_info=True,
        extra={"extra_data": context or {}},
    )
    metrics.track("error", {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context,
    })
