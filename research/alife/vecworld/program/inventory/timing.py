"""Per-step wall time of candidate level-0 worlds, one CPU thread, small fixed step counts.

Collective worlds: their own numpy world.py (labkit ops with WORKERS=1), as claimed, no LabWorld noise.
Flow-Lenia: the VW-1 JAX port (flowlenia_jax.make_level), one substep with flow noise 0.5, jitted.
Classic families: minimal JAX float64 reference steps written here (not tuned).
Run: OMP_NUM_THREADS=1 XLA_FLAGS=... nice -n 10 python -B timing.py  -> timing.json
"""
import importlib.util
import json
import os
import sys
import time

import numpy as np

OUT = "/home/user/evalwork/vecworld/program/inventory/timing.json"
LAB = "/home/user/physim/research/alife"
C = LAB + "/collective/contrib"
WORLDS = {
    "fed_vortex_heredity": (C + "/20261027T0845-c53-fed-vortex-selection-claim/world.py", {"eps": 0.2, "mut_dt": 50.0}),
    "phase_membrane": (LAB + "/threads/autopoiesis/worlds/phase_membrane/world.py", None),
    "cips_iso": ("/home/user/swpo/residency-environments/scripts/physim/labworlds/worlds/cips_iso.py", None),
    "marangoni_rods": (C + "/20261026T0505-c34-nematic-marangoni/world.py", None),
}
sys.path.insert(0, LAB)
res = {}


