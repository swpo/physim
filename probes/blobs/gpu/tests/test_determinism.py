"""tests/test_determinism.py — GPU determinism: same batch, same seed, run
twice -> bitwise identical. (Cross-batch-shape bitwise equality does NOT hold
on GPU: cuFFT plans/kernels differ by batch size; see GATES.md Gate PAD.)"""
import sys, os
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..")))
import jax.numpy as jnp
from blobgpu import pack_genomes, pack_states, make_stepper, diffusion_E
from blobgpu.core import batch_keys
from tests.gt_worlds import world
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..", "..", "l0",
                                                 "stage2", "lib")))
import genome as G

N, dx, dt = 64, 0.5, 0.02

def run_once(nsteps=500):
    gens = [world("pred"), world("m4"), world("bf")]
    params, struct, aux = pack_genomes(gens, dtype=np.float32)
    states = []
    for g in gens:
        F = G.state_vacuum(g, N)
        states.append(G.poke(F, g, 0, 16.0, 16.0, 2.0, 3.0, dx).astype(np.float32))
    Fb = pack_states(gens, states, struct["na_max"], struct["nc_max"])
    p = {k: jnp.asarray(v) for k, v in params.items()}
    p["E"] = diffusion_E(params["D"], N, dx, dt, np.float32)
    step = make_stepper(struct, N, dx, dt, noise=2e-3)
    keys = batch_keys([11, 12, 13])
    F = step(jnp.asarray(Fb), p, keys, 0, nsteps)
    return np.asarray(F)

def main():
    a, b = run_once(), run_once()
    same = np.array_equal(a, b)
    print(f"same-shape determinism (500 steps, noise on): {same}")
    print("PASS" if same else "FAIL")
    return 0 if same else 1

if __name__ == "__main__":
    raise SystemExit(main())
