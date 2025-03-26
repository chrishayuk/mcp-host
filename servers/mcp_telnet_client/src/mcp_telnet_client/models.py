# mcp_telnet_client/models.py
from pydantic import BaseModel, Field
from typing import List

class TelnetClientInput(BaseModel):
    host: str = Field(..., description="Host or IP address of the Telnet server.")
    port: int = Field(..., description="Port on which the Telnet server is listening.")
    commands: List[str] = Field(..., description="Commands to send sequentially.")

class CommandResponse(BaseModel):
    command: str
    response: str

class TelnetClientOutput(BaseModel):
    host: str
    port: int
    initial_banner: str
    responses: List[CommandResponse]
