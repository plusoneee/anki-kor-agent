from functools import wraps
from typing import Callable, Dict, Any
from rich.console import Console
from rich.panel import Panel
from datetime import datetime

console = Console()


def bold_label(text: str) -> str:
    return f"[bold]{text}:[/]"

def bold_key(text: str) -> str:
    return f"[bold]{text}[/]"

def color_val(val: Any, color: str) -> str:
    # Handle bytes specially to avoid Rich markup parsing issues
    if isinstance(val, bytes):
        display = f"<bytes: {len(val)} bytes>"
    else:
        display = repr(val)
    # Escape brackets to prevent Rich markup parsing
    display = display.replace("[", "\\[").replace("]", "\\]")
    return f"[{color}]{display}[/{color}]"


def node_logger(func: Callable):
    """
    Node Logger:
    - bold labels
    - bold keys
    - colored value diff
    """

    @wraps(func)
    async def wrapper(state: Dict[str, Any], *args, **kwargs):
        node_name = func.__name__
        start_time = datetime.now()

        # Snapshot state before execution
        before_state = dict(state)
        before_keys = set(before_state.keys())

        colored_name = f"[bold cyan]{node_name}[/]"

        # ---- Node Start ----
        start_body = (
            f"{bold_label('name')} {colored_name}\n"
            f"{bold_label('input')} {[bold_key(k) for k in before_keys]}"
        )

        console.log(
            Panel(start_body, title="Node Start", border_style="cyan", padding=(0, 1)),
            markup=True,
        )

        # Execute node
        result_delta = await func(state, *args, **kwargs)

        # After state
        after_state = before_state | result_delta
        after_keys = set(after_state.keys())

        # Compute changed keys and value diff
        changed_keys = []
        diff_lines = []

        for key in after_keys:
            before_val = before_state.get(key, "<missing>")
            after_val = after_state.get(key)

            if before_val != after_val:
                changed_keys.append(key)
                diff_lines.append(
                    f"{bold_key(key)}: {color_val(before_val, 'red')} → {color_val(after_val, 'green')}"
                )

        duration = (datetime.now() - start_time).total_seconds()
        diff_block = "  " + "\n  ".join(diff_lines) if diff_lines else "  <no changes>"

        end_body = (
            f"{bold_label('name')} {colored_name}\n"
            f"{bold_label('output')} {[bold_key(k) for k in result_delta.keys()]}\n"
            f"{bold_label('changed')} {[bold_key(k) for k in changed_keys]}\n"
            f"{bold_label('diff')}\n{diff_block}\n"
            f"{bold_label('time')} {duration:.3f}s"
        )

        console.log(
            Panel(end_body, title="Node End", border_style="green", padding=(0, 1)),
            markup=True,
        )

        return result_delta

    return wrapper
