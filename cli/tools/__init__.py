"""Tool registry -- collects all tools and provides API-compatible schemas."""

from .base import ToolDefinition
from .command_tool import execute_command_tool
from .file_tools import list_files_tool, read_file_tool, search_files_tool, write_file_tool
from .pptx_tool import generate_pptx_tool

ALL_TOOLS: list[ToolDefinition] = [
    read_file_tool,
    write_file_tool,
    list_files_tool,
    search_files_tool,
    execute_command_tool,
    generate_pptx_tool,
]

TOOL_MAP: dict[str, ToolDefinition] = {t.name: t for t in ALL_TOOLS}


def get_anthropic_tools() -> list[dict]:
    """Return tool definitions in Anthropic API format."""
    return [
        {
            "name": t.name,
            "description": t.description,
            "input_schema": t.input_schema,
        }
        for t in ALL_TOOLS
    ]
