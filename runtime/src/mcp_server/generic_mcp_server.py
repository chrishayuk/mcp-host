# runtime/src/mcp_server/generic_mcp_server.py
import asyncio
import importlib
import json
import os
import sys
import yaml
from typing import List, Dict, Any, Optional, Tuple
import glob
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("generic_mcp_server")

class ServerRegistry:
    """Registry for managing MCP tool servers with components"""
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.config = self._load_config()
        self._configure_logging()
        self.server_paths, self.components = self._setup_server_paths()
        self._setup_python_paths()
        self.loaded_modules = {}
        
    def _load_config(self) -> Dict[str, Any]:
        """Load server configuration from config file if it exists"""
        config_paths = [
            os.path.join(self.project_root, "config.yaml"),
            os.path.join(self.project_root, "config.yml"),
            os.path.join(self.project_root, "runtime", "config.yaml"),
        ]
        
        for path in config_paths:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    logger.info(f"Loading config from {path}")
                    return yaml.safe_load(f)
        
        # Default config if no file found
        logger.info("No config file found, using default configuration")
        return {
            "host": {"name": "generic-mcp", "log_level": "INFO"},
            "core": {
                "common": "common/src",
                "runtime": "runtime/src"
            },
            "mcp_servers": {
                "time_server": {
                    "location": "servers/time_server/src", 
                    "enabled": True,
                    "tools": {
                        "module": "time_server.tools",
                        "enabled": True
                    }
                },
                "echo_server": {
                    "location": "servers/echo_server/src", 
                    "enabled": True,
                    "tools": {
                        "module": "echo_server.tools",
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
    
    def _configure_logging(self) -> None:
        """Configure logging based on config settings"""
        log_level = self.config.get("host", {}).get("log_level", "INFO")
        level = getattr(logging, log_level.upper(), logging.INFO)
        logger.setLevel(level)
        logging.getLogger().setLevel(level)
        logger.info(f"Log level set to {log_level}")
    
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


# Main server code
def get_project_root() -> str:
    """Determine the project root directory"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(script_dir, "..", "..", ".."))

async def serve() -> None:
    """Run the MCP server"""
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
    from common.mcp_tool_decorator import TOOLS_REGISTRY
    
    # Load configuration to get host server name
    config = {}
    config_path = os.path.join(get_project_root(), "config.yaml")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    
    server_name = config.get("host", {}).get("name", "generic-mcp")
    server = Server(server_name)

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        if not TOOLS_REGISTRY:
            logger.warning("No tools available")
            return []
        return [func._mcp_tool for func in TOOLS_REGISTRY.values()]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:
        if name not in TOOLS_REGISTRY:
            raise ValueError(f"Tool not found: {name}")
        func = TOOLS_REGISTRY[name]
        try:
            result = func(**arguments)
        except Exception as e:
            logger.error(f"Error processing tool '{name}': {e}", exc_info=True)
            raise ValueError(f"Error processing tool '{name}': {str(e)}")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)

def main() -> None:
    # Only bootstrap if NO_BOOTSTRAP is not set
    if os.getenv("NO_BOOTSTRAP"):
        logger.info("Bootstrapping disabled by NO_BOOTSTRAP environment variable")
        # Import tools registry
        from common.mcp_tool_decorator import TOOLS_REGISTRY
        if not TOOLS_REGISTRY:
            logger.warning("No tools available")
    else:
        project_root = get_project_root()
        # Set up server registry and load components
        registry = ServerRegistry(project_root)
        registry.load_server_components()
        
        # Log the number of tools found
        from common.mcp_tool_decorator import TOOLS_REGISTRY
        logger.info(f"Loaded {len(TOOLS_REGISTRY)} tools")
        if TOOLS_REGISTRY:
            logger.info(f"Available tools: {', '.join(TOOLS_REGISTRY.keys())}")
        else:
            logger.warning("No tools were loaded")

    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)

if __name__ == "__main__":
    main()