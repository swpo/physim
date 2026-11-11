"""s0 -- stage 0 of the membrane carrier (round 6, dials, study B of ../PLAN.md): the CPU gate.

    python -B s0.py presmoke            every stage once at full array shapes with short counts; prints the rate
    python -B s0.py scanV PART NPARTS   scan V (hidden parameter set of the public law), a share of its points
    python -B s0.py scanC PART NPARTS   scan C (ranges of rho, D_X, a0), a share of its points
    python -B s0.py ranges              apply DECLARED.md 2.6 to the scans: ranges.json + ranges.sha256
    python -B s0.py gate SEED ARM       one seed and arm (main | control) of the gate
    python -B s0.py analyse             pooled tables and the verdict: analysis.json
    python -B s0.py align               the gate's code path on the designer's pilot seed 5 against his file (not fatal)

Sizes come from S0_SIZE (full | tiny); outputs go to $OUT (default ./out). DECLARED.md in this folder is the
specification; nothing here may change a declared size or rule. State given, 64 px, CPU. Every hidden value is a
PILOT value: never to be reused as an exam.

Imported unchanged: the designer's `sublevel`, `screen`, `gvh` (sublevel_second) and the adversary's `adv_act`
(its grid and command filter) and `adv_sim` (its blur matrix). `gvh.py`'s and `adv_act.py`'s main() are single
scripts that write into their own folders, so their recipes are re-stated here as functions (G1-G4 line for line
from gvh.py with the fitting scale as an argument; A_act from adv_act.py with the grid, filter, 2 futures and
common random numbers it uses).
"""
import hashlib
import json
import math
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
DIALS = os.path.dirname(HERE)
VW1 = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "vw1"))
sys.path.insert(0, VW1)
import vw  # noqa: E402  (the repository's copy, before track1/membrane_world/_paths.py adds its own path)

for _p in (os.path.join(DIALS, "crit_adversary"), os.path.join(DIALS, "sublevel_second")):
    sys.path.insert(0, _p)

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import sublevel as SL  # noqa: E402
from sublevel import MJ, MW  # noqa: E402
import screen as SC  # noqa: E402
import gvh as GV  # noqa: E402
import adv_act as AA  # noqa: E402
from adv_sim import blur_matrix  # noqa: E402
from vw.scoring import energy_fair, energy_loo  # noqa: E402
from vw.world import Carry  # noqa: E402

PILOT = "PILOT_NEVER_REUSE_AS_EXAM"
OUT = os.environ.get("OUT", os.path.join(HERE, "out"))
SIZE = os.environ.get("S0_SIZE", "full")
PX, T0, H, NATS = 64, 150, 32, 300.0
HS4 = (4, 8, 16, 32)                     # recorded horizons; the rules use 8, 16, 32 (columns 1, 2, 3)
EX = (1, 2, 3)
CHUNK = 48
SEEDS = (31, 32, 33, 34, 35, 36, 37, 38)
ARMS = ("main", "control")
CENTRE = {"rho": 0.02, "DX": 0.5, "a0": 0.03}
SCAN_C = {"a0": (0.02, 0.025, 0.03, 0.04, 0.05), "rho": (0.005, 0.01, 0.02, 0.04, 0.08), "DX": (0.05, 0.1, 0.2, 0.35, 0.5)}
V_PARAMS = ("DS", "DK", "DL", "Dp", "r", "a", "th", "F", "c", "b", "dK", "dL", "chi")
V_FACTORS = (0.8, 0.9, 1.1, 1.2)
FAMILY = {"DS": "transport", "DK": "transport", "DL": "transport", "Dp": "transport", "r": "phase", "a": "phase", "th": "phase",
          "F": "metabolism", "c": "metabolism", "b": "metabolism", "dK": "decay", "dL": "decay", "chi": "link"}
DX_MAX = 0.5
FULL = dict(M=16, n_lab=16, n_prog=4, R=6, act_grid=None, act_rb=2, h_n1=48, h_n2=24, h_best=6, h_rep=3, st_rep=2,
            v_M=8, v_R=4, v_params=V_PARAMS, c_M=16, c_R=6, c_values=None, seeds=SEEDS, boot=2000)
TINY = dict(M=4, n_lab=4, n_prog=2, R=3, act_grid=(2, 3, 5), act_rb=2, h_n1=4, h_n2=2, h_best=2, h_rep=2, st_rep=2,
            v_M=3, v_R=3, v_params=("F", "chi"), c_M=4, c_R=3, c_values={"a0": (0.03, 0.05), "rho": (0.02,), "DX": (0.2, 0.5)},
            seeds=(91, 92), boot=200)
SZ = FULL if SIZE == "full" else TINY
CLOCK = {"member_ticks": 0, "sim_s": 0.0, "t0": time.time(), "steady_ticks": 0, "steady_s": 0.0}


def progress(msg):
    os.makedirs(OUT, exist_ok=True)
    line = f"{time.strftime('%H:%M:%S', time.gmtime())} {msg}"
    print(line, flush=True)
    with open(os.path.join(OUT, "progress.txt"), "a") as f:
        f.write(line + "\n")


def jdump(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".tmp", "w") as f:
        json.dump(obj, f, indent=1)
    os.replace(path + ".tmp", path)


# ----------------------------------------------------------------------------- worlds and rollouts
class Sim:
    """One vw world with chunked 32-tick rollouts from given states (one compile per world and record length)."""

    def __init__(self, spec, world_seed):
        self.w = MW.MapWorld(spec, world_seed=world_seed)
        self.d = self.w.designer
        self.base = dict(self.w.params)
        self._mem = jax.jit(jax.vmap(self.w._start_mem))
        self._warm = False

    def set(self, **kw):
        self.w.params = dict(self.base, **{k: jnp.asarray(v, jnp.float64) for k, v in kw.items()})

    def form(self, M, seed, T=T0):
        t = time.time()
        ens = self.d.ensemble(M, seed=seed)
        ens, rec = self.d.rollout(ens, None, T=T, rec=("L1",))
        CLOCK["member_ticks"] += M * T
        CLOCK["sim_s"] += time.time() - t
        return {k: np.asarray(v) for k, v in ens.x.items()}, rec["L1"]

    def keys(self, n):
        return self.w._fresh_keys(n)

    def roll(self, xs, P, keys=None):
        """xs {field: (B, H, W)}, P (B, H, m) or None -> level 1 at ticks 0..H: (B, H + 1, d1)."""
        t = time.time()
        B = next(iter(xs.values())).shape[0]
        assert B * (H + 1) * 256 < 2 ** 31
        keys = self.w._fresh_keys(B) if keys is None else keys
        m = self.w.n_in
        out = []
        for s in range(0, B, CHUNK):
            idx = np.arange(s, min(s + CHUNK, B))
            ii = np.concatenate([idx, np.repeat(idx[-1:], CHUNK - len(idx))])
            x = {k: jnp.asarray(v[ii]) for k, v in xs.items()}
            A = np.zeros((H, CHUNK, m))
            if P is not None:
                A[:] = np.transpose(P[ii], (1, 0, 2))
            tc = time.time()
            c = Carry(x, self._mem(x), jnp.zeros((CHUNK,), jnp.int64), keys[ii])
            _, o = self.w._rollout(self.w.params, c, jnp.asarray(A), rec=("L1",))
            out.append(np.asarray(jnp.swapaxes(o["L1"], 0, 1))[:len(idx)])
            if self._warm:                                   # compiled: the steady rate (padded members are work too)
                CLOCK["steady_ticks"] += CHUNK * H
                CLOCK["steady_s"] += time.time() - tc
            self._warm = True
        CLOCK["member_ticks"] += B * H
        CLOCK["sim_s"] += time.time() - t
        return np.concatenate(out)


def make_worlds(hidden=None):
    cfg = SL.small_cfg(PX)
    spec_p, parts = SL.build(cfg)
    K = parts["tracker"].K
    pub = Sim(spec_p, 1)
    hid = None
    if hidden is not None:
        spec_h, _ = SL.build(cfg, "pro", hidden=hidden)
        hid = Sim(spec_h, 0)
    return cfg, K, pub, hid


# ----------------------------------------------------------------------------- programs
def draw_prog(rng):
    """gvh.one_program's draws, in its order: sign, duration, onset, offset distance, direction."""
    sign = rng.choice([-1.0, 1.0])
    dur = int(rng.choice([2, 5, 10, 20]))
    onset = int(rng.choice([0, 4, 8]))
    r = float(rng.choice([0.0, 8.0, 16.0]))
    ang = rng.uniform(0, 2 * np.pi)
    return float(sign), dur, onset, r, float(ang)


