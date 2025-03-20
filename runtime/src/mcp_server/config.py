# src/runtime/src/mcp_server/config.py
import os
import yaml
import logging
from typing import Any, Dict

# Use relative import for shared logger
from .logging_config import logger

def load_config(project_root: str) -> Dict[str, Any]:
    """
    Load server configuration from one of the expected config file paths.
    
    The function searches for configuration files in the following order:
      1. <project_root>/config.yaml
      2. <project_root>/config.yml
      3. <project_root>/runtime/config.yaml

    Args:
        project_root: The root directory of the project.

    Returns:
        A dictionary containing the configuration.

    Raises:
        FileNotFoundError: If no configuration file is found in any expected location.
    """
    config_paths = [
        os.path.join(project_root, "config.yaml"),
        os.path.join(project_root, "config.yml"),
        os.path.join(project_root, "runtime", "config.yaml"),
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                logger.info(f"Loading config from {path}")
                config = yaml.safe_load(f)
                if config is None:
                    logger.warning(f"Config file {path} is empty, using empty configuration.")
                    return {}
                return config

    error_message = "No config file found in any of the expected locations."
    logger.error(error_message)
    raise FileNotFoundError(error_message)

def configure_logging(config: Dict[str, Any]) -> None:
    """
    Configure logging based on the provided configuration.
    
    This function sets the log level for both the shared logger and the root logger,
    ensuring consistent logging behavior throughout the application.

    Args:
        config: A dictionary containing the configuration settings.
    """
    log_level_str = config.get("host", {}).get("log_level", "INFO")
    level = getattr(logging, log_level_str.upper(), logging.INFO)
    logger.setLevel(level)
    logging.getLogger().setLevel(level)
    logger.info(f"Log level set to {log_level_str}")
