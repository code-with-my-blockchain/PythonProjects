from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math Server")


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
        raise ValueError("Cannot divide by zero")
    return a / b


@mcp.tool()
def power(a: float, b: float) -> float:
    """Raise a to the power b"""
    return a ** b


@mcp.tool()
def square_root(a: float) -> float:
    """Return square root"""
    if a < 0:
        raise ValueError("Negative number")
    return a ** 0.5


if __name__ == "__main__":
    mcp.run()