def aimed(cfg, tg, pr, nats=NATS):
    """gvh.one_program's pulse for given draws, aimed at the focus point of tg: (P (H, m), features (5,))."""
    sign, dur, onset, r, ang = pr
    cy, cx = (tg["cy"] + r * np.sin(ang)) % cfg.H, (tg["cx"] + r * np.cos(ang)) % cfg.W
    cen = MJ.bump_centres(cfg)
    dd = np.hypot((cen[:, 0] - cy + cfg.H / 2) % cfg.H - cfg.H / 2, (cen[:, 1] - cx + cfg.W / 2) % cfg.W - cfg.W / 2)
    sel = np.flatnonzero(dd <= 8.0)
    if sel.size < 2:
        sel = np.argsort(dd)[:2]
    amp = np.sqrt(2 * cfg.sigma_a ** 2 * nats / (dur * sel.size))
    P = np.zeros((H, cfg.m))
    P[onset:onset + dur][:, sel] = sign * amp
    return P, np.array([sign, sign * dur / 20.0, sign * onset / 8.0, sign * r / 16.0, sign * dur / 20.0 * r / 16.0])


def check_aimed(cfg):
    """aimed(draw_prog) is gvh.one_program draw for draw."""
    tg = {"cy": 20.3, "cx": 41.7}
    r1, r2 = np.random.default_rng(123), np.random.default_rng(123)
    for _ in range(20):
        P1, F1 = GV.one_program(cfg, tg, r1, NATS)
        P2, F2 = aimed(cfg, tg, draw_prog(r2))
        assert np.array_equal(P1, P2) and np.array_equal(F1, F2), "aimed() differs from gvh.one_program"


# ----------------------------------------------------------------------------- views of the cell list
def _cells(L1, K, size):
    T = L1[..., :K * 12].reshape(L1.shape[:-1] + (K, 12))
    pres = T[..., 0] > 0.5
    cx = (np.arctan2(T[..., 4], T[..., 3]) * size / (2 * np.pi)) % size
    cy = (np.arctan2(T[..., 6], T[..., 5]) * size / (2 * np.pi)) % size
    return pres, T[..., 1], T[..., 1] * T[..., 2], cy, cx


def _dist(cy, cx, py, px, size):
    return np.hypot((cy - py + size / 2) % size - size / 2, (cx - px + size / 2) % size - size / 2)


def anchors_of(L1_start, K, tg, size, rad=24.0, n_max=4):
    """The cells of the start state within rad px of the focus point, nearest first, at most n_max: (na, 2) (y, x)."""
    pres, _, _, cy, cx = _cells(L1_start, K, size)
    d = np.where(pres, _dist(cy, cx, tg["cy"], tg["cx"], size), 1e9)
    order = [k for k in np.argsort(d) if d[k] <= rad][:n_max]
    return np.array([[cy[k], cx[k]] for k in order]).reshape(-1, 2)


def cr_view(L1, K, anc, size, rad=12.0, n_max=4):
    """Cell-resolved list (DECLARED 2.2): per anchor the cell mass and catalyst mass of the cells within rad px of
    it and nearer to it than to any other anchor; missing anchors are zeros: (..., 2 * n_max)."""
    pres, mass, kmass, cy, cx = _cells(L1, K, size)
    out = np.zeros(L1.shape[:-1] + (n_max, 2))
    if len(anc):
        d = np.stack([_dist(cy, cx, a[0], a[1], size) for a in anc], -1)       # (..., K, na)
        near, dmin = d.argmin(-1), d.min(-1)
        okc = pres & (dmin <= rad)
        for a in range(len(anc)):
            w = okc & (near == a)
            out[..., a, 0] = (w * mass).sum(-1)
            out[..., a, 1] = (w * kmass).sum(-1)
    return out.reshape(L1.shape[:-1] + (2 * n_max,))


def ring_mass(L1, K, tg, size, r0=16.0, r1=32.0):
    pres, mass, _, cy, cx = _cells(L1, K, size)
    d = _dist(cy, cx, tg["cy"], tg["cx"], size)
    return ((pres & (d > r0) & (d <= r1)) * mass).sum(-1)


def n_and_area(L1, K, size):
    pres, mass, _, _, _ = _cells(L1, K, size)
    return pres.sum(-1), (pres * mass).sum(-1) / float(size * size)


def floor_scale(sc):
    pos = sc[sc > 1e-9]
    return np.maximum(sc, 0.1 * np.median(pos)) if pos.size else np.ones_like(sc)


def lab_scale(y_lab):
    """adv_act.py's Lab-only scale per tick and coordinate ((H + 1, d)): SD over the Lab outcomes, floored at a
    tenth of the coordinate's median SD over ticks 1..H; a coordinate that is zero in every Lab outcome takes
    the median of the positive entries."""
    s = np.maximum(y_lab.std(0), 0.1 * np.median(y_lab[:, 1:].std(0), 0))
    pos = s[s > 1e-12]
    return np.where(s > 1e-12, s, np.median(pos) if pos.size else 1.0)


def es_h(X, Y, sc, cols):
    """Fair energy score per item and horizon: X (N, m, T, d), Y (N, R, T, d), sc (nh, d), cols = tick per horizon."""
    return np.stack([energy_fair(X[:, :, c], Y[:, :, c], sc[j]) for j, c in enumerate(cols)], 1)


def es_loo_h(Y, sc, cols):
    return np.stack([energy_loo(Y[:, :, c], sc[j]) for j, c in enumerate(cols)], 1)


# ----------------------------------------------------------------------------- the designer's recipes (gvh.py)
def ridge_fit(X, y, a):
    return np.linalg.solve(X.T @ X + a * np.eye(X.shape[1]), X.T @ y)


def gains_fit(y, pl, p0l, F, s):
    """gvh.py's G2 and G3 on Lab arrays at the horizons: y (n, nh, d), pl / p0l (n, nh, d) public means with /
    without the program, F (n, 5), s (nh, d) fitting scale. Returns per-horizon gain g (nh,) and G3's b (nh, 4)."""
    dl, yl = (pl - p0l) / s, (y - p0l) / s
    n, nh, d = y.shape
    Z = np.concatenate([np.ones((n, 1)), np.abs(F[:, 1:4])], 1)
    g, b = np.zeros(nh), np.zeros((nh, 4))
    for j in range(nh):
        g[j] = float((dl[:, j] * yl[:, j]).sum() / max((dl[:, j] ** 2).sum(), 1e-12))
        A = (Z[:, None, :] * dl[:, j, :, None]).reshape(n * d, 4)
        b[j] = np.linalg.solve(A.T @ A + 0.3 * np.eye(4), A.T @ yl[:, j].reshape(-1))
    return g, b


def gains_apply(P, P0, F, g, b):
    """Forecast ensembles of G2 and G3: P, P0 (N, R, nh, d) public futures with / without the program."""
    dt_ = P.mean(1) - P0.mean(1)                                   # (N, nh, d)
    Z = np.concatenate([np.ones((len(F), 1)), np.abs(F[:, 1:4])], 1)
    G2 = P + ((g[None, :, None] - 1.0) * dt_)[:, None]
    G3 = P + (((Z @ b.T) - 1.0)[:, :, None] * dt_)[:, None]
    return G2, G3


def designer_recipes(y, PL, P0L, Fl, P, P0, Ft, s):
    """G1-G4 of gvh.py (fitting scale s from the Lab) and the leave-one-episode-out forecasts of G2 and G3."""
    n, nh, d = y.shape
    pl, p0l = PL.mean(1), P0L.mean(1)
    g, b = gains_fit(y, pl, p0l, Fl, s)
    G2, G3 = gains_apply(P, P0, Ft, g, b)
    Xl = np.concatenate([np.ones((n, 1)), Fl], 1)
    Xt = np.concatenate([np.ones((len(Ft), 1)), Ft], 1)
    res = (y - pl) / s
    G1, G4 = P.copy(), G3.copy()
    Zl = np.concatenate([np.ones((n, 1)), np.abs(Fl[:, 1:4])], 1)
    dl, yl = (pl - p0l) / s, (y - p0l) / s
    for j in range(nh):
        r3 = yl[:, j] - (Zl @ b[j])[:, None] * dl[:, j]
        for c in range(d):
            best = None
            for a in (0.03, 0.3, 3.0, 30.0):
                loo = 0.0
                for i in range(n):
                    k = np.arange(n) != i
                    loo += (Xl[i] @ ridge_fit(Xl[k], res[k, j, c], a) - res[i, j, c]) ** 2
                if best is None or loo < best[0]:
                    best = (loo, a)
            G1[:, :, j, c] += (Xt @ ridge_fit(Xl, res[:, j, c], best[1]))[:, None] * s[j, c]
            G4[:, :, j, c] += (Xt @ ridge_fit(Xl, r3[:, c], 3.0))[:, None] * s[j, c]
    loo2, loo3 = np.zeros_like(PL), np.zeros_like(PL)              # (n, R, nh, d): episode i forecast without it
    for i in range(n):
        k = np.arange(n) != i
        gi, bi = gains_fit(y[k], pl[k], p0l[k], Fl[k], s)
        a2, a3 = gains_apply(PL[i:i + 1], P0L[i:i + 1], Fl[i:i + 1], gi, bi)
        loo2[i], loo3[i] = a2[0], a3[0]
    return {"G1": G1, "G2": G2, "G3": G3, "G4": G4}, {"G2": loo2, "G3": loo3}, {"G2_gain": g.tolist(), "G3_b": b.tolist()}


