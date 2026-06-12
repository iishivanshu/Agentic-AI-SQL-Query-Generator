# Logger Module
# Configures logging for the application
"""
Centralized logging configuration.
"""

import logging
import sys


def setup_logger(name: str = "agentic_sql_ai") -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


# Create default logger instance
logger = setup_logger()