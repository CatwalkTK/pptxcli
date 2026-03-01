"""Base definitions for tools."""

from dataclasses import dataclass
from typing import Any, Awaitable, Callable

ToolResult = str


@dataclass(frozen=True)
class ToolDefinition:
    """Wraps a tool's schema and its handler function."""

    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable[..., Awaitable[ToolResult]]
