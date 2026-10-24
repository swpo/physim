"""World contract and loader.

A world is ONE Python file (world.py) that defines:

    META = {
        "name": "orbium-ref",          # short id, unique within the thread
        "family": "lenia",             # lenia | flow-lenia | particle | phase-field | chemotaxis | rd | ...
        "parent": None,                # path or id of the world this was mutated from (lineage)
        "mutation": "",                # one line: what changed relative to the parent, and why
        "size": (256, 256),            # default grid (H, W) for field worlds
        "steps_per_frame": 10,         # internal steps between recorded frames
        "dt": 0.1,                     # simulation time per internal step (for reporting)
        "channels": ["A"],             # names of the channels returned by fields()
        "matter": None,                # channel indices that define "stuff" for tracking (None = all)
        "threshold": None,             # absolute segmentation threshold on the matter field (None = auto)
        "smooth": 1.0,                 # Gaussian blur (px) of the matter field before segmentation
        "periodic": True,              # False for open boundaries
        # particle worlds only:
        "domain": None,                # (Lx, Ly) world units, or None for an open plane
        # optional measurement settings (labkit v0.2):
        "lineage_k": None,             # lineage window K in recorded frames (None = 20; CLI --lineage-k wins)
        "radial_channels": None,       # channels (indices or names) for radial profiles (None = all)
        "species": None,               # {"prey": [0], "predator": [1, 2]}: separate tracking per species
    }

    def init(seed: int, size: tuple) -> state
    def step(state) -> state                 # one internal step (may mutate and return state)
    def fields(state) -> np.ndarray          # (C, H, W) float; channels to render and measure

Optional hooks:

    def particles(state) -> np.ndarray       # (N, 2) positions or (N, 3) with a type column
    def matter(fields) -> np.ndarray         # (H, W) custom "stuff" field for tracking
    def damage(state, mask) -> state         # erase matter where mask (H, W) bool is True

damage() is called by `--damage FRAME:FRAC[:MODE]`. labkit chooses the target (a mature,
compact individual of about median size, see labkit/metrics.py) and builds the mask (core
disk, rim disk or half-plane cut). The hook should erase matter under the mask (remove
it, or reset it to the background state); it should not turn it into the individual's
resource. Whatever the hook does, labkit MEASURES the loss as the drop of the matter
field inside the target's component just before vs just after the call and reports that.

Species: META["species"] maps a name to channel indices (or names). Each species is
segmented, tracked and given a lineage on its own channel sum with its own robust range,
in addition to the main matter tracking. META["radial_channels"] selects the channels of
the radial boundary profiles (default: all channels, including ones outside the matter
set, since a membrane channel is often not the tracked one).

Loading a world through labkit never writes __pycache__ next to the world file (importing
labkit sets sys.dont_write_bytecode first; see labkit/__init__.py).

Everything else (numerics, parameters, RNG) lives inside the state. A world must be
deterministic given the seed. Keep world files self-contained so anyone can fork one
by copying the file.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

DEFAULT_META = {
    "name": None,
    "family": "unknown",
    "parent": None,
    "mutation": "",
    "size": (256, 256),
    "steps_per_frame": 1,
    "dt": 1.0,
    "channels": None,
    "matter": None,
    "threshold": None,
    "smooth": 1.0,
    "periodic": True,
    "domain": None,
    "lineage_k": None,
    "radial_channels": None,
    "species": None,
}


def load_world(path):
    """Import a world file and return the module with META filled from defaults."""
    path = Path(path).resolve()
    if path.is_dir():
        path = path / "world.py"
    name = "world_" + "_".join(path.parts[-3:]).replace(".", "_").replace("-", "_")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    for fn in ("init", "step", "fields"):
        if not hasattr(mod, fn):
            raise AttributeError(f"{path} must define {fn}()")
    meta = dict(DEFAULT_META)
    meta.update(getattr(mod, "META", {}))
    if meta["name"] is None:
        meta["name"] = path.parent.name
    meta["path"] = str(path)
    mod.META = meta
    return mod