def lab_loo_score(ens, y, s):
    """Mean over Lab episodes of the fair energy score of the single hidden future, Lab scale, summed over the
    exam horizons: ens (n, m, nh, d), y (n, nh, d), s (nh, d)."""
    return float(sum(energy_fair(ens[:, :, j], y[:, None, j], s[j]).mean() for j in EX))


# ----------------------------------------------------------------------------- the gate: one seed and arm
def load_ranges():
    p = os.path.join(OUT, "ranges.json")
    raw = open(p, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    want = open(os.path.join(OUT, "ranges.sha256")).read().split()[0]
    assert sha == want, "ranges.json does not match ranges.sha256"
    return json.loads(raw), sha


def draw_truth(seed, rg):
    rng = np.random.default_rng([20261111, seed])
    out = {}
    for k in ("rho", "DX", "a0"):
        lo, hi = rg["carrier_ranges"][k]["range"]
        out[k] = float(np.exp(rng.uniform(np.log(lo), np.log(hi))))
    return out


def h_box(rg):
    box = {"lam": (0.25, 1.0)}
    for k in ("rho", "DX", "a0"):
        lo, hi = rg["carrier_ranges"][k]["range"]
        box[k] = (lo / 1.5, min(hi * 1.5, DX_MAX) if k == "DX" else hi * 1.5)
    return box


def h_points(u, box):
    """Unit-cube points (n, 4) -> (lam, rho, DX, a0): lam uniform, the others log-uniform over the box."""
    out = np.zeros_like(u)
    out[:, 0] = box["lam"][0] + u[:, 0] * (box["lam"][1] - box["lam"][0])
    for j, k in enumerate(("rho", "DX", "a0")):
        out[:, j + 1] = np.exp(np.log(box[k][0]) + u[:, j + 1] * (np.log(box[k][1]) - np.log(box[k][0])))
    return out


def gate(seed, arm, smoke=False, truth=None):
    """One seed and arm. With `truth` given (the alignment check on a pilot seed) the hidden values are taken as
    given, no ranges file is read, and the run stops after the generic recipes."""
    from scipy.stats import qmc
    sz = dict(SZ)
    if smoke:                                               # full array shapes, short counts
        sz.update(act_grid=(2, 20), h_n1=2, h_n2=1, h_best=1)
    align = truth is not None
    if align:
        rg, sha = None, "none (alignment check)"
    else:
        rg, sha = load_ranges()
        truth = draw_truth(seed, rg)
    hidden = dict(lam=1.0, cat=1.0 if arm == "main" else 0.0, **truth)
    tag = f"s{seed}_{arm}"
    t_start = time.time()
    progress(f"gate {tag} start truth {json.dumps({k: round(v, 5) for k, v in truth.items()})} ranges {sha[:12]}")
    cfg, K, pub, hid = make_worlds(hidden)
    check_aimed(cfg)
    M, R, n_lab = sz["M"], sz["R"], sz["n_lab"]
    x, L1h = hid.form(M, (78, seed))
    Pcls, tgt = SC.programs(cfg, L1h[:, -1], K, NATS, np.random.default_rng([seed, 7]))
    ok = [i for i in range(M) if tgt[i]["mass_t0"] > 0]
    lab_m, test_m = [i for i in ok if i < M // 2], [i for i in ok if i >= M // 2]
    if len(lab_m) < 2 or len(test_m) < 2:
        raise SystemExit(f"gate {tag}: fewer than 2 Lab or test states with a focus cell ({lab_m}, {test_m})")
    anc = {i: anchors_of(L1h[i, -1], K, tgt[i], PX) for i in ok}
    rng = np.random.default_rng(seed)
    lab, test = [], []
    for j in range(n_lab):
        m_ = lab_m[j % len(lab_m)]
        pr = draw_prog(rng)
        lab.append((m_, pr) + aimed(cfg, tgt[m_], pr))
    for i in test_m:
        for _ in range(sz["n_prog"]):
            pr = draw_prog(rng)
            test.append((i, pr) + aimed(cfg, tgt[i], pr))
    Fl, Ft = np.stack([it[3] for it in lab]), np.stack([it[3] for it in test])
    tm = np.array([it[0] for it in test])
    VIEWS = ("focus", "cr")

    def views(L1, members):
        """L1 (n, reps, T, d1) -> {view: (n, reps, T, dv)} about each item's own focus point and anchors."""
        return {"focus": np.stack([SC.focus_view(L1[j], K, tgt[m_], PX) for j, m_ in enumerate(members)]),
                "cr": np.stack([cr_view(L1[j], K, anc[m_], PX) for j, m_ in enumerate(members)])}

    def run(sim, members, progs, reps, full, keys=None, focus_only=False):
        mem = np.repeat(np.asarray(members), reps)
        xs = {k: x[k][mem] for k in (x if full else MJ.FIELDS)}
        P = None if progs is None else np.repeat(np.stack(progs), reps, axis=0)
        L1 = sim.roll(xs, P, keys=keys).reshape(len(members), reps, H + 1, -1)
        if focus_only:
            return np.stack([SC.focus_view(L1[j], K, tgt[m_], PX) for j, m_ in enumerate(members)])
        return views(L1, members)

    lm, lp = [it[0] for it in lab], [it[2] for it in lab]
    tmem, tp = [it[0] for it in test], [it[2] for it in test]
    hs = list(HS4)
    y_lab = {v: a[:, 0] for v, a in run(hid, lm, lp, 1, True).items()}          # (n_lab, H + 1, dv): what the Lab shows
    pub_lab, pub0_lab = run(pub, lm, lp, R, False), run(pub, lm, None, R, False)
    Yt = run(hid, tmem, tp, R, True)
    pubt, pub0t = run(pub, tmem, tp, R, False), run(pub, tmem, None, R, False)
    progress(f"gate {tag} base runs done: lab states {lab_m} test states {test_m} items {len(test)} "
             f"rate {CLOCK['member_ticks'] / max(CLOCK['sim_s'], 1e-9):.0f} member-ticks/s")
    sc = {v: floor_scale(Yt[v][:, :, hs].reshape(-1, len(hs), Yt[v].shape[-1]).std(0)) for v in VIEWS}
    s_t = {v: lab_scale(y_lab[v]) for v in VIEWS}
    L = {v: {"pub": es_h(pubt[v], Yt[v], sc[v], hs), "pub0": es_h(pub0t[v], Yt[v], sc[v], hs), "O": es_loo_h(Yt[v], sc[v], hs)}
         for v in VIEWS}
    info = {v: {} for v in VIEWS}
    lab_loo = {v: {} for v in VIEWS}

    # --- the designer's recipes
    for v in VIEWS:
        ens, loo, fit = designer_recipes(y_lab[v][:, hs], pub_lab[v][:, :, hs], pub0_lab[v][:, :, hs], Fl,
                                         pubt[v][:, :, hs], pub0t[v][:, :, hs], Ft, s_t[v][hs])
        for k, e in ens.items():
            L[v][k] = es_h(e, Yt[v][:, :, hs], sc[v], range(len(hs)))
        for k, e in loo.items():
            lab_loo[v][k] = lab_loo_score(e, y_lab[v][:, hs], s_t[v][hs])
        info[v].update(fit)

    # --- A_act (adv_act.py): the public law under a filtered command, 39-point grid, 2 futures, common random numbers
    Wb = blur_matrix(cfg)
    grid = AA.GRID if sz["act_grid"] is None else [AA.GRID[g] for g in sz["act_grid"]]
    RB = sz["act_rb"]
    kl = pub.keys(len(lab) * RB)                                              # the same noise for every grid point
    kg = jnp.concatenate([kl] * len(grid))
    r = run(pub, lm * len(grid), [AA.filtered(P_, *g, Wb) for g in grid for P_ in lp], RB, False, keys=kg)
    act_test = {}
    for v in VIEWS:
        S = r[v].reshape((len(grid), len(lab)) + r[v].shape[1:])              # (G, n_lab, RB, H + 1, dv)
        sse = ((((S.mean(2) - y_lab[v][None]) / s_t[v])[:, :, 1:]) ** 2).sum((2, 3))    # (G, n_lab)
        gbest = int(np.argmin(sse.sum(1)))
        loo = np.stack([S[int(np.argmin(sse[:, np.arange(len(lab)) != i].sum(1))), i] for i in range(len(lab))])
        lab_loo[v]["A_act"] = lab_loo_score(loo[:, :, hs], y_lab[v][:, hs], s_t[v][hs])
        if gbest not in act_test:
            act_test[gbest] = run(pub, tmem, [AA.filtered(P_, *grid[gbest], Wb) for P_ in tp], R, False)
        L[v]["A_act"] = es_h(act_test[gbest][v], Yt[v], sc[v], hs)
        info[v]["A_act_fit_g0_g1_tau_blur"] = list(grid[gbest])
        info[v]["A_act_lab_sse"] = float(sse[gbest].sum())
        info[v]["A_act_lab_sse_public_law"] = float(sse[[i for i, g in enumerate(grid) if g == (1.0, 0.0, 0.0, 0)][0]].sum()) \
            if (1.0, 0.0, 0.0, 0) in grid else None
    progress(f"gate {tag} A_act done ({len(grid)} grid points)")

    # --- G*: the better generic recipe, picked on the Lab episodes (leave-one-episode-out)
    for v in VIEWS:
        pick = min(("G2", "G3", "A_act"), key=lambda k: lab_loo[v][k])
        L[v]["Gstar"] = L[v][pick].copy()
        info[v]["Gstar_pick"] = pick
        info[v]["lab_loo_score"] = lab_loo[v]

    if align:
        return {"L": L, "info": info, "test_state": tm, "lab_states": lab_m, "test_states": test_m}

    # --- H: told the form, fits (lam, rho, DX, a0) on a quasi-random design that does not contain the truth
    box = h_box(rg)
    kh = hid.keys(len(lab) * sz["h_rep"])
    u1 = qmc.Sobol(4, scramble=True, seed=1000 + seed).random(sz["h_n1"])

    def h_sse(pts):
        out = {v: [] for v in VIEWS}
        for p in pts:
            hid.set(lam=p[0], rho=p[1], DX=p[2], a0=p[3])
            r = run(hid, lm, lp, sz["h_rep"], True, keys=kh)
            for v in VIEWS:
                out[v].append(float(((((r[v].mean(1) - y_lab[v]) / s_t[v])[:, 1:]) ** 2).sum()))
        hid.set()
        return {v: np.array(a) for v, a in out.items()}
    p1 = h_points(u1, box)
    sse1 = h_sse(p1)
    h_test = {}
    for iv, v in enumerate(VIEWS):
        best = np.argsort(sse1[v])[:sz["h_best"]]
        lo, hi = u1[best].min(0), u1[best].max(0)
        w = 0.1 * (hi - lo)
        lo, hi = np.clip(lo - w, 0, 1), np.clip(hi + w, 0, 1)
        u2 = lo + np.random.default_rng([2000, seed, iv]).uniform(size=(sz["h_n2"], 4)) * (hi - lo)
        p2 = h_points(u2, box)
        sse2 = h_sse(p2)[v]
        pts, sse = np.concatenate([p1, p2]), np.concatenate([sse1[v], sse2])
        fit = pts[int(np.argmin(sse))]
        key = tuple(np.round(fit, 12))
        if key not in h_test:
            hid.set(lam=fit[0], rho=fit[1], DX=fit[2], a0=fit[3])
            h_test[key] = run(hid, tmem, tp, R, True)
            hid.set()
        L[v]["H"] = es_h(h_test[key][v], Yt[v], sc[v], hs)
        info[v]["H_fit_lam_rho_DX_a0"] = fit.tolist()
        info[v]["H_fit_stage"] = 1 if int(np.argmin(sse)) < len(p1) else 2
        info[v]["H_lab_sse_best"] = float(sse.min())
        info[v]["H_best5_sse_lam_rho_DX_a0"] = [[float(sse[i])] + pts[i].tolist() for i in np.argsort(sse)[:5]]
    info["H_box"] = {k: list(b) for k, b in box.items()}
    progress(f"gate {tag} H done ({sz['h_n1']} + {sz['h_n2']} points per view)")

    # --- the history-only stand-in (DECLARED 2.5), focus view, classes aimed / blind / none
    bp = [Pcls[i, 1] for i in test_m]
    Yb, Yn = run(hid, test_m, bp, R, True, focus_only=True), run(hid, test_m, None, R, True, focus_only=True)
    pb, pn = run(pub, test_m, bp, R, False, focus_only=True), run(pub, test_m, None, R, False, focus_only=True)
    scf = sc["focus"]
    feat = {}
    for j in ok:
        f0 = SC.focus_view(L1h[j, -1], K, tgt[j], PX)
        f8 = SC.focus_view(L1h[j, -1 - 8], K, tgt[j], PX)
        feat[j] = np.array([f0[0], f0[1], f0[0] - f8[0], ring_mass(L1h[j, -1], K, tgt[j], PX)])
    sr = sz["st_rep"]
    st_items = ([("aimed", i, pr) for (i, pr, _, _) in test] + [("blind", i, b_) for i, b_ in zip(test_m, bp)]
                + [("none", i, None) for i in test_m])
    Ytru = np.concatenate([Yt["focus"], Yb, Yn])[:, :, hs]                         # (n_items, R, nh, 2)
    Ppub = np.concatenate([pubt["focus"], pb, pn])[:, :, hs]
    train = {}
    for law, sim, full in (("public", pub, False), ("true", hid, True)):
        mem, progs, owner = [], [], []
        for q, (cls, i, a) in enumerate(st_items):
            if cls == "none":
                continue
            for j in ok:
                if j != i:
                    mem.append(j)
                    progs.append(aimed(cfg, tgt[j], a)[0] if cls == "aimed" else a)
                    owner.append(q)
        tr = run(sim, mem, progs, sr, full, focus_only=True)[:, :, hs]             # (rows, sr, nh, 2)
        none = run(sim, ok, None, sr, full, focus_only=True)[:, :, hs]             # (n_ok, sr, nh, 2)
        train[law] = (np.array(mem), np.array(owner), tr, none)

    def llr(law, q, cls, i):
        mem, owner, tr, none = train[law]
        if cls == "none":
            js, Ytr = [j for j in ok if j != i], none[[ok.index(j) for j in ok if j != i]]
        else:
            rows = np.flatnonzero(owner == q)
            js, Ytr = mem[rows].tolist(), tr[rows]
        X = np.repeat(np.stack([feat[j] for j in js]), sr, axis=0)
        mu, sd = X.mean(0), X.std(0) + 1e-9
        Z = (X - mu) / sd
        zi = (feat[i] - mu) / sd
        ens = np.zeros((len(Z), len(hs), 2))
        for jh in range(len(hs)):
            Y = Ytr[:, :, jh].reshape(-1, 2) / scf[jh]
            ym = Y.mean(0)
            W = np.linalg.solve(Z.T @ Z + 0.01 * len(Z) * np.eye(Z.shape[1]), Z.T @ (Y - ym))
            ens[:, jh] = (ym + zi @ W) + (Y - ym - Z @ W)
        return ens                                                                  # scaled units
    st = {k: np.zeros((len(st_items), len(hs))) for k in ("P0s", "Cs", "K", "pub", "O")}
    none_true = train["true"][3]
    for q, (cls, i, a) in enumerate(st_items):
        Yq = Ytru[q]
        for name, law in (("P0s", "public"), ("Cs", "true")):
            e = llr(law, q, cls, i)
            st[name][q] = [float(energy_fair(e[:, jh], Yq[:, jh] / scf[jh])) for jh in range(len(hs))]
        pool = none_true[[ok.index(j) for j in ok if j != i]].reshape(-1, len(hs), 2)
        st["K"][q] = [float(energy_fair(pool[:, jh], Yq[:, jh], scf[jh])) for jh in range(len(hs))]
        st["pub"][q] = [float(energy_fair(Ppub[q][:, jh], Yq[:, jh], scf[jh])) for jh in range(len(hs))]
        st["O"][q] = [float(energy_loo(Yq[:, jh], scf[jh])) for jh in range(len(hs))]
    progress(f"gate {tag} stand-in done ({len(st_items)} items)")

    gap = (L["focus"]["pub"] - L["focus"]["O"])[:, list(EX)].sum(1)
    heavy = max(sorted(set(tm.tolist())), key=lambda m_: gap[tm == m_].sum())
    meta = {PILOT: True, "seed": seed, "arm": arm, "smoke": smoke, "size": SIZE, "truth_pilot": hidden, "ranges_sha256": sha,
            "lab_states": lab_m, "test_states": test_m, "n_lab": len(lab), "n_test_items": len(test), "R": R,
            "horizons": hs, "heaviest_test_state": int(heavy),
            "heaviest_share_of_gap": float(gap[tm == heavy].sum() / gap.sum()),
            "focus_mass_at_start": {str(i): tgt[i]["mass_t0"] for i in ok}, "anchors_per_state": {str(i): int(len(anc[i])) for i in ok},
            "info": info, "member_ticks": CLOCK["member_ticks"], "sim_s": CLOCK["sim_s"], "wall_s": time.time() - t_start,
            "rate_member_ticks_per_s": CLOCK["member_ticks"] / max(CLOCK["sim_s"], 1e-9)}
    if smoke:
        return meta
    arrs = {f"L_{v}_{k}": a for v in VIEWS for k, a in L[v].items()}
    arrs.update({f"S_{k}": a for k, a in st.items()})
    os.makedirs(os.path.join(OUT, "gate"), exist_ok=True)
    tmp = os.path.join(OUT, "gate", f".{tag}.tmp.npz")                              # written whole, then renamed
    np.savez_compressed(tmp, test_state=tm, st_class=np.array([c for c, _, _ in st_items]),
                        st_state=np.array([i for _, i, _ in st_items]), F_test=Ft, **arrs)
    os.replace(tmp, os.path.join(OUT, "gate", f"{tag}.npz"))
    jdump(meta, os.path.join(OUT, "gate", f"{tag}.json"))
    progress(f"gate {tag} DONE wall {meta['wall_s']:.0f}s member-ticks {meta['member_ticks']} "
             f"pick {info['focus']['Gstar_pick']} heaviest {heavy} ({meta['heaviest_share_of_gap']:.2f})")
    return meta


# ----------------------------------------------------------------------------- the scans
def screen_items(sim_t, sim_q, x, tgt, ok, P, cls_idx, R, K, full_t):
    """Truths under sim_t and comparison futures under sim_q (projected state) for every (state, class):
    focus view at the horizons, (n_ok, C, R, nh, 2) each."""
    mem = np.repeat(np.repeat(np.asarray(ok), len(cls_idx)), R)
    progs = np.repeat(np.stack([P[i, c] for i in ok for c in cls_idx]), R, axis=0)
    out = []
    for sim, full in ((sim_t, full_t), (sim_q, False)):
        xs = {k: x[k][mem] for k in (x if full else MJ.FIELDS)}
        L1 = sim.roll(xs, progs).reshape(len(ok), len(cls_idx), R, H + 1, -1)
        out.append((np.stack([SC.focus_view(L1[j][:, :, list(HS4)], K, tgt[i], PX) for j, i in enumerate(ok)]), L1))
    return out[0][0], out[1][0], out[0][1]


def screen_gap(Yt, Yq, none_col=0):
    """screen.py's scores on the focus view: per (state, class, horizon) L(O), L(comparison), L(K); K = the other
    states' no-input truths. Scale: SD over all truths of the run, floored."""
    n, C, R, nh, d = Yt.shape
    sc = floor_scale(Yt.reshape(n * C * R, nh, d).std(0))
    esO, esQ, esK = np.zeros((n, C, nh)), np.zeros((n, C, nh)), np.zeros((n, C, nh))
    pool = Yt[:, none_col]
    for j in range(nh):
        esO[:, :, j] = energy_loo(Yt[:, :, :, j], sc[j])
        esQ[:, :, j] = energy_fair(Yq[:, :, :, j], Yt[:, :, :, j], sc[j])
        for i in range(n):
            others = np.delete(pool[:, :, j], i, axis=0).reshape((n - 1) * R, d)
            esK[i, :, j] = energy_fair(np.broadcast_to(others, (C,) + others.shape), Yt[i, :, :, j], sc[j])
    return esO, esQ, esK


def gap_of(esO, esQ, esK, cls, idx=None):
    idx = np.arange(esO.shape[0]) if idx is None else idx
    f = lambda a: a[idx][:, cls][:, :, list(EX)].sum(-1).mean()      # noqa: E731
    return float((f(esQ) - f(esO)) / (f(esK) - f(esO)))


def scan_c(part, nparts, smoke=False):
    vals = SCAN_C if SZ["c_values"] is None else SZ["c_values"]
    pts = [("centre", None)] + [(k, v) for k in ("a0", "rho", "DX") for v in vals[k] if v != CENTRE[k]]
    pts = pts[:1] if smoke else [p for j, p in enumerate(pts) if j % nparts == part]
    M, R = SZ["c_M"], SZ["c_R"]
    cfg, K, pub, hid = make_worlds(dict(lam=1.0, cat=1.0, **CENTRE))
    for name, val in pts:
        hv = dict(CENTRE) if name == "centre" else dict(CENTRE, **{name: val})
        tag = "centre" if name == "centre" else f"{name}_{val:g}"
        hid.set(**hv)
        x, L1h = hid.form(M, (77, 2))
        P, tgt = SC.programs(cfg, L1h[:, -1], K, NATS, np.random.default_rng([2, 77]))
        ok = [i for i in range(M) if tgt[i]["mass_t0"] > 0]
        res = {PILOT: True, "scan": "C", "point": tag, "hidden_pilot": dict(lam=1.0, cat=1.0, **hv), "members": M, "R": R,
               "members_with_focus_cell": len(ok), "classes": list(SC.CLASSES), "horizons_pooled": [8, 16, 32]}
        if len(ok) >= 3:
            Yt, Yq, _ = screen_items(hid, pub, x, tgt, ok, P, [0, 1, 2, 3], R, K, True)
            esO, esQ, esK = screen_gap(Yt, Yq)
            rb = np.random.default_rng(12345)
            boots = rb.integers(0, len(ok), size=(400, len(ok)))
            for cname, cls in (("none", [0]), ("blind", [1]), ("feed", [2]), ("starve", [3]), ("aimed", [2, 3])):
                res[f"gap_{cname}"] = gap_of(esO, esQ, esK, cls)
                res[f"gap_{cname}_se_members"] = float(np.std([gap_of(esO, esQ, esK, cls, b) for b in boots], ddof=1))
        hid.set()
        if smoke:
            return res
        jdump(res, os.path.join(OUT, "scan", f"C_{tag}.json"))
        progress(f"scanC {tag}: focus cells {len(ok)}/{M} gaps none {res.get('gap_none', float('nan')):+.3f} "
                 f"blind {res.get('gap_blind', float('nan')):+.3f} aimed {res.get('gap_aimed', float('nan')):+.3f}")


def v_tag(name, fac):
    """File tag of a scan V point. The index keeps names distinct on file systems that ignore case (DK / dK,
    DL / dL): the jobs r6-dialsb-001/002 ran commit 52ae6e4, which wrote V_<name>_x<factor>.json."""
    return f"{V_PARAMS.index(name):02d}_{name}_x{fac:g}"


def scan_v(part, nparts, smoke=False):
    pts = [("default", 1.0)] + [(p, f) for p in SZ["v_params"] for f in V_FACTORS]
    pts = pts[1:2] if smoke else [p for j, p in enumerate(pts) if j % nparts == part]
    M, R = SZ["v_M"], SZ["v_R"]
    cfg = SL.small_cfg(PX)
    spec_p, parts = SL.build(cfg)
    K = parts["tracker"].K
    tru, plug = Sim(spec_p, 0), Sim(spec_p, 1)
    need = math.ceil(0.75 * M)
    for name, fac in pts:
        tag = "default" if name == "default" else v_tag(name, fac)
        if name != "default":
            tru.set(**{name: MJ.THETA[name] * fac})
        x, L1h = tru.form(M, (79, 1))
        finite = [bool(all(np.isfinite(x[k][i]).all() for k in x)) for i in range(M)]
        P, tgt = SC.programs(cfg, np.nan_to_num(L1h[:, -1]), K, NATS, np.random.default_rng([1, 79]))
        n0, a0_ = n_and_area(np.nan_to_num(L1h[:, -1]), K, PX)
        cand = [i for i in range(M) if finite[i] and tgt[i]["mass_t0"] > 0]
        res = {PILOT: True, "scan": "V", "point": tag, "param": name, "factor": fac, "members": M, "R": R,
               "value": None if name == "default" else MJ.THETA[name] * fac, "cells_at_T0": n0.tolist(), "area_at_T0": a0_.tolist(),
               "finite": finite, "horizons_pooled": [8, 16, 32]}
        viable = []
        if len(cand) >= 2:
            Pm = np.stack([np.stack([P[i, 0], P[i, 2] if i % 2 == 0 else P[i, 3]]) for i in range(M)])   # none, aimed
            Yt, Yq, L1t = screen_items(tru, plug, x, tgt, cand, Pm, [0, 1], R, K, True)
            n32, a32 = n_and_area(np.nan_to_num(L1t[:, 0, :, -1]), K, PX)                               # (n_cand, R)
            fin32 = np.isfinite(L1t).all((1, 2, 3, 4))
            for j, i in enumerate(cand):
                good = (2 <= n0[i] <= K - 1 and 0.02 <= a0_[i] <= 0.5 and bool(fin32[j])
                        and bool(((n32[j] >= 2) & (n32[j] <= K - 1) & (a32[j] >= 0.02) & (a32[j] <= 0.5)).all()))
                if good:
                    viable.append(j)
            res["cells_at_32_no_input"] = n32.tolist()
            res["area_at_32_no_input"] = a32.tolist()
            if len(viable) >= 3:
                esO, esQ, esK = screen_gap(Yt[viable], Yq[viable])
                rb = np.random.default_rng(12345)
                boots = rb.integers(0, len(viable), size=(400, len(viable)))
                res["headroom"] = gap_of(esO, esQ, esK, [0, 1])
                res["headroom_se_members"] = float(np.std([gap_of(esO, esQ, esK, [0, 1], b) for b in boots], ddof=1))
                res["headroom_none"], res["headroom_aimed"] = gap_of(esO, esQ, esK, [0]), gap_of(esO, esQ, esK, [1])
        res["viable_members"] = len(viable)
        res["viable"] = bool(len(viable) >= need)
        tru.set()
        if smoke:
            return res
        jdump(res, os.path.join(OUT, "scan", f"V_{tag}.json"))
        progress(f"scanV {tag}: viable {len(viable)}/{M} headroom {res.get('headroom', float('nan')):+.3f}")


def ranges():
    """DECLARED.md 2.6 applied to the scan files; writes ranges.json and ranges.sha256."""
    sd = os.path.join(OUT, "scan")
    V = {}
    for p in SZ["v_params"]:
        V[p] = {f: json.load(open(os.path.join(sd, f"V_{v_tag(p, f)}.json"))) for f in V_FACTORS}
    table = {}
    for p, r in V.items():
        via = {f: r[f]["viable"] for f in V_FACTORS}
        row = {"family": FAMILY[p], "default": MJ.THETA[p], "viable": {str(f): via[f] for f in V_FACTORS},
               "headroom_by_factor": {str(f): r[f].get("headroom") for f in V_FACTORS}, "box_factors": None, "headroom": None}
        if via[0.9] and via[1.1]:
            lo, hi = (0.8 if via[0.8] else 0.9), (1.2 if via[1.2] else 1.1)
            h = [r[lo].get("headroom"), r[hi].get("headroom")]
            row["box_factors"] = [lo, hi]
            row["box"] = [MJ.THETA[p] * lo, MJ.THETA[p] * hi]
            row["headroom"] = None if None in h else min(h)
        row["eligible"] = bool(row["box_factors"] is not None and row["headroom"] is not None and row["headroom"] >= 0.02)
        table[p] = row
    best = {}
    for p, row in table.items():
        if row["eligible"] and (row["family"] not in best or row["headroom"] > table[best[row["family"]]]["headroom"]):
            best[row["family"]] = p
    chosen = sorted(best.values(), key=lambda p: -table[p]["headroom"])[:4]
    default = json.load(open(os.path.join(sd, "V_default.json")))
    vals = SCAN_C if SZ["c_values"] is None else SZ["c_values"]
    need = math.ceil(0.875 * SZ["c_M"])
    cr = {}
    for k in ("a0", "rho", "DX"):
        rows = []
        for v in sorted(set(vals[k]) | {CENTRE[k]}):
            r = json.load(open(os.path.join(sd, "C_centre.json" if v == CENTRE[k] else f"C_{k}_{v:g}.json")))
            silent = "gap_none" in r and r["gap_none"] <= 0.03 and r["gap_blind"] <= 0.05
            effective = "gap_aimed" in r and r["gap_aimed"] >= 0.10
            enough = r["members_with_focus_cell"] >= need
            rows.append({"value": v, "gap_none": r.get("gap_none"), "gap_blind": r.get("gap_blind"), "gap_aimed": r.get("gap_aimed"),
                         "se_none": r.get("gap_none_se_members"), "se_blind": r.get("gap_blind_se_members"),
                         "se_aimed": r.get("gap_aimed_se_members"), "members_with_focus_cell": r["members_with_focus_cell"],
                         "silent": bool(silent), "effective": bool(effective), "admissible": bool(silent and effective and enough)})
        ic = [j for j, r in enumerate(rows) if r["value"] == CENTRE[k]][0]
        if rows[ic]["admissible"]:
            lo = hi = ic
            while lo > 0 and rows[lo - 1]["admissible"]:
                lo -= 1
            while hi < len(rows) - 1 and rows[hi + 1]["admissible"]:
                hi += 1
            cr[k] = {"range": [rows[lo]["value"], rows[hi]["value"]], "scan_failed": False, "rows": rows}
        else:
            cr[k] = {"range": [CENTRE[k], CENTRE[k]], "scan_failed": True, "rows": rows}
    out = {PILOT: True, "what": "stage 0 of the membrane carrier: the hidden parameter set of the public law and the ranges of "
           "rho, D_X, a0, by the rules of DECLARED.md 2.6 (pilot values, never an exam)", "size": SIZE,
           "hidden_set": [{"param": p, "family": table[p]["family"], "box": table[p]["box"], "headroom": table[p]["headroom"]} for p in chosen],
           "carrier_ranges": cr, "pilot_centre": CENTRE, "scan_V": table,
           "scan_V_default_floor": {"headroom": default.get("headroom"), "se_members": default.get("headroom_se_members"),
                                    "viable_members": default["viable_members"]}}
    raw = json.dumps(out, indent=1, sort_keys=True).encode()
    with open(os.path.join(OUT, "ranges.json"), "wb") as f:
        f.write(raw)
    sha = hashlib.sha256(raw).hexdigest()
    with open(os.path.join(OUT, "ranges.sha256"), "w") as f:
        f.write(sha + "  ranges.json\n")
    progress(f"ranges.json sha256 {sha} hidden set {chosen} ranges "
             + json.dumps({k: v["range"] for k, v in cr.items()}) + " failed " + json.dumps({k: v["scan_failed"] for k, v in cr.items()}))


# ----------------------------------------------------------------------------- alignment with the pilots
def align():
    """The gate's code path on the designer's seed 5 at the pilot centre (a pilot seed, not a gate seed): the
    same start states, programs and noise keys as gvh.py, so L(pub), L(pub0), L(O) should equal the designer's
    file (exactly on the machine that made it; closely elsewhere, the dynamics being chaotic). G2 is fitted here
    with the Lab's scale (gvh.py: the test truths'), A_act with other noise keys than adv_act.py. Not fatal."""
    r = gate(5, "main", truth=dict(CENTRE))
    L = r["L"]["focus"]
    ref = json.load(open(os.path.join(DIALS, "sublevel_second", "results", "gvh_lam1_n16_s5_cat1_rho0.02_DX0.5_a00.03.json")))
    adv = json.load(open(os.path.join(DIALS, "crit_adversary", "results", "adv_s5.json")))
    gap = L["pub"] - L["O"]
    out = {PILOT: True, "what": "alignment of s0.py with sublevel_second/gvh.py and crit_adversary on the designer's seed 5 (pilot)",
           "size": SIZE, "L_mean_over_items_sum_of_4_horizons": {k: float(L[k].sum(1).mean()) for k in ("pub", "pub0", "O", "G2", "A_act")},
           "designer_file_L": {k: ref["L"][k] for k in ("pub", "pub0", "O", "G2")},
           "closed_by_horizon_4_8_16_32": {k: ((L["pub"] - L[k]).sum(0) / gap.sum(0)).tolist() for k in ("G2", "G3", "A_act", "Gstar")},
           "adversary_file_closed_by_horizon": {k: adv["closed_by_horizon"][k2] for k, k2 in (("G2", "G2"), ("A_act", "A_act_n16"))},
           "closed_h_8_16_32": {k: float((L["pub"] - L[k])[:, list(EX)].sum() / gap[:, list(EX)].sum()) for k in ("G2", "G3", "A_act", "Gstar")},
           "adversary_file_closed_h_8_16_32": {k: adv["closed_h_8_16_32"][k2] for k, k2 in (("G2", "G2"), ("A_act", "A_act_n16"))},
           "A_act_fit": r["info"]["focus"]["A_act_fit_g0_g1_tau_blur"], "adversary_A_act_fit": adv["recipes"]["A_act_n16"]["fit_g0_g1_tau_blur"],
           "Gstar_pick": r["info"]["focus"]["Gstar_pick"], "lab_loo_score": r["info"]["focus"]["lab_loo_score"],
           "lab_states": r["lab_states"], "test_states": r["test_states"], "designer_lab_test_states": [ref["lab_members"], ref["test_members"]]}
    out["max_abs_diff_L_pub_pub0_O"] = float(max(abs(out["L_mean_over_items_sum_of_4_horizons"][k] - ref["L"][k]) for k in ("pub", "pub0", "O")))
    jdump(out, os.path.join(OUT, "align.json"))
    progress(f"align: max |dL| over pub, pub0, O against the designer's file {out['max_abs_diff_L_pub_pub0_O']:.3g}; "
             f"G2 by horizon {np.round(out['closed_by_horizon_4_8_16_32']['G2'], 3).tolist()} (adversary {np.round(out['adversary_file_closed_by_horizon']['G2'], 3).tolist()}); "
             f"A_act {np.round(out['closed_by_horizon_4_8_16_32']['A_act'], 3).tolist()} (adversary {np.round(out['adversary_file_closed_by_horizon']['A_act'], 3).tolist()})")


# ----------------------------------------------------------------------------- presmoke
def presmoke():
    """Every stage once at full array shapes with short counts; the rate for job.sh's speed guard."""
    global OUT
    t = time.time()
    rv = scan_v(0, 1, smoke=True)
    rc = scan_c(0, 1, smoke=True)
    assert "gap_aimed" in rc and np.isfinite(rc["gap_aimed"]), rc
    sd = os.path.join(OUT, "presmoke")
    os.makedirs(sd, exist_ok=True)
    fake = {PILOT: True, "carrier_ranges": {k: {"range": [CENTRE[k] * 0.7, min(CENTRE[k] * 1.3, DX_MAX)]} for k in CENTRE}}
    raw = json.dumps(fake, indent=1, sort_keys=True).encode()
    keep, OUT = OUT, sd
    with open(os.path.join(sd, "ranges.json"), "wb") as f:
        f.write(raw)
    with open(os.path.join(sd, "ranges.sha256"), "w") as f:
        f.write(hashlib.sha256(raw).hexdigest() + "  ranges.json\n")
    meta = gate(30, "main", smoke=True)
    OUT = keep
    rate = CLOCK["member_ticks"] / max(CLOCK["sim_s"], 1e-9)
    res = {PILOT: True, "what": "presmoke: every stage once at full array shapes (seed 30, not a gate seed)", "size": SIZE,
           "wall_s": time.time() - t, "member_ticks": CLOCK["member_ticks"], "sim_s": CLOCK["sim_s"],
           "rate_member_ticks_per_s_incl_compiles": rate, "gate_rate_member_ticks_per_s": meta["rate_member_ticks_per_s"],
           "steady_rate_member_ticks_per_s": CLOCK["steady_ticks"] / max(CLOCK["steady_s"], 1e-9),
           "scanV_point": {k: rv.get(k) for k in ("point", "viable_members", "headroom")},
           "scanC_point": {k: rc.get(k) for k in ("point", "gap_none", "gap_blind", "gap_aimed")},
           "planned_member_ticks": planned_member_ticks()}
    jdump(res, os.path.join(OUT, "presmoke.json"))
    progress(f"presmoke ok wall {res['wall_s']:.0f}s rate {rate:.0f} member-ticks/s with compiles, "
             f"{res['steady_rate_member_ticks_per_s']:.0f} compiled; planned "
             f"{res['planned_member_ticks']['total']}")


def planned_member_ticks():
    z = SZ
    n_test = (z["M"] // 2) * z["n_prog"]
    n_ok = z["M"]
    grid = len(AA.GRID) if z["act_grid"] is None else len(z["act_grid"])
    g = (z["M"] * T0 + z["n_lab"] * H * (1 + 2 * z["R"]) + n_test * z["R"] * H * 3
         + grid * z["n_lab"] * z["act_rb"] * H + 2 * n_test * z["R"] * H
         + (z["h_n1"] + 2 * z["h_n2"]) * z["n_lab"] * z["h_rep"] * H + 2 * n_test * z["R"] * H
         + 4 * (z["M"] // 2) * z["R"] * H + 2 * ((n_test + z["M"] // 2) * (n_ok - 1) + n_ok) * z["st_rep"] * H)
    vals = SCAN_C if z["c_values"] is None else z["c_values"]
    nc = 1 + sum(1 for k in vals for v in vals[k] if v != CENTRE[k])
    c = nc * (z["c_M"] * T0 + z["c_M"] * 4 * z["c_R"] * H * 2)
    v = (1 + len(z["v_params"]) * len(V_FACTORS)) * (z["v_M"] * T0 + z["v_M"] * 2 * z["v_R"] * H * 2)
    return {"gate_per_seed_arm": int(g), "gate": int(g * len(z["seeds"]) * 2), "scan_C": int(c), "scan_V": int(v),
            "total": int(g * len(z["seeds"]) * 2 + c + v)}


# ----------------------------------------------------------------------------- analysis
def _t90(n):
    from scipy.stats import t as student
    return float(student.ppf(0.90, n - 1))


def contrast(per_seed):
    """Mean over seeds and its one-sided 90% bounds (Student's t): >= 0 means the condition holds."""
    a = np.asarray(per_seed, float)
    n = len(a)
    se = float(a.std(ddof=1) / np.sqrt(n)) if n > 1 else float("nan")
    q = _t90(n) if n > 1 else float("nan")
    lo, hi = float(a.mean() - q * se), float(a.mean() + q * se)
    return {"mean": float(a.mean()), "se": se, "lower90": lo, "upper90": hi,
            "reading": "holds clearly" if lo >= 0 else ("fails clearly" if hi < 0 else "close")}


def analyse():
    gd = os.path.join(OUT, "gate")
    seeds = list(SZ["seeds"])
    D = {}
    for arm in ARMS:
        for s in seeds:
            z = np.load(os.path.join(gd, f"s{s}_{arm}.npz"))
            D[(arm, s)] = ({k: z[k] for k in z.files}, json.load(open(os.path.join(gd, f"s{s}_{arm}.json"))))
    rb = np.random.default_rng(20261111)
    boots = rb.integers(0, len(seeds), size=(SZ["boot"], len(seeds)))
    pols = ("G2", "G3", "A_act", "Gstar", "G1", "G4", "H", "pub0")
    out = {PILOT: True, "what": "stage 0 of the membrane carrier (study B of ../PLAN.md): state given, 64 px; shares of the "
           "public-to-oracle gap closed, pooled over seeds; DECLARED.md is the specification", "size": SIZE, "seeds": seeds,
           "horizons": list(HS4), "exam_horizons": [8, 16, 32], "ranges_sha256": sorted({m["ranges_sha256"] for _, m in D.values()}),
           "truths_pilot": {str(s): D[("main", s)][1]["truth_pilot"] for s in seeds}, "arms": {}}

    def sums(arm, view, pol, cols, drop_heavy):
        """Per seed: (sum over items of L(pub) - L(pol), sum of L(pub) - L(O), contrast sum L(pol) - 0.3 L(pub) - 0.7 L(O))."""
        num, den, con = [], [], []
        for s in seeds:
            z, m = D[(arm, s)]
            keep = z["test_state"] != m["heaviest_test_state"] if drop_heavy else np.ones(len(z["test_state"]), bool)
            Lp, Lo, Lk = (z[f"L_{view}_{k}"][keep][:, cols].sum(1) for k in ("pub", "O", pol))
            num.append(float((Lp - Lk).sum()))
            den.append(float((Lp - Lo).sum()))
            con.append(float((Lk - 0.3 * Lp - 0.7 * Lo).sum()))
        return np.array(num), np.array(den), np.array(con)

    def share(arm, view, pol, cols, drop_heavy):
        num, den, con = sums(arm, view, pol, cols, drop_heavy)
        per = num / den
        loo = [float(np.delete(num, j).sum() / np.delete(den, j).sum()) for j in range(len(seeds))]
        bs = np.array([num[b].sum() / den[b].sum() for b in boots])
        dse = float(den.std(ddof=1) / np.sqrt(len(den))) if len(den) > 1 else float("nan")
        return {"closed": float(num.sum() / den.sum()), "per_seed": per.tolist(), "median_seed": float(np.median(per)),
                "leave_one_seed_out_range": [min(loo), max(loo)], "bootstrap_seeds_5_95": [float(np.quantile(bs, 0.05)), float(np.quantile(bs, 0.95))],
                "contrast_per_seed_at_0.7": con.tolist(), "gap_mean_per_seed": float(den.mean()), "gap_se_seeds": dse,
                "gap_readable": bool(den.mean() > 2 * dse) if len(den) > 1 else False}
    for arm in ARMS:
        A = {}
        for view in ("focus", "cr"):
            V = {}
            for drop, name in ((False, "all_start_states"), (True, "heaviest_left_out")):
                V[name] = {"pooled_8_16_32": {p: share(arm, view, p, list(EX), drop) for p in pols},
                           "by_horizon": {str(h): {p: share(arm, view, p, [j], drop)["closed"] for p in pols} for j, h in enumerate(HS4)},
                           "by_horizon_per_seed": {str(h): {p: share(arm, view, p, [j], drop)["per_seed"] for p in ("Gstar", "A_act", "G2", "G3", "H")}
                                                   for j, h in enumerate(HS4)}}
            V["Gstar_picks"] = {str(s): D[(arm, s)][1]["info"][view]["Gstar_pick"] for s in seeds}
            V["lab_loo_scores"] = {str(s): D[(arm, s)][1]["info"][view]["lab_loo_score"] for s in seeds}
            V["A_act_fits"] = {str(s): D[(arm, s)][1]["info"][view]["A_act_fit_g0_g1_tau_blur"] for s in seeds}
            V["H_fits_lam_rho_DX_a0"] = {str(s): D[(arm, s)][1]["info"][view]["H_fit_lam_rho_DX_a0"] for s in seeds}
            gap_h = np.array([[(D[(arm, s)][0][f"L_{view}_pub"] - D[(arm, s)][0][f"L_{view}_O"])[:, j].sum() for j in range(len(HS4))] for s in seeds])
            V["gap_share_by_horizon_8_16_32"] = (gap_h[:, 1:].sum(0) / gap_h[:, 1:].sum()).tolist()
            A[view] = V
        A["heaviest"] = {str(s): {"state": D[(arm, s)][1]["heaviest_test_state"], "share_of_gap": D[(arm, s)][1]["heaviest_share_of_gap"],
                                  "test_states": D[(arm, s)][1]["test_states"], "items": D[(arm, s)][1]["n_test_items"]} for s in seeds}
        # the stand-in (focus view, declared mix)
        W = {"none": 1 / 8, "blind": 1 / 8, "aimed": 3 / 4}

        def st_terms(cols, classes=("none", "blind", "aimed")):
            """Per seed, class-weighted means of L for P0s, Cs, K, pub, O over the given horizons."""
            rows = []
            for s in seeds:
                z, _ = D[(arm, s)]
                r = {}
                for k in ("P0s", "Cs", "K", "pub", "O"):
                    r[k] = sum(W[c] * z[f"S_{k}"][z["st_class"] == c][:, cols].sum(1).mean() for c in classes) / sum(W[c] for c in classes)
                rows.append(r)
            return {k: np.array([r[k] for r in rows]) for k in rows[0]}

        def st_block(cols, classes=("none", "blind", "aimed")):
            T = st_terms(cols, classes)
            f = lambda idx=None: {k: (v if idx is None else v[idx]).mean() for k, v in T.items()}      # noqa: E731

            def q(m):
                return {"share_s": float((m["P0s"] - m["Cs"]) / (m["K"] - m["Cs"])),
                        "state_given_gap": float((m["pub"] - m["O"]) / (m["K"] - m["O"])),
                        "kept": float((m["P0s"] - m["Cs"]) / (m["pub"] - m["O"])) if abs(m["pub"] - m["O"]) > 1e-12 else None,
                        "skill_Cs_of_oracle": float((m["K"] - m["Cs"]) / (m["K"] - m["O"])),
                        "skill_P0s_of_oracle": float((m["K"] - m["P0s"]) / (m["K"] - m["O"]))}
            r = q(f())
            per = (T["P0s"] - T["Cs"]) / (T["K"] - T["Cs"])
            loo = [q(f(np.delete(np.arange(len(seeds)), j)))["share_s"] for j in range(len(seeds))]
            bs = [q(f(b))["share_s"] for b in boots]
            r.update({"share_s_per_seed": per.tolist(), "share_s_median_seed": float(np.median(per)),
                      "share_s_leave_one_seed_out_range": [min(loo), max(loo)],
                      "share_s_bootstrap_seeds_5_95": [float(np.quantile(bs, 0.05)), float(np.quantile(bs, 0.95))],
                      "contrast_s_ge_0.10": contrast(T["P0s"] - 0.9 * T["Cs"] - 0.1 * T["K"])})
            return r
        A["stand_in"] = {"mix_8_16_32": st_block(list(EX)), "by_class_8_16_32": {c: st_block(list(EX), (c,)) for c in W},
                         "by_horizon_mix": {str(h): st_block([j]) for j, h in enumerate(HS4)}}
        out["arms"][arm] = A

    def cond(arm, pol, drop, at_most):
        num, den, con = sums(arm, "focus", pol, list(EX), drop)
        c = contrast(con if at_most else -con)
        sh = share(arm, "focus", pol, list(EX), drop)
        c.update({"closed": sh["closed"], "threshold": 0.7, "direction": "<=" if at_most else ">=",
                  "holds_at_point": bool(sh["closed"] <= 0.7 if at_most else sh["closed"] >= 0.7), "gap_readable": sh["gap_readable"]})
        if not sh["gap_readable"]:
            c["reading"] = "not readable (counts as close)"
        return c
    C = {"C1_main_Gstar_all_states_le_0.7": cond("main", "Gstar", False, True),
         "C2_main_Gstar_heaviest_left_out_le_0.7": cond("main", "Gstar", True, True),
         "C3_control_Gstar_ge_0.7": cond("control", "Gstar", False, False),
         "C4_main_H_ge_0.7": cond("main", "H", False, False)}
    st = out["arms"]["main"]["stand_in"]["mix_8_16_32"]
    C["C5_main_stand_in_share_ge_0.10"] = {"share_s": st["share_s"], "holds_at_point": bool(st["share_s"] >= 0.10),
                                           "reading": st["contrast_s_ge_0.10"]["reading"], "status": "depends on A (in no verdict here)"}
    four = [C[k] for k in list(C)[:4]]
    literal = "GO" if all(c["holds_at_point"] for c in four) else "NO-GO"
    if all(c["reading"] == "holds clearly" for c in four):
        verdict = "GO"
    elif any(c["reading"] == "fails clearly" for c in four):
        verdict = "NO-GO"
    else:
        verdict = "CLOSE CALL"
    out["conditions"] = C
    out["verdict"] = {"three_way": verdict, "plan_rule_at_point_estimates": literal,
                      "note": "C5 is reported and marked 'depends on A'; it enters neither reading"}
    out["cost"] = {"member_ticks_gate": int(sum(m["member_ticks"] for _, m in D.values())),
                   "sim_s_gate": float(sum(m["sim_s"] for _, m in D.values())), "wall_s_gate_sum": float(sum(m["wall_s"] for _, m in D.values()))}
    jdump(out, os.path.join(OUT, "analysis.json"))
    progress(f"analysis: verdict {verdict} (plan's point rule: {literal}) "
             + " ".join(f"{k.split('_')[0]}={c.get('closed', c.get('share_s')):.3f}[{c['reading']}]" for k, c in C.items()))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "presmoke":
        presmoke()
    elif cmd == "scanV":
        scan_v(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "scanC":
        scan_c(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "ranges":
        ranges()
    elif cmd == "gate":
        gate(int(sys.argv[2]), sys.argv[3])
    elif cmd == "analyse":
        analyse()
    elif cmd == "align":
        align()
    else:
        raise SystemExit(f"unknown command {cmd}")