def load(name, path, wp):
    os.environ["WORLD_P"] = json.dumps(wp or {})
    spec = importlib.util.spec_from_file_location("w_" + name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    if hasattr(m, "ops"):
        m.ops.WORKERS = 1
    return m


def tstate(s):
    out = {}
    for k, v in s.items():
        if isinstance(v, np.ndarray) and v.ndim >= 2 and k not in ("kx", "ky", "k2", "k2s", "da", "inv", "yy", "xx") \
                and not k.startswith("L"):
            out[k] = (list(v.shape), str(v.dtype))
    return out


for name, (path, wp) in WORLDS.items():
    m = load(name, path, wp)
    size = tuple(m.META["size"])
    s = m.init(0, size)
    for _ in range(5):
        s = m.step(s)
    n = 200
    t0 = time.perf_counter()
    for _ in range(n):
        s = m.step(s)
    dt = (time.perf_counter() - t0) / n
    res[name] = {"size": size, "native_dt": m.META.get("dt"), "steps_per_frame": m.META.get("steps_per_frame"),
                 "state": tstate(s), "s_per_step": dt, "steps_timed": n}
    print(name, res[name], flush=True)

# ---------------------------------------------------------------- JAX
import jax  # noqa: E402

jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp  # noqa: E402


def jtime(fn, x, n_inner=50, reps=3):
    """s per step of a jitted scan of n_inner steps (compile excluded)."""
    @jax.jit
    def run(x, key):
        def body(c, k):
            return fn(c, k), None
        return jax.lax.scan(body, x, jax.random.split(key, n_inner))[0]
    key = jax.random.key(0)
    y = run(x, key)
    jax.block_until_ready(y)
    best = 1e9
    for r in range(reps):
        t0 = time.perf_counter()
        y = run(y, jax.random.key(r + 1))
        jax.block_until_ready(y)
        best = min(best, (time.perf_counter() - t0) / n_inner)
    return best, y


def lap(u):
    return jnp.roll(u, 1, -1) + jnp.roll(u, -1, -1) + jnp.roll(u, 1, -2) + jnp.roll(u, -1, -2) - 4 * u


# Flow-Lenia, VW-1 port
sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/port")
import _paths  # noqa: E402,F401
import flowlenia_jax as FJ  # noqa: E402
import vw  # noqa: E402

for w in ("A_gliders", "B_swarm", "C_cells"):
    lev, cfg, meta = FJ.make_level(w, 0.5)
    x = lev.init(lev.params, jax.random.key(1))
    u0 = jnp.zeros(cfg.H * cfg.W)

    def fl(A, k, lev=lev, u0=u0):
        return lev.step(lev.params, A, vw.Noise(k, 0), u0)
    sp, y = jtime(fl, x, n_inner=20)
    res["flowlenia_" + w] = {"state": [list(x.shape), str(x.dtype)], "kernels": cfg.k, "s_per_substep": sp,
                             "mass_drift_rel": float(abs(y.sum() - x.sum()) / x.sum())}
    print(w, res["flowlenia_" + w], flush=True)

# Gray-Scott (Pearson 1993 parameters, explicit Euler, 5-point Laplacian), additive Gaussian noise on both fields
N = 256
Du, Dv, F, Kk, sig = 0.16, 0.08, 0.035, 0.060, 1e-3


def gs(x, k):
    u, v = x
    uvv = u * v * v
    xi = jax.random.normal(k, (2, N, N))
    return jnp.stack([u + Du * lap(u) - uvv + F * (1 - u) + sig * xi[0],
                      v + Dv * lap(v) + uvv - (F + Kk) * v + sig * xi[1]])


x = jnp.stack([jnp.ones((N, N)), jnp.zeros((N, N))]).at[:, 120:136, 120:136].set(jnp.array([0.5, 0.25])[:, None, None])
sp, _ = jtime(gs, x, 100)
res["gray_scott_256"] = {"state": [[2, N, N], "float64"], "s_per_step": sp}
print("gs", sp, flush=True)

# Lattice Boltzmann D2Q9 BGK, periodic, with a Gaussian random body force (fluctuating forcing)
NL = 128
cx = jnp.array([0, 1, 0, -1, 0, 1, -1, -1, 1])
cy = jnp.array([0, 0, 1, 0, -1, 1, 1, -1, -1])
wq = jnp.array([4 / 9] + [1 / 9] * 4 + [1 / 36] * 4)
tau = 0.6


def feq(rho, ux, uy):
    cu = 3 * (cx[:, None, None] * ux + cy[:, None, None] * uy)
    return wq[:, None, None] * rho * (1 + cu + 0.5 * cu ** 2 - 1.5 * (ux ** 2 + uy ** 2))


def lbm(f, k):
    rho = f.sum(0)
    fx = 1e-5 * jax.random.normal(k, (2, NL, NL))
    ux = ((f * cx[:, None, None]).sum(0) + 0.5 * fx[0]) / rho
    uy = ((f * cy[:, None, None]).sum(0) + 0.5 * fx[1]) / rho
    f = f - (f - feq(rho, ux, uy)) / tau
    f = f + 3 * wq[:, None, None] * (cx[:, None, None] * fx[0] + cy[:, None, None] * fx[1])
    return jnp.stack([jnp.roll(jnp.roll(f[i], cx[i], 1), cy[i], 0) for i in range(9)])


f0 = feq(jnp.ones((NL, NL)), 0.01 * jnp.sin(jnp.arange(NL) * 2 * jnp.pi / NL)[None, :] * jnp.ones((NL, 1)),
         jnp.zeros((NL, NL)))
sp, y = jtime(lbm, f0, 100)
res["lbm_d2q9_128"] = {"state": [[9, NL, NL], "float64"], "s_per_step": sp, "mass_drift_rel": float(abs(y.sum() - f0.sum()) / f0.sum())}
print("lbm", sp, flush=True)

# Ising, checkerboard Metropolis, one sweep = two half-sweeps
NI, beta = 128, 0.44
ii, jj = jnp.meshgrid(jnp.arange(NI), jnp.arange(NI), indexing="ij")
parity = (ii + jj) % 2


def ising(s, k):
    k1, k2 = jax.random.split(k)
    for p, kk in ((0, k1), (1, k2)):
        nb = jnp.roll(s, 1, 0) + jnp.roll(s, -1, 0) + jnp.roll(s, 1, 1) + jnp.roll(s, -1, 1)
        dE = 2 * s * nb
        acc = jax.random.uniform(kk, s.shape) < jnp.exp(-beta * dE)
        s = jnp.where((parity == p) & acc, -s, s)
    return s


s0 = jnp.where(jax.random.uniform(jax.random.key(3), (NI, NI)) < 0.5, 1, -1).astype(jnp.int8)
sp, _ = jtime(lambda s, k: ising(s.astype(jnp.float64), k).astype(jnp.int8), s0, 100)
res["ising_128_sweep"] = {"state": [[NI, NI], "int8"], "s_per_sweep": sp}
print("ising", sp, flush=True)

# Particle life: N particles, K types, all-pairs piecewise-linear forces, periodic box, overdamped + Langevin noise
NP, KT, BOX, RMAX = 1024, 6, 1.0, 0.1
Amat = jax.random.uniform(jax.random.key(5), (KT, KT), minval=-1, maxval=1)
types = jnp.arange(NP) % KT


def plife(x, k):
    d = x[None, :, :] - x[:, None, :]
    d = d - BOX * jnp.round(d / BOX)
    r = jnp.sqrt((d ** 2).sum(-1) + 1e-12) / RMAX
    a = Amat[types[:, None], types[None, :]]
    beta_ = 0.3
    fmag = jnp.where(r < beta_, r / beta_ - 1, jnp.where(r < 1, a * (1 - jnp.abs(2 * r - 1 - beta_) / (1 - beta_)), 0.0))
    fvec = (fmag[..., None] * d / (r[..., None] * RMAX)).sum(1)
    return (x + 0.01 * RMAX * fvec + 1e-4 * jax.random.normal(k, x.shape)) % BOX


p0 = jax.random.uniform(jax.random.key(6), (NP, 2))
sp, _ = jtime(plife, p0, 50)
res["particle_life_1024"] = {"state": [[NP, 2], "float64"], "types": KT, "s_per_step": sp}
print("plife", sp, flush=True)

# Neural CA (Mordvintsev et al. 2020 shape): 16 channels, 64^2, identity+sobel perception, 48->128->16, stochastic mask
NC, CH, HID = 64, 16, 128
kw = jax.random.split(jax.random.key(7), 2)
W1 = 0.05 * jax.random.normal(kw[0], (3 * CH, HID))
W2 = 0.0 * jax.random.normal(kw[1], (HID, CH)) + 1e-3


def nca(x, k):
    gx = (jnp.roll(x, -1, 1) - jnp.roll(x, 1, 1)) / 2
    gy = (jnp.roll(x, -1, 0) - jnp.roll(x, 1, 0)) / 2
    z = jnp.concatenate([x, gx, gy], -1)
    dx = jax.nn.relu(z @ W1) @ W2
    m = jax.random.uniform(k, (NC, NC, 1)) < 0.5
    return x + dx * m


x0 = jnp.zeros((NC, NC, CH)).at[NC // 2, NC // 2].set(1.0)
sp, _ = jtime(nca, x0, 50)
res["nca_64x16"] = {"state": [[NC, NC, CH], "float64"], "s_per_step": sp}
print("nca", sp, flush=True)

res["env"] = {"OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"), "XLA_FLAGS": os.environ.get("XLA_FLAGS"),
              "jax": jax.__version__, "numpy": np.__version__, "note": "wall s per step on a shared 4-core box, 1 thread, nice 10"}
json.dump(res, open(OUT, "w"), indent=1, default=str)
print("wrote", OUT)
