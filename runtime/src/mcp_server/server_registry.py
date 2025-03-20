# runtime/src/mcp_server/server_registry.py
"""
Server Registry Module for MCP Tool Servers

This module provides a ServerRegistry class for managing 
MCP tool servers and their components.
"""
import os
import sys
import importlib
from typing import List, Dict, Any, Tuple

# runtime imports
from runtime.src.mcp_server.logging_config import get_logger, logger
class ServerRegistry:
    """Registry for managing MCP tool servers with components"""
    def __init__(self, project_root: str, config: Dict[str, Any]):
        self.project_root = project_root
        self.config = config
        
        # Reconfigure logger with the loaded config
        logger = get_logger(config=config)
        
        self.server_paths, self.components = self._setup_server_paths()
        self._setup_python_paths()
        self.loaded_modules = {}
    
    def _setup_server_paths(self) -> Tuple[Dict[str, str], Dict[str, List[Dict[str, Any]]]]:
        """Process server configurations and resolve paths"""
        server_paths = {}
        components = {}
        
        # Add core paths
        core_paths = self.config.get("core", {})
        for name, location in core_paths.items():
            full_path = os.path.join(self.project_root, location)
            if os.path.exists(full_path):
                server_paths[name] = full_path
                logger.debug(f"Added core path {name} at {full_path}")
            else:
                logger.warning(f"Core path does not exist: {full_path}")
        
        # Process MCP servers
        mcp_servers = self.config.get("mcp_servers", {})
        for server_name, server_config in mcp_servers.items():
            if isinstance(server_config, dict) and server_config.get("enabled", True):
                location = server_config.get("location")
                if location:
                    full_path = os.path.join(self.project_root, location)
                    if os.path.exists(full_path):
                        server_paths[server_name] = full_path
                        
                        # Process components (tools, resources, prompts)
                        components[server_name] = []
                        
                        # Process tools
                        self._add_component(server_name, server_config, "tools", components)
                        self._add_component(server_name, server_config, "resources", components)
                        self._add_component(server_name, server_config, "prompts", components)
                        
                        logger.debug(f"Added MCP server {server_name} at {full_path}")
                    else:
                        logger.warning(f"MCP server location does not exist: {full_path}")
        
        # Auto-discover additional MCP servers if enabled
        if self.config.get("auto_discover", False):
            discovery_config = self.config.get("discovery", {}).get("components", {
                "tools": True,
                "resources": False,
                "prompts": False
            })
            
            servers_dir = os.path.join(self.project_root, "servers")
            if os.path.exists(servers_dir):
                for item in os.listdir(servers_dir):
                    server_dir = os.path.join(servers_dir, item)
                    if not os.path.isdir(server_dir):
                        continue
                        
                    # Skip if server is already configured
                    if item in server_paths:
                        continue
                        
                    # Check if the server has a src directory
                    src_dir = os.path.join(server_dir, "src")
                    if os.path.exists(src_dir):
                        server_paths[item] = src_dir
                        components[item] = []
                        
                        # Auto-discover components based on discovery configuration
                        if discovery_config.get("tools", True):
                            tools_module = f"{item}.tools"
                            components[item].append({
                                "type": "tools",
                                "module": tools_module,
                                "auto_discovered": True
                            })
                        
                        if discovery_config.get("resources", False):
                            resources_module = f"{item}.resources"
                            components[item].append({
                                "type": "resources",
                                "module": resources_module,
                                "auto_discovered": True
                            })
                            
                        if discovery_config.get("prompts", False):
                            prompts_module = f"{item}.prompts"
                            components[item].append({
                                "type": "prompts",
                                "module": prompts_module,
                                "auto_discovered": True
                            })
                        
                        logger.info(f"Auto-discovered MCP server: {item}")
        
        core_servers = [name for name in server_paths.keys() if name in core_paths]
        mcp_servers_list = [name for name in server_paths.keys() if name not in core_paths]
        
        logger.info(f"Core paths: {', '.join(core_servers)}")
        logger.info(f"MCP servers: {', '.join(mcp_servers_list)}")
        
        return server_paths, components
    
    def _add_component(self, server_name: str, server_config: Dict[str, Any], 
                       component_type: str, components: Dict[str, List[Dict[str, Any]]]) -> None:
        """Add a component (tools, resources, prompts) to the components dictionary"""
        component_config = server_config.get(component_type, {})
        if not isinstance(component_config, dict):
            return
            
        enabled = component_config.get("enabled", True)
        module = component_config.get("module")
        
        if enabled and module:
            components[server_name].append({
                "type": component_type,
                "module": module,
                "auto_discovered": False
            })
    
    def _setup_python_paths(self) -> None:
        """Add server source directories to Python path"""
        # Add paths to sys.path in reverse order for correct priority
        paths = list(self.server_paths.values())
        for path in reversed(paths):
            if path not in sys.path:
                logger.debug(f"Adding {path} to sys.path")
                sys.path.insert(0, path)
    
    def load_server_components(self) -> None:
        """Load all enabled components from configured servers"""
        for server_name, server_components in self.components.items():
            for component in server_components:
                module_name = component["module"]
                component_type = component["type"]
                auto_discovered = component.get("auto_discovered", False)
                
                try:
                    logger.info(f"Loading {component_type} from {module_name}" + 
                               (" (auto-discovered)" if auto_discovered else ""))
                    self.loaded_modules[module_name] = importlib.import_module(module_name)
                except ImportError as e:
                    if auto_discovered:
                        logger.debug(f"Auto-discovered module {module_name} not found: {e}")
                    else:
                        logger.warning(f"Failed to import {module_name}: {e}")