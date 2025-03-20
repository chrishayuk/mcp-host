import asyncio
import json
import os
import sys

# Only bootstrap sys.path if NO_BOOTSTRAP is not set.
if not os.getenv("NO_BOOTSTRAP"):
    # Go up three directories:
    #   serverless-mcp/runtime/src/mcp_server/generic_mcp_server.py
    #   ../ -> serverless-mcp/runtime/src/mcp_server
    #   ../../ -> serverless-mcp/runtime/src
    #   ../../../ -> serverless-mcp
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    common_src = os.path.join(project_root, "common", "src")
    if common_src not in sys.path:
        sys.path.insert(0, common_src)

# Explicitly import the tool modules so that their decorators register tools.
import time_server.tools   # Registers time-related tools.
import echo_server.tools   # Registers echo-related tools.

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from common.mcp_tool_decorator import TOOLS_REGISTRY

async def serve() -> None:
    server = Server("generic-mcp")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        if not TOOLS_REGISTRY:
            print("No tools available. Exiting chat mode.")
        return [func._mcp_tool for func in TOOLS_REGISTRY.values()]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:
        if name not in TOOLS_REGISTRY:
            raise ValueError(f"Tool not found: {name}")
        func = TOOLS_REGISTRY[name]
        try:
            result = func(**arguments)
        except Exception as e:
            raise ValueError(f"Error processing tool '{name}': {str(e)}")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)

def get_handlers():
    server = Server("generic-mcp")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [func._mcp_tool for func in TOOLS_REGISTRY.values()]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:
        if name not in TOOLS_REGISTRY:
            raise ValueError(f"Tool not found: {name}")
        func = TOOLS_REGISTRY[name]
        try:
            result = func(**arguments)
        except Exception as e:
            raise ValueError(f"Error processing tool '{name}': {str(e)}")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    return list_tools, call_tool

def main() -> None:
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    main()