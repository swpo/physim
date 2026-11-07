"""Where each suite in use lives and where its shadow reports were written."""
from pathlib import Path

GC = Path("/home/user/evalwork/gc_suites")
OUT = GC / "rescore_fair" / "out"
SUITE_DIRS = {
    ("vortex", "main"): GC / "vortex" / "suite",
    ("vortex", "formation"): GC / "vortex" / "formation",
    ("vortex", "long2"): GC / "vortex" / "long2",
    ("phase_membrane", "main_iter1"): GC / "phase_membrane" / "suite",
    ("phase_membrane", "main_iter2"): GC / "phase_membrane" / "iter2" / "suite",
    ("phase_membrane", "formation"): GC / "phase_membrane" / "formation" / "suite",
    ("cips", "main_iter1"): GC / "cips" / "suite",
    ("cips", "main_iter2"): GC / "cips" / "iter2" / "suite",
    ("cips", "formation"): GC / "cips" / "formation" / "suite",
    ("rods", "main_iter1"): GC / "rods" / "suite",
    ("rods", "main_iter2"): GC / "rods" / "iter2" / "suite",
    ("rods", "formation"): GC / "rods" / "formation" / "suite",
}


def folder(world, label, which):
    """which: 'stored' (the suite itself), 'plugin' or 'fair' (shadow)."""
    return SUITE_DIRS[(world, label)] if which == "stored" else OUT / world / label / which


def getter(which):
    import json

    def get(world, label, name):
        p = folder(world, label, which) / name
        if not p.exists():
            p = SUITE_DIRS[(world, label)] / name       # suite.json is not copied for the vortex shadows
        return json.loads(p.read_text())
    return get
