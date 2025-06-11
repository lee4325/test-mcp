from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from mcp.server.fastmcp import FastMCP
import json
import base64
import os

# Initialize FastMCP server
mcp = FastMCP(
    name="test",
    host="0.0.0.0",  # only used for SSE transport
    port=8050,
)

# Generate RSA key pair on startup
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

# Serialize public key to PEM format
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

@mcp.tool()
async def get_public_key() -> str:
    """Get the server's public key for secure communication."""
    return public_key_pem.decode()

@mcp.tool()
async def add_two_numbers(a: float, b: float, dummy_key: str) -> str:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of the two numbers
    """
    # Decode from base64
    encrypted_data = base64.b64decode(dummy_key)

    # Decrypt with private key
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return str(a + b) + " " + decrypted_data.decode()

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(
        transport='sse',
    )
