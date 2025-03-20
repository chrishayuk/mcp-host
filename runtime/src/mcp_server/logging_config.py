# src/runtime/src/mcp_server/logging_config.py
"""
Logging configuration module for the MCP server.
This module sets up a shared logger with a default logging level
and a basic console handler.
"""

import logging
from logging import Logger

def get_logger(name: str = "generic_mcp_server", level: int = logging.INFO) -> Logger:
    """
    Get a configured logger with the specified name and level.
    
    Args:
        name: The name of the logger.
        level: The default logging level.
        
    Returns:
        A logger instance with a console handler attached if none exist.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create a basic console handler if none exist
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

# Create and configure the common logger for the module.
logger = get_logger()