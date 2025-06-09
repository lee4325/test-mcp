from mcp.server.fastmcp import FastMCP, RequestContext

# Initialize FastMCP server
mcp = FastMCP(
    name="test",
    host="0.0.0.0",  # only used for SSE transport
    port=8050,
)


@mcp.tool()
async def add_two_numbers(a: float, b: float, dummy_key: str = "") -> str:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of the two numbers
    """
    #print(dummy_token)

    return str(a + b) + " " + dummy_key

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(
        transport='sse',
    )
