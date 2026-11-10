"""Where the public simulator sources live: physim2/_vendor in an agent workspace (verbatim copies made by
evaluator/build_workspace.py, hashes in MANIFEST.json), or the repository tree in a development checkout."""
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
_B = os.path.join(HERE, "_vendor")
BUNDLED = os.path.isdir(_B)
VEC = _B if BUNDLED else os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def add(*rel):
    """Put VEC/<rel> first on sys.path (in the given order)."""
    for r in reversed(rel):
        p = os.path.join(VEC, r)
        if p in sys.path:
            sys.path.remove(p)
        sys.path.insert(0, p)
