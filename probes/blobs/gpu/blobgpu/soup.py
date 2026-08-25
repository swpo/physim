"""blobgpu/soup.py — drop-in GPU backend for the S1 soup assay (soup_sim_v2).

Contract: identical records to soup_sim_v2 (ts/blobs/mass/ct/patches/orgs/memf/
snaps + snapshot_rec keys). ICs are built by soup_sim_v2.init_soup itself
(same numpy RNG -> bit-identical seeded states). Only the stepping loop is
swapped: chunks of REC (250 steps) run on the JAX device (fori_loop inside one
jit), fields are pulled to host at each record point and fed to the verbatim
CPU _record. Blob tracking stays on CPU (locked measurement code).

Noise: jax threefry (per-world key, folded on absolute step + field index).
Different stream than CPU PCG64, same law -> descriptor-level parity gate.
Chunked continuation is bitwise-identical to a single long GPU run at the same
final T (absolute-step key folds; verified in tests/test_chunking.py).

Usage:
  S = init_soup_gpu(g, L=128.0, seed=1)              # single world
  advance_gpu(S, 2500.0); rec = snapshot_rec_gpu(S)  # same as v2

  SS = init_soup_gpu_batch([(g1, 1), (g2, 1), ...])  # one tensor, B worlds
  advance_gpu_batch(SS, 2500.0)
  recs = [snapshot_rec_gpu(S) for S in SS["worlds"]]

Do NOT wire into the live v2 run; this is the future-swap hook.
"""
import os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CPLX = os.path.normpath(os.path.join(HERE, "..", "..", "l0", "complexity"))
LIB = os.path.normpath(os.path.join(HERE, "..", "..", "l0", "stage2", "lib"))
for p in (CPLX, LIB):
    if p not in sys.path:
        sys.path.insert(0, p)

import soup_sim_v2 as V2                       # noqa: E402  (locked CPU assay)
from soup_sim import NOISE, N_SOUP             # noqa: E402
from .packing import pack_genomes, pack_states, unpack_state   # noqa: E402
from .core import make_stepper, diffusion_E, batch_keys        # noqa: E402

import jax.numpy as jnp                        # noqa: E402


# ------------------------------------------------------------- single world
def init_soup_gpu(g, L=128.0, seed=0, n_soup=N_SOUP, dtype="f32", kicks=None,
                  noise=NOISE, gpu_seed=None):
    """soup_sim_v2.init_soup + device packing. gpu_seed defaults to seed."""
    S = V2.init_soup(g, L=L, seed=seed, n_soup=n_soup, dtype=dtype,
                     kicks=kicks, noise=noise, workers=0)
    _attach_gpu(S, [g], [S["F"]], [seed if gpu_seed is None else gpu_seed],
                dtype, noise)
    return S


def _attach_gpu(S_master, gens, states, gpu_seeds, dtype, noise):
    npdt = np.float32 if dtype == "f32" else np.float64
    if npdt is np.float64:
        from .core import enable_x64
        enable_x64()          # must precede device-array creation (JAX trap:
                              # without x64, f64 inputs silently become f32)
    N = states[0].shape[-1]
    dx, dt = 0.5, 0.02
    params, struct, aux = pack_genomes(gens, dtype=npdt)
    Fb = pack_states(gens, [np.asarray(s, npdt) for s in states],
                     struct["na_max"], struct["nc_max"])
    p = {k: jnp.asarray(v) for k, v in params.items()}
    p["E"] = diffusion_E(params["D"], N, dx, dt, npdt)
    G = dict(params=p, struct=struct,
             step=make_stepper(struct, N, dx, dt, noise=noise),
             keys=batch_keys(gpu_seeds), F=jnp.asarray(Fb),
             gens=gens, N=N)
    S_master["_gpu"] = G
    return G


def _pull(G, acts_only=False):
    """Device -> host, per-world natural layout list. Blocks.
    acts_only: pull just the activator block (tracking records need only u;
    4x less PCIe traffic + f64 conversion). Channel slots are filled with 0."""
    na_max = G["struct"]["na_max"]
    if acts_only:
        Fh = np.asarray(G["F"][:, :na_max])
        out = []
        for b, g in enumerate(G["gens"]):
            na, nc = len(g["acts"]), len(g["chans"])
            s = np.zeros((na + nc,) + Fh.shape[-2:], Fh.dtype)
            s[:na] = Fh[b, :na]
            out.append(s)
        return out
    Fh = np.asarray(G["F"])
    return [unpack_state(g, Fh[b], na_max)
            for b, g in enumerate(G["gens"])]


def advance_gpu(S, T_target):
    """GPU version of soup_sim_v2.advance. Same record grid, same exits."""
    t0w = time.time()
    dt = S["dt"]
    steps_target = int(round(T_target / dt))
    if steps_target % S["crec"] != 0:
        raise ValueError("T_target must be a multiple of CREC")
    G = S["_gpu"]
    rec = S["rec"]
    t = S["t_step"]
    while S["status"] == "ok" and t <= steps_target:
        if S["recorded_at"] < t:
            S["F"] = _pull(G)[0]
            ok = V2._record(S, t)
            S["recorded_at"] = t
            if not ok:
                break
        if t == steps_target:
            break
        n = min(rec, steps_target - t)
        G["F"] = G["step"](G["F"], G["params"], G["keys"], t, n)
        t += n
    S["t_step"] = t
    S["wall_s"] += time.time() - t0w
    return S["status"]


