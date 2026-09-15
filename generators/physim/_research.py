"""Explicit access to frozen research fixtures for migration checks only."""

import os
from pathlib import Path


def activate_research():
    import physim

    root = Path(__file__).resolve().parents[2]
    legacy = str(root / "probes/legacy/physim/physim")
    if legacy not in physim.__path__:
        physim.__path__.append(legacy)
    os.environ.setdefault("PHYSIM_AGENTENV_DIR", str(root / "probes/blobs/agentenv"))
    return root
