"""Shell command execution tool."""

import asyncio
import os

from .base import ToolDefinition, ToolResult


async def _execute_command(command: str, timeout: int = 30) -> ToolResult:
    """Execute a shell command and return its output."""
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=os.getcwd(),
        )
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=timeout,
        )
        result_parts: list[str] = []
        if stdout:
            result_parts.append(stdout.decode("utf-8", errors="replace"))
        if stderr:
            result_parts.append(f"[stderr]\n{stderr.decode('utf-8', errors='replace')}")
        result_parts.append(f"\n[exit code: {process.returncode}]")
        output = "\n".join(result_parts)
        if len(output) > 50_000:
            output = output[:50_000] + "\n... (output truncated)"
        return output
    except asyncio.TimeoutError:
        return f"Error: Command timed out after {timeout}s"
    except Exception as e:
        return f"Error executing command: {e}"


execute_command_tool = ToolDefinition(
    name="execute_command",
    description="Execute a shell command and return stdout/stderr. Use for running scripts, git commands, etc.",
    input_schema={
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "Shell command to execute"},
            "timeout": {
                "type": "integer",
                "description": "Timeout in seconds (default: 30)",
                "default": 30,
            },
        },
        "required": ["command"],
    },
    handler=_execute_command,
)
