"""tests/test_padding.py — padding inertness is EXACT.

Claim (packing.py): padding a world into a larger (na_max, nc_max) layout does
not change its trajectory AT ALL (bit-for-bit on the same backend/dtype), and
padded slots stay exactly 0. Verified for bf (tanh + bilin) and xv, solo vs
mixed batch, plus noise-stream batch invariance (per-world keys).
"""
import sys, numpy as np
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
_GPU = os.path.normpath(os.path.join(_HERE, ".."))
_BLOBS = os.path.normpath(os.path.join(_GPU, ".."))
sys.path.insert(0, _GPU)
sys.path.insert(0, os.path.join(_BLOBS, "l0", "stage2", "lib"))
sys.path.insert(0, os.path.join(_BLOBS, "l0", "complexity"))
import genome as G
from tests.gt_worlds import world as _gtw
class W:
    WORLDS = {k: (lambda k=k: _gtw(k)) for k in ("bf", "xv", "pred", "m4")}
import jax.numpy as jnp
from blobgpu import pack_genomes, pack_states, unpack_state, make_stepper, diffusion_E
from blobgpu.core import batch_keys

N, dx, dt = 64, 0.5, 0.02
NSTEP = 200


def run_batch(gens, states, nsteps=NSTEP, noise=0.0, seeds=None):
    params, struct, aux = pack_genomes(gens, dtype=np.float32)
    Fb = pack_states(gens, [s.astype(np.float32) for s in states],
                     struct["na_max"], struct["nc_max"])
    p = {k: jnp.asarray(v) for k, v in params.items()}
    p["E"] = diffusion_E(params["D"], N, dx, dt, np.float32)
    step = make_stepper(struct, N, dx, dt, noise=noise)
    keys = batch_keys(seeds or list(range(len(gens))))
    F = step(jnp.asarray(Fb), p, keys, 0, nsteps)
    return np.asarray(F), struct


def state_for(g):
    F = G.state_vacuum(g, N)
    return G.poke(F, g, 0, 16.0, 16.0, 2.0, 3.0, dx)


def main():
    import jax
    on_gpu = jax.devices()[0].platform != "cpu"
    # GPU: cuFFT plan/kernel choice depends on batch shape -> last-bit
    # differences across batch shapes are expected; gate is a short-T tol.
    TOL = 1e-5 if on_gpu else 0.0
    failures = []
    g_bf, g_xv, g_pred = W.WORLDS["bf"](), W.WORLDS["xv"](), W.WORLDS["pred"]()
    for gname, g in (("bf", g_bf), ("xv", g_xv)):
        s = state_for(g)
        F1, st1 = run_batch([g], [s])
        ref = unpack_state(g, F1[0], st1["na_max"])
        F2, st2 = run_batch([g, g_pred], [s, state_for(g_pred)])
        got = unpack_state(g, F2[0], st2["na_max"])
        d = float(np.linalg.norm(ref - got) / max(np.linalg.norm(ref), 1e-30))
        exact = (d == 0.0) if TOL == 0.0 else (d <= TOL)
        na, nc = len(g["acts"]), len(g["chans"])
        pads = np.concatenate([F2[0][na:st2["na_max"]],
                               F2[0][st2["na_max"] + nc:]])
        pad_zero = bool((pads == 0.0).all())
        print(f"{gname}: padded-vs-solo relL2={d:.2e} ok={exact} "
              f"pad-slots-zero={pad_zero}")
        if not exact:
            failures.append((gname, "traj", d))
        if not pad_zero:
            failures.append((gname, "pad", float(np.abs(pads).max())))

    g = W.WORLDS["m4"]()
    s = state_for(g)
    Fa, sta = run_batch([g], [s], noise=2e-3, seeds=[7])
    Fb_, stb = run_batch([g, g_pred, g_xv],
                         [s, state_for(g_pred), state_for(g_xv)],
                         noise=2e-3, seeds=[7, 8, 9])
    ra = unpack_state(g, Fa[0], sta["na_max"])
    rb = unpack_state(g, Fb_[0], stb["na_max"])
    dn = float(np.linalg.norm(ra - rb) / max(np.linalg.norm(rb), 1e-30))
    same = (dn == 0.0) if TOL == 0.0 else (dn <= TOL)
    print(f"noise stream batch-invariant (m4, seed 7): relL2={dn:.2e} ok={same}")
    if not same:
        failures.append(("m4", "noise-batch", dn))

    print("PASS" if not failures else f"FAIL {failures}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
