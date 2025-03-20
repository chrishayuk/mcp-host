# runtime/src/mcp_server
import os
import json
import yaml
import logging

# logger
logger = logging.getLogger("generic_mcp_server")

# MCP Imports
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

# Imports
from runtime.src.mcp_server.se import Server
from common.mcp_tool_decorator import TOOLS_REGISTRY

async def serve() -> None:
    """Run the MCP server"""
    # Load configuration to get host server name
    config = {}
    project_root = get_project_root()
    config_path = os.path.join(project_root, "config.yaml")
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

def get_project_root() -> str:
    """Determine the project root directory"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
