import asyncio
from pathlib import Path

from agents import Agent, Runner
from agents.mcp import MCPServerStdio, MCPServerStdioParams

# Absolute path to the MCP server script. with_name() keeps this file's
# directory and swaps the filename, so the lookup survives any working directory.
SCRIPT = Path(__file__).with_name("01_claude_mcp_server.py").resolve()


async def main():
    async with MCPServerStdio(
        name="Research Tools",  # client-side label, used only in logs and traces
        params=MCPServerStdioParams(
            command="mcp",  # the `mcp` CLI must be on PATH of the spawned process
            args=["run", str(SCRIPT)],
        ),
    ) as research_server:
        agent = Agent(
            name="Assistant",
            instructions="Use the research tools to perform research.",
            mcp_servers=[research_server],
        )

        # Runs the model/tool loop: tool calls are routed back over stdio to
        # the server, and the results are fed to the model until it answers.
        print("Running: Get the available research sources")
        result = await Runner.run(agent, "Get the available research sources")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
