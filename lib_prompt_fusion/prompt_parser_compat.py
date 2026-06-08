from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence, Tuple


def normalize_conditioning_arguments(
    args: Sequence[Any],
    kwargs: Mapping[str, Any],
) -> Tuple[Optional[Any], bool, Tuple[Any, ...], Mapping[str, Any]]:
    """Extract hires_steps and use_old_scheduling from args/kwargs,
    returning normalized copies. Forge Neo passes hires_steps as a keyword
    argument, unlike A1111 which passed it positionally."""
    hires_steps = kwargs.get("hires_steps")
    use_old_scheduling = kwargs.get("use_old_scheduling", False)

    if len(args) >= 1:
        hires_steps = args[0]
    if len(args) >= 2:
        use_old_scheduling = args[1]

    if use_old_scheduling is None:
        use_old_scheduling = False

    if isinstance(use_old_scheduling, str):
        use_old_scheduling = use_old_scheduling.strip().lower()
        use_old_scheduling = use_old_scheduling not in {"", "0", "false", "no", "off"}
    else:
        use_old_scheduling = bool(use_old_scheduling)

    normalized_args = list(args)
    normalized_kwargs = dict(kwargs)

    if len(normalized_args) >= 1:
        normalized_args[0] = hires_steps
    elif "hires_steps" in normalized_kwargs:
        normalized_kwargs["hires_steps"] = hires_steps

    if len(normalized_args) >= 2:
        normalized_args[1] = use_old_scheduling
    elif "use_old_scheduling" in normalized_kwargs:
        normalized_kwargs["use_old_scheduling"] = use_old_scheduling

    return hires_steps, use_old_scheduling, tuple(normalized_args), normalized_kwargs
