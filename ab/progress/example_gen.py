"""Generate canonical (plain-script) example source.

Used by ``scripts/ingest_captures.py`` (turn a pasted endpoint into an example) and
by scaffolding to fill coverage gaps. Output matches
``examples/dashboard.py`` / ``specs/037-example-coverage/contracts/example-contract.md``
§1: module docstring + RTD link, ``ABConnectAPI``, ``from examples._capture import
save``, a real call, ``print(format_result(...))``, ``save("<Model>.json", result)``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ab.api.rtd import endpoint_doc_url, endpoint_top_group

# Best-effort map from a path/param name (snake or camel) to a TEST_* constant in
# examples/constants.py. Keys are matched case-insensitively after stripping
# underscores. Anything unmatched becomes a clearly-marked placeholder so the
# endpoint surfaces as awaiting-data rather than silently calling with junk.
PARAM_CONSTANTS: dict[str, str] = {
    "jobid": "TEST_JOB_DISPLAY_ID",
    "jobdisplayid": "TEST_JOB_DISPLAY_ID",
    "companyid": "TEST_COMPANY_ID",
    "companycode": "TEST_COMPANY_CODE",
    "contactid": "TEST_CONTACT_ID",
    "contactdid": "TEST_CONTACT_DID",
    "catalogid": "TEST_CATALOG_ID",
    "sellerid": "TEST_SELLER_ID",
    "lotid": "TEST_LOT_ID",
    "lotnumber": "TEST_LOT_NUMBER",
    "itemid": "TEST_ITEM_ID",
    "noteid": "TEST_NOTE_ID",
    "userid": "TEST_USER_ID",
    "onholdid": "TEST_ON_HOLD_ID",
    "taskcode": "TEST_TIMELINE_TASK_CODE",
    "taskid": "TEST_TIMELINE_TASK_ID",
    "smstemplateid": "TEST_SMS_TEMPLATE_ID",
}

_PLACEHOLDER = '"REPLACE_ME"'


@dataclass
class CallSpec:
    """One demonstrated call inside an example module."""

    group: str  # discovery group, e.g. "jobs.payment"
    method: str  # method name, e.g. "list"
    call_expr: str  # full RHS, e.g. 'api.jobs.payment.list(str(TEST_JOB_DISPLAY_ID))'
    save_name: str | None  # "JobPayment.json" or None (no fixture, e.g. binary)
    constants: set[str] = field(default_factory=set)  # TEST_* imports needed
    comment: str | None = None  # optional note printed above the call


def constant_for_param(param_name: str) -> str | None:
    """Return the TEST_* constant for *param_name*, or None when unknown."""
    key = param_name.replace("_", "").lower()
    return PARAM_CONSTANTS.get(key)


def call_expr_for(group: str, method: str, param_names: list[str]) -> tuple[str, set[str]]:
    """Build ``api.<group>.<method>(<args>)`` using best-effort constants.

    Returns ``(call_expr, needed_constants)``. Unknown params become a clearly
    marked ``"REPLACE_ME"`` placeholder.
    """
    args: list[str] = []
    consts: set[str] = set()
    for p in param_names:
        const = constant_for_param(p)
        if const:
            args.append(f"str({const})")
            consts.add(const)
        else:
            args.append(_PLACEHOLDER)
    call = f"api.{group}.{method}({', '.join(args)})"
    return call, consts


def _module_path_for(group: str) -> str:
    """Repo-relative file path for a group's canonical example."""
    top = endpoint_top_group(group)
    sub = group.split(".")[1:]
    if sub:
        return f"examples/{top}/{'_'.join(sub)}.py"
    return f"examples/{group}.py"


def render_module(group: str, calls: list[CallSpec]) -> str:
    """Render a complete canonical example module for *group*."""
    top = endpoint_top_group(group)
    doc_url = endpoint_doc_url(group, calls[0].method) if calls else f"{top}.html"
    title = group.replace("_", " ").replace(".", " ").title()

    constants: set[str] = set()
    for c in calls:
        constants.update(c.constants)

    lines: list[str] = []
    lines.append(f'"""Example: {title}.')
    lines.append("")
    lines.append("Live SDK example — real call, real printed pydantic response.")
    lines.append(f"See also: {doc_url}")
    lines.append('"""')
    lines.append("")
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from ab import ABConnectAPI")
    lines.append("from ab.cli.formatter import format_result")
    lines.append("from examples._capture import save")
    if constants:
        const_list = ", ".join(sorted(constants))
        lines.append(f"from examples.constants import {const_list}")
    lines.append("")
    lines.append("")
    lines.append("def main() -> None:")
    lines.append('    api = ABConnectAPI(env="staging")')
    for c in calls:
        lines.append("")
        if c.comment:
            lines.append(f"    # {c.comment}")
        lines.append(f'    print("\\n# {c.call_expr}")')
        lines.append(f"    result = {c.call_expr}")
        lines.append("    print(format_result(result))")
        if c.save_name:
            lines.append(f'    save("{c.save_name}", result)')
    lines.append("")
    lines.append("")
    lines.append('if __name__ == "__main__":')
    lines.append("    main()")
    return "\n".join(lines) + "\n"


def module_path_for(group: str) -> str:
    """Public alias for the canonical example file path of *group*."""
    return _module_path_for(group)


def strip_list_wrapper(model: str | None) -> str:
    """``List[Foo]`` / ``list[Foo]`` -> ``Foo``; else unchanged."""
    if not model:
        return ""
    m = re.match(r"^(?:List|list|PaginatedList)\[(.+)\]$", model.strip())
    return m.group(1).strip() if m else model.strip()
