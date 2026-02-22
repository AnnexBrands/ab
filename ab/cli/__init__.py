"""ABConnect endpoint CLI — ``ab`` (production) and ``abs`` (staging)."""

from ab.cli.__main__ import main


def main_prod() -> None:
    """Entry point for ``ab`` — production API."""
    main(env=None)


def main_staging() -> None:
    """Entry point for ``abs`` — staging API."""
    main(env="staging")
