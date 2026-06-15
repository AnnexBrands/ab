"""Acme pickup-and-pack agent — staging client factory (test infrastructure).

Underscore-prefixed: this is shared infra, not a canonical endpoint example, so
the example-coverage harness ignores it.

Acme is an *agent* on jobs owned by other companies (e.g. the Live-owned job
``LIVE_OWNED_JOB_DISPLAY_ID``). It can advance the pickup (PU) timeline category
but has fewer permissions than the job owner — notably it cannot write
top-level job notes. It is a disposable staging test account, so mutations are
*always* enabled for it (no ``AB_RUN_MUTATIONS`` gate needed when you drive it
deliberately).

Secrets live in the gitignored ``.env.acme``; only non-secret identifiers live
in :mod:`examples.constants`.
"""

from __future__ import annotations

from pathlib import Path

from ab import ABConnectAPI
from examples.constants import ACME_ENV_FILE

#: Repo-root path to the gitignored Acme credentials file.
ACME_ENV_PATH = Path(__file__).resolve().parent.parent / ACME_ENV_FILE


def acme_env_available() -> bool:
    """True when the gitignored ``.env.acme`` credentials file is present."""
    return ACME_ENV_PATH.is_file()


def acme_api() -> ABConnectAPI:
    """Return a staging client authenticated as the Acme pickup-and-pack agent.

    Loads ``.env.acme`` when present; otherwise falls back to ``ABCONNECT_*``
    already in the environment (still pinned to staging). Always staging.
    """
    if acme_env_available():
        return ABConnectAPI(env_file=str(ACME_ENV_PATH))
    return ABConnectAPI(env="staging")


def acme_mutations_enabled() -> bool:
    """Acme is a throwaway staging agent — mutating the server is always OK.

    Examples that drive the Acme account use this instead of
    :func:`examples._capture.mutations_enabled` so they do not require the
    ``AB_RUN_MUTATIONS`` opt-in when run deliberately.
    """
    return True
