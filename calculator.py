from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="calculator")

@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract two numbers"""
    return a - b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide two numbers"""
    if b == 0:
        return float('inf')  # Ou lève une exception selon vos besoins
    return a / b

if __name__ == "__main__":
    mcp.run(transport="stdio")