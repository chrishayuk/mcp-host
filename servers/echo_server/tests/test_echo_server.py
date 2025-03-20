from echo_server.tools import echo

def test_echo_valid():
    result = echo("Hello, World!")
    assert result["message"] == "Hello, World!"
