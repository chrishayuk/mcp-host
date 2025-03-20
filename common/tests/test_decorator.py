# common/tests/test_decorator.py
import pytest
import inspect
from pydantic import BaseModel
from common.mcp_tool_decorator import mcp_tool, TOOLS_REGISTRY
from mcp.types import Tool  # This should be your MCP Tool model

@mcp_tool(name="sample_tool", description="Test tool description")
def sample_tool(a: int, b: str) -> dict:
    return {"a": a, "b": b}

def test_tool_registration():
    # Verify that the tool function is registered in the global registry.
    assert "sample_tool" in TOOLS_REGISTRY, "sample_tool should be in the TOOLS_REGISTRY"
    
    # Verify that the decorated function has a _mcp_tool attribute.
    tool_metadata = getattr(sample_tool, "_mcp_tool", None)
    assert tool_metadata is not None, "Tool metadata (_mcp_tool) should be attached to the function"
    
    # Check that the metadata contains the correct name and description.
    assert tool_metadata.name == "sample_tool", "Tool name should be 'sample_tool'"
    assert tool_metadata.description == "Test tool description", "Tool description should match"

    # Validate that the inputSchema includes the parameters 'a' and 'b'
    input_schema = tool_metadata.inputSchema
    assert isinstance(input_schema, dict), "inputSchema should be a dict"
    assert "properties" in input_schema, "inputSchema should have a 'properties' key"
    properties = input_schema["properties"]
    assert "a" in properties, "Schema should include property 'a'"
    assert "b" in properties, "Schema should include property 'b'"
    
    # Optionally, check that type information is included in the schema
    assert properties["a"]["type"] == "integer", "Parameter 'a' should be of type integer"
    assert properties["b"]["type"] == "string", "Parameter 'b' should be of type string"

def test_tool_functionality():
    # Verify that the decorated function returns the expected output.
    result = sample_tool(a=42, b="hello")
    assert result == {"a": 42, "b": "hello"}, "The tool function should return the correct dictionary"
    
    # Additionally, check that the original function signature is preserved.
    sig = inspect.signature(sample_tool)
    assert "a" in sig.parameters, "Parameter 'a' should be in the function signature"
    assert "b" in sig.parameters, "Parameter 'b' should be in the function signature"
