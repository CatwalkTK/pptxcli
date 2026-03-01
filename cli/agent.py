"""Agent: Claude API interaction with tool-use agentic loop."""

import inspect

from anthropic import AsyncAnthropic

from .config import ANTHROPIC_API_KEY, MAX_TOKENS, MODEL, SYSTEM_PROMPT
from .tools import TOOL_MAP, get_anthropic_tools
from .ui.console import print_error, print_tool_call, print_tool_result


class Agent:
    def __init__(self) -> None:
        self._client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
        self._messages: list[dict] = []
        self._tools = get_anthropic_tools()

    async def send(self, user_input: str) -> str:
        """Send user message, run tool loop, return final assistant text."""
        self._messages.append({"role": "user", "content": user_input})
        return await self._run_loop()

    async def _run_loop(self) -> str:
        """Agentic loop: call Claude, handle tool use, repeat until done."""
        max_iterations = 20

        for _ in range(max_iterations):
            response = await self._client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                messages=self._messages,
                tools=self._tools,
            )

            collected_blocks = response.content

            # Extract text and tool_use blocks
            text_parts: list[str] = []
            tool_uses: list = []
            for block in collected_blocks:
                if block.type == "text":
                    text_parts.append(block.text)
                elif block.type == "tool_use":
                    tool_uses.append(block)

            full_text = "\n".join(text_parts)

            # Append assistant message to history
            self._messages.append({"role": "assistant", "content": collected_blocks})

            # If no tool use, we are done
            if response.stop_reason != "tool_use" or not tool_uses:
                return full_text

            # Process tool calls and collect results
            tool_results: list[dict] = []
            for tool_use in tool_uses:
                tool_name = tool_use.name
                tool_input = tool_use.input

                print_tool_call(tool_name, tool_input)

                tool_def = TOOL_MAP.get(tool_name)
                if tool_def is None:
                    result = f"Error: Unknown tool '{tool_name}'"
                else:
                    try:
                        handler = tool_def.handler
                        sig = inspect.signature(handler)
                        filtered = {
                            k: v
                            for k, v in tool_input.items()
                            if k in sig.parameters
                        }
                        result = await handler(**filtered)
                    except Exception as e:
                        result = f"Error: {type(e).__name__}: {e}"
                        print_error(result)

                print_tool_result(tool_name, result)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": result,
                    }
                )

            # Append tool results as user message
            self._messages.append({"role": "user", "content": tool_results})

        return "(Max tool iterations reached)"

    def clear_history(self) -> None:
        """Reset conversation history."""
        self._messages.clear()
