import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


def setup_logger(
    name: str = "app",
    level: str = "INFO",
    log_dir: str = "logs",
    json_format: bool = False
) -> logging.Logger:
    """
    Setup application logger with console and file handlers.
    
    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files
        json_format: Use JSON formatting for structured logs
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create log directory if it doesn't exist
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # Choose formatter
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Rotating file handler (10MB per file, keep 5 backup files)
    file_handler = RotatingFileHandler(
        f"{log_dir}/app.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Error file handler (separate file for errors)
    error_handler = RotatingFileHandler(
        f"{log_dir}/error.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    return logger


def setup_timed_logger(
    name: str = "app",
    level: str = "INFO",
    log_dir: str = "logs",
    when: str = "midnight",
    interval: int = 1,
    backup_count: int = 30
) -> logging.Logger:
    """
    Setup logger with time-based rotation (daily, hourly, etc.).
    
    Args:
        name: Logger name
        level: Log level
        log_dir: Directory for log files
        when: Rotation interval ('midnight', 'H' for hour, 'D' for day)
        interval: Number of intervals between rotations
        backup_count: Number of backup files to keep
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    logger.handlers.clear()
    
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Timed rotating file handler
    timed_handler = TimedRotatingFileHandler(
        f"{log_dir}/app.log",
        when=when,
        interval=interval,
        backupCount=backup_count
    )
    timed_handler.setFormatter(formatter)
    logger.addHandler(timed_handler)
    
    return logger


# Usage example
"""
from logger_config import setup_logger

# Basic setup
logger = setup_logger(name="my_app", level="INFO")

# With JSON formatting for production
logger = setup_logger(name="my_app", level="INFO", json_format=True)

# Use logger
logger.info("Application started")
logger.error("An error occurred", extra={"user_id": 123, "action": "login"})

# Time-based rotation (daily logs)
logger = setup_timed_logger(name="my_app", when="midnight", backup_count=30)
"""
