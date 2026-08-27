"""backend_gpu.py — soup_sim_v2-contract sim backend on blobgpu (GPU/JAX).

Drop-in module for assay_v2's SS2 dependency: init_soup / advance /
snapshot_rec / save_run with identical signatures + record contract.
ONLY the stepping backend is swapped (blobgpu jitted kernel; certified
gates in probes/blobs/gpu/GATES.md). ICs, record grids, exits, thresholds:
soup_sim_v2 verbatim (blobgpu reuses V2.init_soup + V2._record).

Path-relative: this file lives at probes/blobs/l0/deepsearch/gpu_run/, the
same relative layout on laptop and pod.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BLOBS = os.path.normpath(os.path.join(HERE, "..", "..", ".."))   # probes/blobs
GPU = os.path.join(BLOBS, "gpu")
for p in (GPU,):
    if p not in sys.path:
        sys.path.insert(0, p)

import blobgpu.soup as BS                      # noqa: E402
import soup_sim_v2 as _V2                      # noqa: E402 (via BS path setup)
from soup_sim import NOISE, N_SOUP, save_run, load_run   # noqa: E402,F401


def init_soup(g, L=128.0, seed=0, n_soup=N_SOUP, dtype="f32", kicks=None,
              noise=NOISE, workers=4):
    """workers accepted for signature parity (CPU FFT threads; unused)."""
    return BS.init_soup_gpu(g, L=L, seed=seed, n_soup=n_soup, dtype=dtype,
                            kicks=kicks, noise=noise)


def advance(S, T_target):
    return BS.advance_gpu(S, T_target)


def snapshot_rec(S):
    return BS.snapshot_rec_gpu(S)
