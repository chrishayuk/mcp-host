import telnetlib
import time
from typing import List, Optional, Dict
from pydantic import ValidationError

from common.mcp_tool_decorator import mcp_tool
from mcp.shared.exceptions import McpError

from .models import TelnetClientInput, TelnetClientOutput, CommandResponse

# Telnet IAC / negotiation constants
IAC  = bytes([255])  # Interpret As Command
DONT = bytes([254])
DO   = bytes([253])
WONT = bytes([252])
WILL = bytes([251])

# Global session store
TELNET_SESSIONS: Dict[str, dict] = {}

@mcp_tool(name="telnet_client", description="Connect to a Telnet server, run commands, and return output.")
def telnet_client_tool(
    host: str, 
    port: int, 
    commands: List[str], 
    session_id: Optional[str] = None,
    close_session: bool = False
) -> dict:
    """
    Connect to the given Telnet server, do minimal Telnet option negotiation, 
    send each command, and capture/return the responses in a dict.

    :param host: Host/IP of the Telnet server.
    :param port: Port number (e.g. 8023).
    :param commands: List of commands to send to the server.
    :param session_id: Optional session ID to maintain connection between calls.
    :param close_session: If True, close the session after processing commands.
    :return: A dict containing the server's responses and session info.
    """
    # 1) Validate input using TelnetClientInput
    try:
        validated_input = TelnetClientInput(
            host=host, 
            port=port, 
            commands=commands
        )
    except ValidationError as e:
        raise ValueError(f"Invalid input for telnet_client_tool: {e}")

    # Generate a session ID if none provided
    if not session_id:
        session_id = f"telnet_{host}_{port}_{int(time.time())}"
    
    # Check if we have an existing session
    session = TELNET_SESSIONS.get(session_id)
    tn = None
    initial_data = ""
    
    if session:
        # Reuse existing session
        tn = session.get("telnet")
        if not tn:
            raise McpError(f"Session {session_id} exists but telnet connection is invalid")
    else:
        # Create new session
        tn = telnetlib.Telnet()
        
        # Minimal negotiation callback: always refuse
        def negotiation_callback(sock, cmd, opt):
            if cmd == DO:
                sock.sendall(IAC + WONT + opt)
            elif cmd == WILL:
                sock.sendall(IAC + DONT + opt)

        tn.set_option_negotiation_callback(negotiation_callback)

        # Open the connection
        try:
            tn.open(validated_input.host, validated_input.port, timeout=10)
        except Exception as ex:
            raise McpError(f"Failed to connect to Telnet server: {ex}")

        # Read initial banner
        initial_data = tn.read_until(b"> ", timeout=2).decode("utf-8", errors="ignore")
        
        # Store the session
        TELNET_SESSIONS[session_id] = {
            "telnet": tn,
            "host": validated_input.host,
            "port": validated_input.port,
            "created_at": time.time()
        }

    # Send commands and collect responses
    responses = []
    for cmd in validated_input.commands:
        tn.write(cmd.encode("utf-8") + b"\n")
        data = tn.read_until(b"> ", timeout=5)
        responses.append(CommandResponse(
            command=cmd,
            response=data.decode("utf-8", errors="ignore")
        ))

    # Close the session if requested
    if close_session and session_id in TELNET_SESSIONS:
        tn.close()
        del TELNET_SESSIONS[session_id]

    # Construct output
    output_model = TelnetClientOutput(
        host=validated_input.host,
        port=validated_input.port,
        initial_banner=initial_data,
        responses=responses,
        session_id=session_id,
        session_active=session_id in TELNET_SESSIONS
    )

    return output_model.model_dump()

# Add a tool for closing specific sessions
@mcp_tool(name="telnet_close_session", description="Close a specific Telnet session.")
def telnet_close_session(session_id: str) -> dict:
    """
    Close a specific Telnet session by ID.

    :param session_id: The session ID to close.
    :return: Status of the operation.
    """
    if session_id in TELNET_SESSIONS:
        try:
            TELNET_SESSIONS[session_id]["telnet"].close()
        except:
            pass  # Best effort to close
        del TELNET_SESSIONS[session_id]
        return {"success": True, "message": f"Session {session_id} closed"}
    else:
        return {"success": False, "message": f"Session {session_id} not found"}

# Add a tool for listing active sessions
@mcp_tool(name="telnet_list_sessions", description="List all active Telnet sessions.")
def telnet_list_sessions() -> dict:
    """
    List all active Telnet sessions.

    :return: Dict with session information.
    """
    sessions = {}
    for session_id, session_data in TELNET_SESSIONS.items():
        sessions[session_id] = {
            "host": session_data["host"],
            "port": session_data["port"],
            "created_at": session_data["created_at"],
            "age_seconds": time.time() - session_data["created_at"]
        }
    
    return {
        "active_sessions": len(sessions),
        "sessions": sessions
    }