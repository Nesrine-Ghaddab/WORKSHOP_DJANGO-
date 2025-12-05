from mcp.server.fastmcp import FastMCP
mcp=FastMCP(name="say hello")

@mcp.tool()

def say_hello(name :str ="nesrine"):
    return"Hello from mcp-project!"+name


if __name__ == "__main__":
    mcp.run(transport="stdio")
