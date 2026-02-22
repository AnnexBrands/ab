"""CLI argument parsing — maps CLI flags to Python keyword arguments."""

from __future__ import annotations

import inspect
import json
import sys
from typing import Any

from ab.cli.discovery import MethodInfo, ParamInfo


def _coerce_value(value: str, param: ParamInfo) -> Any:
    """Coerce a string CLI value to the parameter's annotated type."""
    annotation = param.annotation

    if annotation is None:
        # Try int if it looks numeric
        if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
            return int(value)
        return value

    # Unwrap Optional[X] → X
    origin = getattr(annotation, "__origin__", None)
    args = getattr(annotation, "__args__", ())
    if origin is type(int | str):  # Union type
        # Pick the first non-None type
        for arg in args:
            if arg is not type(None):
                annotation = arg
                break

    if annotation is int:
        return int(value)
    if annotation is float:
        return float(value)
    if annotation is bool:
        return value.lower() in ("true", "1", "yes")
    if annotation is dict or annotation is Any:
        return json.loads(value)

    return value


def print_method_help(method: MethodInfo) -> None:
    """Print detailed help for a method and exit."""
    print(f"\n  {method.name}", file=sys.stderr)
    if method.docstring:
        print(f"  {method.docstring}", file=sys.stderr)

    if method.positional_params:
        print("\n  Positional arguments:", file=sys.stderr)
        for p in method.positional_params:
            type_str = getattr(p.annotation, "__name__", str(p.annotation)) if p.annotation else "str"
            print(f"    {p.name} ({type_str})", file=sys.stderr)

    if method.keyword_params:
        print("\n  Keyword arguments:", file=sys.stderr)
        for p in method.keyword_params:
            type_str = getattr(p.annotation, "__name__", str(p.annotation)) if p.annotation else "str"
            default_str = f" [default: {p.default}]" if p.default is not inspect.Parameter.empty else " (required)"
            print(f"    {p.cli_name}=VALUE ({type_str}){default_str}", file=sys.stderr)

    print(file=sys.stderr)


def parse_cli_args(
    args: list[str], method: MethodInfo
) -> tuple[list[Any], dict[str, Any]]:
    """Parse CLI arguments into positional and keyword args for method invocation.

    Returns (positional_args, keyword_args).
    """
    if "--help" in args:
        print_method_help(method)
        sys.exit(0)

    positional: list[Any] = []
    keyword: dict[str, Any] = {}

    # Build lookup of valid keyword params
    kw_lookup: dict[str, ParamInfo] = {}
    for p in method.keyword_params:
        kw_lookup[p.cli_name] = p
        # Also accept underscore form: --zip_code
        kw_lookup[f"--{p.name}"] = p

    i = 0
    pos_idx = 0
    while i < len(args):
        arg = args[i]

        if arg.startswith("--"):
            # --key=value form
            if "=" in arg:
                key, value = arg.split("=", 1)
            elif i + 1 < len(args) and not args[i + 1].startswith("--"):
                key = arg
                value = args[i + 1]
                i += 1
            else:
                key = arg
                value = "true"  # boolean flag

            # Normalize key
            normalized = key.replace("_", "-")
            if normalized not in kw_lookup and key not in kw_lookup:
                # Check for special --body flag
                if key in ("--body",):
                    keyword["__body__"] = json.loads(value)
                    i += 1
                    continue
                # Unknown flag
                valid = ", ".join(p.cli_name for p in method.keyword_params)
                print(f"Unknown argument: {key}", file=sys.stderr)
                if valid:
                    print(f"Valid parameters: {valid}", file=sys.stderr)
                sys.exit(1)

            param = kw_lookup.get(normalized) or kw_lookup.get(key)
            keyword[param.name] = _coerce_value(value, param)
        else:
            # Positional argument
            if pos_idx < len(method.positional_params):
                param = method.positional_params[pos_idx]
                positional.append(_coerce_value(arg, param))
                pos_idx += 1
            else:
                print(f"Unexpected positional argument: {arg}", file=sys.stderr)
                sys.exit(1)

        i += 1

    # Check required positional args
    for j in range(pos_idx, len(method.positional_params)):
        p = method.positional_params[j]
        if p.required:
            print(f"Missing required argument: {p.name}", file=sys.stderr)
            sig_parts = [p.name for p in method.positional_params]
            sig_parts += [f"[{p.cli_name}=VALUE]" for p in method.keyword_params]
            print(f"Usage: {method.name} {' '.join(sig_parts)}", file=sys.stderr)
            sys.exit(1)

    return positional, keyword
