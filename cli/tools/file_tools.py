"""File operation tools."""

import glob as glob_module
import os

from .base import ToolDefinition, ToolResult


async def _read_file(path: str) -> ToolResult:
    """Read and return the contents of a file."""
    abs_path = os.path.abspath(path)
    if not os.path.isfile(abs_path):
        return f"Error: File not found: {abs_path}"
    with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    max_chars = 100_000
    if len(content) > max_chars:
        content = content[:max_chars] + f"\n\n... (truncated, {len(content)} total chars)"
    return content


async def _write_file(path: str, content: str) -> ToolResult:
    """Write content to a file, creating directories as needed."""
    abs_path = os.path.abspath(path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File written: {abs_path} ({len(content)} chars)"


async def _list_files(path: str = ".", recursive: bool = False) -> ToolResult:
    """List files in a directory."""
    abs_path = os.path.abspath(path)
    if not os.path.isdir(abs_path):
        return f"Error: Not a directory: {abs_path}"
    entries: list[str] = []
    if recursive:
        for root, dirs, files in os.walk(abs_path):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), abs_path)
                entries.append(rel)
    else:
        for item in sorted(os.listdir(abs_path)):
            marker = "/" if os.path.isdir(os.path.join(abs_path, item)) else ""
            entries.append(f"{item}{marker}")
    if not entries:
        return "(empty directory)"
    return "\n".join(entries[:500])


async def _search_files(pattern: str, path: str = ".") -> ToolResult:
    """Search for files matching a glob pattern."""
    abs_path = os.path.abspath(path)
    matches = glob_module.glob(os.path.join(abs_path, pattern), recursive=True)
    if not matches:
        return f"No files matching '{pattern}' in {abs_path}"
    results = [os.path.relpath(m, abs_path) for m in matches[:200]]
    return "\n".join(results)


read_file_tool = ToolDefinition(
    name="read_file",
    description="Read the contents of a file at the given path",
    input_schema={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "File path to read"},
        },
        "required": ["path"],
    },
    handler=_read_file,
)

write_file_tool = ToolDefinition(
    name="write_file",
    description="Write content to a file. Creates the file and parent directories if needed.",
    input_schema={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "File path to write to"},
            "content": {"type": "string", "description": "Content to write"},
        },
        "required": ["path", "content"],
    },
    handler=_write_file,
)

list_files_tool = ToolDefinition(
    name="list_files",
    description="List files and directories at the given path",
    input_schema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Directory path (default: current dir)",
                "default": ".",
            },
            "recursive": {
                "type": "boolean",
                "description": "List recursively",
                "default": False,
            },
        },
        "required": [],
    },
    handler=_list_files,
)

search_files_tool = ToolDefinition(
    name="search_files",
    description="Search for files matching a glob pattern (e.g., '**/*.py')",
    input_schema={
        "type": "object",
        "properties": {
            "pattern": {"type": "string", "description": "Glob pattern to match"},
            "path": {
                "type": "string",
                "description": "Base directory (default: current dir)",
                "default": ".",
            },
        },
        "required": ["pattern"],
    },
    handler=_search_files,
)
