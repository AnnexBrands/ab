"""Discoverability surface of ABConnectAPI: api.<TAB>, groups(), repr().

These pin the developer-ergonomics contract: endpoint groups must be visible
to static type checkers/IDEs (so ``api.<TAB>`` autocompletes them), and there
must be a runtime way to list them that mirrors the CLI's ``ab <enter>``.
"""

from __future__ import annotations

import os
from unittest.mock import patch

from ab import ABConnectAPI
from ab.auth import MemoryTokenStorage as _MemoryStorage
from ab.cli.discovery import discover_endpoints_from_class


def _make_api() -> ABConnectAPI:
    env = {"ABCONNECT_CLIENT_ID": "cid", "ABCONNECT_CLIENT_SECRET": "secret"}
    with patch.dict(os.environ, env, clear=True):
        return ABConnectAPI(token_storage=_MemoryStorage())


def _discovered_groups() -> set[str]:
    return {name for name in discover_endpoints_from_class() if "." not in name}


def test_every_endpoint_group_has_a_class_annotation():
    """Each ``api.<group>`` must be declared at class level so Pylance/IDEs
    autocomplete it. Guards against drift between _init_endpoints and the
    class-level type declarations."""
    annotated = set(ABConnectAPI.__annotations__)
    missing = _discovered_groups() - annotated
    assert not missing, (
        f"endpoint groups assigned in _init_endpoints but missing a class-level "
        f"annotation (invisible to api.<TAB>): {sorted(missing)}"
    )


def test_groups_lists_canonical_groups_without_alias_duplicates():
    api = _make_api()
    groups = api.groups()

    assert groups == sorted(groups)
    assert _discovered_groups() <= set(groups)
    assert {"companies", "jobs", "contacts", "catalog"} <= set(groups)
    # Back-compat aliases dedupe out (they point at the same instances).
    assert "docs" not in groups
    assert "cmaps" not in groups
    # Aliases still resolve to the same object they shadow.
    assert api.docs is api.documents
    assert api.cmaps is api.commodity_maps


def test_repr_summarizes_env_and_group_count():
    api = _make_api()
    text = repr(api)
    assert text.startswith("<ABConnectAPI ")
    assert "groups=" in text
    assert f"groups={len(api.groups())}" in text


def test_groups_are_instance_attributes_for_runtime_tab_completion():
    """Runtime REPL (IPython/Jupyter) tab-completion relies on dir() exposing
    the groups as instance attributes."""
    api = _make_api()
    listing = set(dir(api))
    assert _discovered_groups() <= listing
