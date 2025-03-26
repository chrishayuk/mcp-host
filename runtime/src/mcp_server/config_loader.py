# src/runtime/src/mcp_server/config_loader.py
"""
Configuration Loader Module

This module provides functionality to load and manage 
configuration files for the MCP server.
"""
import os
import yaml
from typing import Dict, Any

def load_config(project_root: str) -> Dict[str, Any]:
    """
    Load server configuration from config file.
    
    Args:
        project_root: The root directory of the project.
    
    Returns:
        A dictionary containing the configuration settings.
    """
    config_paths = [
        os.path.join(project_root, "config.yaml"),
        os.path.join(project_root, "config.yml"),
        os.path.join(project_root, "runtime", "config.yaml"),
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return yaml.safe_load(f)
    
    # Default configuration if no file found
    return {
        "host": {"name": "generic-mcp", "log_level": "INFO"},
        "core": {
            "common": "common/src",
            "runtime": "runtime/src"
        },
        "mcp_servers": {
            "time_server": {
                "location": "servers/mcp_time_server/src", 
                "enabled": True,
                "tools": {
                    "module": "mcp_time_server.tools",
                    "enabled": True
                }
            },
            "echo_server": {
                "location": "servers/mcp_echo_server/src", 
                "enabled": True,
                "tools": {
                    "module": "mcp_echo_server.tools",
                    "enabled": True
                }
            },
            "telnet_client": {
                "location": "servers/mcp_telnet_client/src", 
                "enabled": True,
                "tools": {
                    "module": "mcp_telnet_client.tools",
                    "enabled": True
                }
            }
        },
        "auto_discover": True,
        "discovery": {
            "components": {
                "tools": True,
                "resources": False,
                "prompts": False
            }
        }
    }

def get_project_root() -> str:
    """
    Determine the project root directory.
    
    Returns:
        Absolute path to the project root directory.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
