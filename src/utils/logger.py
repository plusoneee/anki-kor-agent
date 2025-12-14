from functools import wraps
from typing import Callable, Dict, Any
from rich.console import Console
from datetime import datetime

console = Console(log_path=False)


def _format_val(val: Any) -> str:
    """Format value for display, escaping Rich markup."""
    if isinstance(val, bytes):
        display = f"<bytes: {len(val)} bytes>"
    else:
        display = repr(val)
        if len(display) > 60:
            display = display[:57] + "..."
    # Only escape opening brackets to prevent Rich markup parsing
    return display.replace("[", "\\[")


def node_logger(func: Callable):
    """Compact node logger matching service log format."""

    @wraps(func)
    async def wrapper(state: Dict[str, Any], *args, **kwargs):
        node_name = func.__name__
        start_time = datetime.now()
        before_state = dict(state)

        # ── Node Start ──
        console.log(f"[cyan]\\[{node_name}][/] ▶ start")

        # Execute node
        result_delta = await func(state, *args, **kwargs)

        # Compute diff
        diff_parts = []
        for key, after_val in result_delta.items():
            before_val = before_state.get(key, "<new>")
            if before_val != after_val:
                diff_parts.append(
                    f"[dim]{key}:[/] [red]{_format_val(before_val)}[/] → [green]{_format_val(after_val)}[/]"
                )

        duration = (datetime.now() - start_time).total_seconds()
        diff_str = ", ".join(diff_parts) if diff_parts else "[dim]<no changes>[/]"

        # ── Node End ──
        console.log(f"[green]\\[{node_name} {duration:.3f}s][/] ✓ {diff_str}")

        return result_delta

    return wrapper
