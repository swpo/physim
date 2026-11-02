"""Bundle entry point for cips_iso.py with the suite's declared noise bounds.

The suite declares LabWorld.noise_bounds = {"e": [0.0, 1.0], "p": [0.0, 1.0]}: right after its dynamics noise is added,
each bounded field is projected onto its range. The physim-lab-bundle-v1 declaration has no noise_bounds key, so
this file makes the same projection at the start of each native step. LabStepper runs injection, noise, then the
world's step, so the step sees the same doubles (gc_bundle.py verify checks a frozen truth member bit for bit).
Everything else is cips_iso.py, loaded from this folder as a fresh module.
"""
import importlib.util
from pathlib import Path

import numpy as np

NOISE_BOUNDS = {'e': (0.0, 1.0), 'p': (0.0, 1.0)}

_spec = importlib.util.spec_from_file_location(__name__ + "_inner", Path(__file__).with_name('cips_iso.py'))
_inner = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_inner)
P = _inner.P
init = _inner.init
if hasattr(_inner, "ops"):
    ops = _inner.ops


def step(s):
    for f, (lo, hi) in NOISE_BOUNDS.items():
        s[f] = np.clip(s[f], lo, hi)
    return _inner.step(s)