def snapshot_rec_gpu(S):
    return V2.snapshot_rec(S)


# ------------------------------------------------------------- batched pop
def init_soup_gpu_batch(jobs, L=128.0, dtype="f32", noise=NOISE, kicks_map=None):
    """jobs: list of (genome, seed). One padded tensor for the whole batch.
    Returns SS = dict(worlds=[S...], _gpu=...). Each S is a full v2 state dict
    (independent records); stepping is shared."""
    worlds, gens, states, seeds = [], [], [], []
    for (g, seed) in jobs:
        kicks = (kicks_map or {}).get(g.get("id"))
        S = V2.init_soup(g, L=L, seed=seed, dtype=dtype, kicks=kicks,
                         noise=noise, workers=0)
        worlds.append(S); gens.append(g); states.append(S["F"]); seeds.append(seed)
    master = dict(worlds=worlds)
    G = _attach_gpu(master, gens, states, seeds, dtype, noise)
    for S in worlds:
        S["_gpu"] = G          # shared handle (advance via the batch driver)
    return master


def advance_gpu_batch(SS, T_target, overlap=True, progress=None):
    """Advance all worlds to T_target on one tensor. CPU tracking overlaps the
    next GPU chunk (JAX async dispatch). Worlds whose status != ok stop being
    recorded but keep stepping (padding-inert, no cross-talk)."""
    t0w = time.time()
    worlds = SS["worlds"]
    G = worlds[0]["_gpu"]
    dt = worlds[0]["dt"]
    rec = worlds[0]["rec"]
    steps_target = int(round(T_target / dt))
    if steps_target % worlds[0]["crec"] != 0:
        raise ValueError("T_target must be a multiple of CREC")
    ok_worlds = [S for S in worlds if S["status"] == "ok"]
    if not ok_worlds:
        return [S["status"] for S in worlds]
    t = ok_worlds[0]["t_step"]
    assert all(S["t_step"] == t for S in ok_worlds), "batch worlds out of sync"

    from concurrent.futures import ThreadPoolExecutor
    n_rec_threads = min(8, os.cpu_count() or 1)

    def record_one(args):
        S, Fh, t_now = args
        if S["status"] != "ok" or S["recorded_at"] >= t_now:
            return
        S["F"] = Fh
        ok = V2._record(S, t_now)          # per-world state: thread-safe
        S["recorded_at"] = t_now
        if not ok:
            S["_t_stopped"] = t_now        # CPU contract: stop at exit point

    def record_all(t_now, F_list):
        if n_rec_threads > 1 and len(worlds) > 4:
            with ThreadPoolExecutor(n_rec_threads) as ex:
                list(ex.map(record_one, [(S, Fh, t_now)
                                         for S, Fh in zip(worlds, F_list)]))
        else:
            for S, Fh in zip(worlds, F_list):
                record_one((S, Fh, t_now))

    crec = worlds[0]["crec"]

    def full_pull_needed(t_now):
        tt = t_now * dt
        if t_now % crec == 0:
            return True
        for S in worlds:                     # pending snapshot due?
            if S["snap_t"] and tt >= S["snap_t"][0] - 1e-9:
                return True
        return False

    while t <= steps_target:
        full = full_pull_needed(t)
        F_host = _pull(G, acts_only=not full)  # blocks on chunk ending at t
        if t < steps_target and overlap:      # dispatch next chunk first
            n = min(rec, steps_target - t)
            G["F"] = G["step"](G["F"], G["params"], G["keys"], t, n)
            record_all(t, F_host)             # CPU tracking overlaps GPU
            t += n
        else:
            record_all(t, F_host)
            if t == steps_target:
                break
            n = min(rec, steps_target - t)
            G["F"] = G["step"](G["F"], G["params"], G["keys"], t, n)
            t += n
        if progress and (t % (rec * 100) == 0):
            progress(t * dt)
    wall = time.time() - t0w
    for S in worlds:
        if "_t_stopped" in S:
            S["t_step"] = S.pop("_t_stopped")   # stopped this call
        elif S["status"] == "ok":
            S["t_step"] = steps_target
        # else: stopped in an earlier call; keep its t_step
        S["wall_s"] += wall / len(worlds)     # amortized per-world wall
    return [S["status"] for S in worlds]


# ------------------------------------------------------------- run_soup_gpu
def run_soup_gpu(g, L=128.0, T=5000.0, seed=0, n_soup=N_SOUP, dtype="f32",
                 kicks=None, noise=NOISE, chunk_tu=None):
    """Drop-in for soup_sim.run_soup / the v2 init+advance+snapshot pipeline:
    same record dict keys (v2 superset), same protocol, GPU stepping.
    chunk_tu: optional intermediate advance targets (multiples of CREC)."""
    S = init_soup_gpu(g, L=L, seed=seed, n_soup=n_soup, dtype=dtype,
                      kicks=kicks, noise=noise)
    S["snap_t"] = sorted({0.0, 250.0, T / 2, float(T)})
    targets = list(np.arange(chunk_tu, T + 1e-9, chunk_tu)) if chunk_tu else [T]
    for Tt in targets:
        if advance_gpu(S, float(Tt)) != "ok":
            break
    return snapshot_rec_gpu(S)
