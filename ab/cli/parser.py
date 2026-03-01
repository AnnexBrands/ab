"""CLI argument parsing — maps CLI flags to Python keyword arguments."""

from __future__ import annotations

import inspect
import json
import re
import sys
from typing import Any

from ab.cli.discovery import MethodInfo, ParamInfo

# ---------------------------------------------------------------------------
# Help-card helpers (T005–T008)
# ---------------------------------------------------------------------------

_RST_ROLE_RE = re.compile(r":\w+:`([^`]+)`")


def _strip_rst(text: str) -> str:
    """Remove RST role markup from docstrings.

    Converts ``:class:`ModelName``` to plain ``ModelName``.
    """
    return _RST_ROLE_RE.sub(r"\1", text)


def _format_python_signature(module_name: str, method: MethodInfo) -> str:
    """Build a full Python call signature string.

    Example: ``api.jobs.get(job_display_id: int) -> Job``
    """
    parts: list[str] = []
    for p in method.positional_params:
        type_str = _annotation_str(p.annotation)
        parts.append(f"{p.name}: {type_str}" if type_str else p.name)
    for p in method.keyword_params:
        type_str = _annotation_str(p.annotation)
        if p.default is not inspect.Parameter.empty:
            parts.append(f"{p.name}={p.default!r}")
        elif type_str:
            parts.append(f"{p.name}: {type_str}")
        else:
            parts.append(p.name)

    sig = ", ".join(parts)
    prefix = f"api.{module_name}.{method.name}" if module_name else method.name

    ret = method.return_annotation
    if not ret and method.route and method.route.response_model:
        ret = method.route.response_model
    if ret:
        return f"{prefix}({sig}) -> {ret}"
    return f"{prefix}({sig})"


def _format_cli_syntax(module_name: str, method: MethodInfo) -> str:
    """Build the CLI invocation string.

    Example: ``ab jobs get <job_display_id> [--flag=VALUE]``
    """
    parts = [f"ab {module_name} {method.name}" if module_name else f"ab {method.name}"]
    for p in method.positional_params:
        parts.append(f"<{p.name}>")
    for p in method.keyword_params:
        parts.append(f"[{p.cli_name}=VALUE]")
    return " ".join(parts)


def _format_model_fields(model_name: str, max_fields: int = 10) -> list[str]:
    """Resolve a Pydantic model and return formatted field lines.

    Returns lines like ``  fieldName       type       description``.
    """
    try:
        import ab.api.models as models_pkg
    except ImportError:
        return []

    # Handle List[Model] — extract inner name
    inner = re.match(r"^[Ll]ist\[(\w+)\]$", model_name)
    if inner:
        model_name = inner.group(1)

    model_cls = getattr(models_pkg, model_name, None)
    if model_cls is None:
        return []

    from pydantic import BaseModel

    if not (isinstance(model_cls, type) and issubclass(model_cls, BaseModel)):
        return []

    lines: list[str] = []
    for i, (fname, finfo) in enumerate(model_cls.model_fields.items()):
        if i >= max_fields:
            lines.append(f"    ... ({len(model_cls.model_fields) - max_fields} more fields)")
            break
        type_str = _field_type_str(finfo)
        desc = finfo.description or ""
        lines.append(f"    {fname:<20} {type_str:<14} {desc}")
    return lines


def _annotation_str(ann: Any) -> str:
    """Convert an annotation to a short string."""
    if ann is None:
        return ""
    if hasattr(ann, "__name__"):
        return ann.__name__
    return str(ann).replace("typing.", "")


def _field_type_str(finfo: Any) -> str:
    """Extract a readable type string from a Pydantic FieldInfo."""
    ann = finfo.annotation
    if ann is None:
        return "Any"
    origin = getattr(ann, "__origin__", None)
    args = getattr(ann, "__args__", ())
    # Optional[X] → X | None
    if origin is type(int | str) and type(None) in args:
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            inner = non_none[0]
            name = getattr(inner, "__name__", str(inner))
            return f"{name} | None"
    if hasattr(ann, "__name__"):
        return ann.__name__
    return str(ann).replace("typing.", "")


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


def print_method_help(method: MethodInfo, module_name: str = "") -> None:
    """Print a structured reference card for a method to stderr."""
    w = sys.stderr.write

    # Header
    w(f"\n  {method.name}\n")
    w(f"  {'─' * len(method.name)}\n")

    # Description (first paragraph, RST-stripped)
    if method.docstring:
        first_para = method.docstring.split("\n\n")[0]
        w(f"\n  {_strip_rst(first_para)}\n")

    w("\n")

    # Route line
    if method.route:
        w(f"  Route   {method.route.method} {method.route.path}\n")

    # Python signature line
    w(f"  Python  {_format_python_signature(module_name, method)}\n")

    # CLI syntax line
    w(f"  CLI     {_format_cli_syntax(module_name, method)}\n")

    # Returns line
    ret = method.return_annotation
    if not ret and method.route and method.route.response_model:
        ret = method.route.response_model
    if ret:
        w(f"\n  Returns: {ret}\n")

    # Positional arguments
    if method.positional_params:
        w("\n  Positional arguments:\n")
        for p in method.positional_params:
            type_str = _annotation_str(p.annotation) or "str"
            w(f"    {p.name} ({type_str})\n")

    # Keyword arguments
    if method.keyword_params:
        w("\n  Keyword arguments:\n")
        for p in method.keyword_params:
            type_str = _annotation_str(p.annotation) or "str"
            default_str = (
                f" [default: {p.default}]"
                if p.default is not inspect.Parameter.empty
                else " (required)"
            )
            w(f"    {p.cli_name}=VALUE ({type_str}){default_str}\n")

    # Model field sections (response, request, params)
    if method.route:
        if method.route.response_model:
            _print_model_section(w, "Response", method.route.response_model)
        if method.route.request_model:
            _print_model_section(w, "Request", method.route.request_model)
        if method.route.params_model:
            _print_model_section(w, "Params", method.route.params_model)

    w("\n")


def _print_model_section(w: Any, label: str, model_name: str) -> None:
    """Print a model fields section to the write callable."""
    fields = _format_model_fields(model_name)
    if fields:
        w(f"\n  {label} model: {model_name}\n")
        for line in fields:
            w(f"{line}\n")


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
