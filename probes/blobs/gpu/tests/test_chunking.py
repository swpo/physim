"""tests/test_chunking.py — chunked continuation == single long run (bitwise),
and GPU-vs-CPU f64 short-trajectory sanity (T=25tu, noise=0) for one world.
Local (CPU-JAX) runnable; the full 7-world T=100 f64 gate lives in gate_f64.py.
"""
import sys, numpy as np
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..")))
import blobgpu.soup as BS
import soup_sim_v2 as V2
from tests.gt_worlds import world as _gtw
class W:
    WORLDS = {k: (lambda k=k: _gtw(k)) for k in ("m4",)}

def main():
    fails = []
    g = W.WORLDS["m4"]()
    # --- chunking bitwise (f32, with noise: the hard case, RNG folds)
    S1 = BS.init_soup_gpu(g, L=64.0, seed=3, dtype="f32")
    BS.advance_gpu(S1, 100.0)
    S2 = BS.init_soup_gpu(g, L=64.0, seed=3, dtype="f32")
    for T in (25.0, 50.0, 75.0, 100.0):
        BS.advance_gpu(S2, T)
    same = np.array_equal(np.asarray(S1["F"]), np.asarray(S2["F"]))
    n1 = [len(b) for b in S1["blobs"][0]]
    n2 = [len(b) for b in S2["blobs"][0]]
    print(f"chunked==single (f32+noise, T=100): fields {same} records {n1 == n2}")
    if not (same and n1 == n2):
        fails.append("chunking")

    # --- f64 noise-free GPU vs CPU trajectory, T=25tu
    Sg = BS.init_soup_gpu(g, L=64.0, seed=1, dtype="f64", noise=0.0)
    BS.advance_gpu(Sg, 25.0)
    Sc = V2.init_soup(g, L=64.0, seed=1, dtype="f64", noise=0.0, workers=2)
    V2.advance(Sc, 25.0)
    a, b = np.asarray(Sg["F"], np.float64), np.asarray(Sc["F"], np.float64)
    rel = float(np.linalg.norm(a - b) / np.linalg.norm(b))
    print(f"f64 noise-free GPU-vs-CPU relL2 @T=25: {rel:.3e}")
    if rel > 1e-9:
        # jnp.fft vs scipy.fft in f64 should agree to ~1e-12 relative per step
        fails.append(f"f64-short {rel:.1e}")
    print("PASS" if not fails else f"FAIL {fails}")
    return 0 if not fails else 1

if __name__ == "__main__":
    raise SystemExit(main())
