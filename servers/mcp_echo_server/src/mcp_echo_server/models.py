# mcp_echo_server/models.py
from pydantic import BaseModel, Field

class EchoInput(BaseModel):
    message: str = Field(..., description="The message to echo back")

class EchoResult(BaseModel):
    message: str = Field(..., description="The echoed message")
