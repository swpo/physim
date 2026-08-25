"""tests/gt_worlds.py — frozen ground-truth worlds (JSON round-trip exact).
Prefers the live builders (local repo); falls back to data/gt_worlds.json
(pod mirror). Frozen 2026-02-25 from complexity/worlds.py; parity checked.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
GPU = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(GPU, "data", "gt_worlds.json")

_d = json.load(open(DATA))
FROZEN = _d["worlds"]
KICKS = {k: {int(a): v for a, v in m.items()} for k, m in _d["kicks"].items()}
NAMES = ["m0", "m4", "xv", "bf", "pred", "coex", "mv3"]


def world(name):
    import copy
    return copy.deepcopy(FROZEN[name])


def check_vs_builders():
    """Local-only: frozen == live builders?"""
    sys.path.insert(0, os.path.normpath(os.path.join(GPU, "..", "l0", "complexity")))
    sys.path.insert(0, os.path.normpath(os.path.join(GPU, "..", "l0", "stage2", "lib")))
    import worlds as W
    import genome as G
    ok = True
    for n in NAMES:
        a = json.loads(json.dumps(G.genome_json(W.WORLDS[n]())))
        b = json.loads(json.dumps(FROZEN[n]))
        if a != b:
            print("MISMATCH", n); ok = False
    return ok


if __name__ == "__main__":
    print("frozen==builders:", check_vs_builders())
