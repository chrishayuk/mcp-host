import asyncio
import json
import pytest

# Import our dummy tool decorator and registry.
from common.mcp_tool_decorator import mcp_tool, TOOLS_REGISTRY
from mcp.types import TextContent

# Define a dummy tool for testing purposes.
@mcp_tool(name="dummy_tool", description="A dummy tool for testing")
def dummy_tool(a: int, b: str) -> dict:
    return {"a": a, "b": b}

# Import the get_handlers helper from our generic MCP server.
from mcp_server.generic_mcp_server import get_handlers

@pytest.mark.asyncio
async def test_list_tools():
    # Clear the registry and add the dummy tool.
    TOOLS_REGISTRY.clear()
    TOOLS_REGISTRY["dummy_tool"] = dummy_tool
    
    list_tools, _ = get_handlers()
    tools = await list_tools()
    # Check that our dummy tool is in the list.
    tool_names = [tool.name for tool in tools]
    assert "dummy_tool" in tool_names

@pytest.mark.asyncio
async def test_call_tool():
    # Clear the registry and add the dummy tool.
    TOOLS_REGISTRY.clear()
    TOOLS_REGISTRY["dummy_tool"] = dummy_tool
    
    _, call_tool = get_handlers()
    result_list = await call_tool("dummy_tool", {"a": 42, "b": "hello"})
    
    # Expect a list with one TextContent object.
    assert isinstance(result_list, list)
    assert len(result_list) == 1
    content = result_list[0]
    assert isinstance(content, TextContent)
    # Parse the JSON text.
    result_data = json.loads(content.text)
    assert result_data == {"a": 42, "b": "hello"}
