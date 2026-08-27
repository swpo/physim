"""blobkit.worlds — packaged world registry (NO tree-walking).

The old complexity/worlds.py rebuilt worlds at call time by walking the source
tree (l0/stage3/engine_10748.json, l0/stage2/merged_results.json, stage3
encounter files, machinev3/lib build_world) — the #1 cause of broken pod
deployments. Here every certified world was EXTRACTED ONCE from the source
tree by running those exact builders (tools/extract_worlds.py; provenance in
MANIFEST.md) into blobkit/data/worlds/<name>.json.

API:
  load(name)      -> deep, mutable genome dict (fresh copy per call)
  names()         -> sorted registry names
  WORLDS          -> {name: zero-arg builder} (drop-in for old worlds.WORLDS)
  KICKS           -> {genome_id: {act: kick_px}} protocol deviations
  GT_SET          -> the 7 ground-truth worlds used by the parity/metric gates

Data override: set BLOBKIT_DATA=/some/dir to load <dir>/worlds/<name>.json
instead of the packaged copy (per-name fallback to packaged data).
"""
import copy
import json
import os

NAMES = [
    "m0", "m4", "xv", "bf", "pred", "coex", "mv3",          # ground truths
    "ds3_014", "ds3_017", "ds6_000", "g0_jit_11",           # champions
    "engine_10748", "rail_111_17", "s2_128_26", "s2_118_41",  # parts/seeds
]
GT_SET = ["m0", "m4", "xv", "bf", "pred", "coex", "mv3"]

# Documented protocol deviation (unchanged from complexity/worlds.py): mv3
# engine blobs are operated kicked (their certified launch convention),
# kick_px per act; all other worlds: no per-world kick override.
KICKS = {"gt_mv3": {0: 0.5}}


def _packaged_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "data", "worlds")


def _candidate_paths(name):
    env = os.environ.get("BLOBKIT_DATA")
    if env:
        yield os.path.join(env, "worlds", name + ".json")
    yield os.path.join(_packaged_dir(), name + ".json")


def load(name):
    """Load world/genome `name` from the registry. Returns a fresh dict."""
    for p in _candidate_paths(name):
        if os.path.exists(p):
            with open(p) as f:
                return json.load(f)
    raise KeyError(f"unknown world {name!r}; registry has {sorted(NAMES)} "
                   f"(BLOBKIT_DATA={os.environ.get('BLOBKIT_DATA')!r})")


def names():
    return sorted(NAMES)


def kicks_for(g):
    """Per-act kick overrides for a genome dict or id (None if none)."""
    gid = g.get("id") if isinstance(g, dict) else g
    k = KICKS.get(gid)
    return copy.deepcopy(k) if k else None


# Drop-in for the old complexity/worlds.py surface: WORLDS[name]() -> genome.
WORLDS = {n: (lambda n=n: load(n)) for n in NAMES}
