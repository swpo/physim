"""w_cpu -- study foundrylong: CPU tests of the weight-inference policy W on a public pilot world (minutes).

    python -B w_cpu.py --world seed2027-46 --out results/w_cpu_<label>.json [--items 8] [--members 8]

Test 1 (state inference): the W predictor at the TRUE weights (members spun up under the true weights, held to the
  item's 17 observed frames, then simulated) against the oracle from the hidden state, persistence and climatology,
  at 8, 16 and 32 ticks, in skill units (K = 0, O = 1). If W(true) is low, a history of block views does not pin
  the fine state and W can do no better than that with perfect weights.
Test 2 (identifiability): the fit loss (one-tick forecasts of a nudged ensemble on Lab episodes) at the true weights,
  at neighbours of the truth (3%, 10%, 30%) and at other screened worlds. If the loss does not rank them, a
  gradient fit on it cannot find the weights.
Test 3 (fit, --skip t1,t2 to run it alone): Adam on the fit coordinates z (fl_w.to_z) from a 30% neighbour of the
  truth (scalars moved too) and from another screened world, on random windows of the Lab episodes with common
  random numbers per episode; the fit loss on all Lab episodes before and after (fixed keys), the distance to the
  truth in z, and the W predictor's skill at the fitted weights.
Everything is simulated here from public seeds: PILOT ONLY, never an exam.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ap = argparse.ArgumentParser()
ap.add_argument("--world", default="seed2027-46")
ap.add_argument("--out", required=True)
ap.add_argument("--items", type=int, default=8)
ap.add_argument("--members", type=int, default=8)
ap.add_argument("--futures", type=int, default=6)
ap.add_argument("--clim", type=int, default=16)
ap.add_argument("--lab", type=int, default=8)
ap.add_argument("--lab-members", type=int, default=4)
ap.add_argument("--burn", type=int, default=300)
ap.add_argument("--others", default="seed2027-581,seed2027-2928,seed2026-198")
ap.add_argument("--skip", default="")
ap.add_argument("--fit-steps", type=int, default=40)
ap.add_argument("--fit-eb", type=int, default=4)
ap.add_argument("--fit-m", type=int, default=2)
ap.add_argument("--fit-T", type=int, default=24)
ap.add_argument("--fit-lr", type=float, default=0.03)
ap.add_argument("--fit-respin", type=int, default=20)
a = ap.parse_args()

import fl_w as W  # noqa: E402

LL, FL = W.LL, W.FL
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from jax import lax  # noqa: E402

import tnca as TN  # noqa: E402
from vw.core import Noise  # noqa: E402
from vw.scoring import energy_fair, energy_loo  # noqa: E402

P, H, QS = LL.P, LL.H, list(LL.HS)
T0 = time.time()


def th_of(label):
    s, i = label[4:].split("-")
    return {k: jnp.asarray(v) for k, v in TN.draw_theta(int(s), int(i)).items()}


def log(m):
    print(f"[{time.time() - T0:6.0f}s] {m}", flush=True)


TH = th_of(a.world)
key = jax.random.key(20261111)
kk = lambda *i: jax.vmap(lambda j: jax.random.fold_in(jax.random.fold_in(key, i[0]), j))(jnp.arange(i[1]))
spin = jax.jit(W.spin, static_argnums=2)
out = dict(PILOT_NEVER_REUSE_AS_EXAM=True, world=a.world, config=vars(a), queries=QS)

# ---- truth: items (history, futures under a mix program), climatology runs, Lab episodes (designer side)
run_free = jax.jit(lambda th, x, keys, t0, T: W.forecast(th, x, jnp.zeros((T, W.NW)), keys, t0), static_argnums=4)


@jax.jit
def run_prog(th, x, U, keys, t0):
    """x (n, ...), U (n, T, NW), keys (n,) -> (n, T, NOBS) and final states."""
    def one(xx, u, k):
        def body(x, inp):
            t, ut = inp
            xn = TN.tick(th, x, Noise(k, t), ut, TN.FAM)
            return xn, W.view(xn)
        return lax.scan(body, xx, (t0 + jnp.arange(u.shape[0]), u))
    return jax.vmap(one)(x, U, keys)


def episodes(th, n, tag, R=1):
    """n exam-shaped episodes from the world's own burn-in: histories (n, P + 1, NOBS), programs (n, H, NW),
    futures (n, R, H, NOBS) under the program with R fresh noise streams."""
    x0 = spin(th, kk(tag, n), a.burn)
    y0 = np.asarray(jax.vmap(W.view)(x0))
    xP, Yh = run_prog(th, x0, jnp.zeros((n, P, W.NW)), kk(tag + 1, n), 0)
    hist = np.concatenate([y0[:, None], np.asarray(Yh)], 1)
    rng = np.random.default_rng([tag, 5])
    U = np.stack([FL.prog_dense("abcd"[i % 4], rng, hist[i, -1]) for i in range(n)])
    xr = jnp.repeat(xP, R, 0)
    _, Yf = run_prog(th, xr, jnp.asarray(np.repeat(U, R, 0)), kk(tag + 2, n * R), P)
    return hist, U, np.asarray(Yf).reshape(n, R, H, -1)


hist, Ptest, fut = episodes(TH, a.items, 100, a.futures)
log(f"items: {hist.shape} futures {fut.shape}")
_, _, clim = episodes(TH, a.clim, 200, 1)
labh, labU, labf = episodes(TH, a.lab, 300, 1)
labY = np.concatenate([labh, labf[:, 0]], 1)                                        # (E, P + H + 1, NOBS)
labUU = np.concatenate([np.zeros((a.lab, P, W.NW)), labU], 1)
log(f"climatology {clim.shape}, Lab {labY.shape}")
qi = np.array(QS) - 1
truth = fut[:, :, qi]                                                               # (n, R, 3, NOBS)
pool = clim[:, 0][:, qi]                                                            # (n_clim, 3, NOBS)
sd = pool.reshape(-1, 3, W.G * W.G).std((0, 2))
mu = pool.reshape(-1, 3, W.G * W.G).mean((0, 2))
scale = np.repeat(np.maximum(sd, 1e-9 * np.abs(mu)), W.G * W.G)                     # per channel, the exam's scaling


def score(S):
    """S (n, m, 3, NOBS) -> per query mean fair energy score over items."""
    return [float(np.mean(energy_fair(S[:, :, j], truth[:, :, j], scale))) for j in range(3)]


L = dict(O=[float(np.mean(energy_loo(truth[:, :, j], scale, True))) for j in range(3)],
         K=score(np.broadcast_to(pool[None], (a.items,) + pool.shape)),
         Kp=score(np.repeat(hist[:, None, None, -1], 2, 1).repeat(3, 2)))
skill = lambda b: [round((L["K"][j] - L[b][j]) / (L["K"][j] - L["O"][j]), 3) for j in range(3)]
out["L"] = L

# ---- Test 1: the W predictor at the true weights and at other weights
pred = jax.jit(lambda th, x, hist, Pt, keys: jax.vmap(lambda h, p, k: W.predict(th, x, h, p, k, QS))(hist, Pt, keys))


def w_predict(th, tag):
    x = spin(th, kk(tag, a.members), a.burn)
    keys = jax.vmap(lambda i: kk(tag + 1 + i, a.members))(jnp.arange(a.items))
    return np.asarray(pred(th, x, jnp.asarray(hist), jnp.asarray(Ptest), keys))


others = [o for o in a.others.split(",") if o]
if "t1" not in a.skip:
    L["W_true"] = score(w_predict(TH, 400))
    log(f"W(true) skill {skill('W_true')}  persistence {skill('Kp')}")
    L["W_prior"] = score(w_predict(th_of(others[0]), 500))
    log(f"W(prior {others[0]}) skill {skill('W_prior')}")
    for e_ in (0.1, 0.3):
        thn = {k: jnp.asarray(v) for k, v in TN.perturb_theta({k: np.asarray(v) for k, v in TH.items()}, 909, 0, e_, hyper=False).items()}
        L[f"W_eps{e_}"] = score(w_predict(thn, 600 + int(100 * e_)))
        log(f"W(eps {e_}) skill {skill(f'W_eps{e_}')}")
    out["skill"] = {b: skill(b) for b in L if b not in ("K", "O")}

# ---- Test 2: the fit loss at the truth, at its neighbours and at other screened worlds
if "t2" not in a.skip:
    lsd = labY.reshape(-1, 3, W.G * W.G).std((0, 2))
    lscale = jnp.asarray(np.repeat(np.maximum(lsd, 1e-12), W.G * W.G))
    loss = jax.jit(W.lab_loss)
    Mm = a.lab_members

    def fit_loss(th, tag):
        pool_ = spin(th, kk(tag, a.members), a.burn)                               # a small pool, reused across episodes
        x = pool_[(jnp.arange(a.lab * Mm) % a.members)].reshape((a.lab, Mm) + (W.C, TN.FAM.H, TN.FAM.W))
        keys = jax.vmap(lambda i: kk(tag + 1 + i, Mm))(jnp.arange(a.lab))
        return float(loss(th, x, jnp.asarray(labY), jnp.asarray(labUU), keys, lscale))
    rows = {}
    rows["true"] = fit_loss(TH, 700)
    rows["true_again"] = fit_loss(TH, 750)
    log(f"fit loss at the truth {rows['true']:.5f} (another ensemble {rows['true_again']:.5f})")
    for e_ in (0.03, 0.1, 0.3):
        thn = {k: jnp.asarray(v) for k, v in TN.perturb_theta({k: np.asarray(v) for k, v in TH.items()}, 909, 0, e_, hyper=False).items()}
        rows[f"eps{e_}"] = fit_loss(thn, 800 + int(100 * e_))
        log(f"fit loss at eps {e_}: {rows[f'eps{e_}']:.5f}")
    for o in others:
        rows[o] = fit_loss(th_of(o), 900 + len(rows))
        log(f"fit loss at {o}: {rows[o]:.5f}")
    out["fit_loss"] = rows
# ---- Test 3: the fit
if "t3" not in a.skip:
    lsd = labY.reshape(-1, 3, W.G * W.G).std((0, 2))
    lscale = jnp.asarray(np.repeat(np.maximum(lsd, 1e-12), W.G * W.G))
    vg = W.fit_step_fn(remat=True)
    lossf = jax.jit(W.lab_loss)
    dens = W.dens_of(labY)
    zt = W.to_z(TH)
    Mm, fm, eb, T = a.lab_members, a.fit_m, a.fit_eb, a.fit_T
    TT = labY.shape[1] - 1

    def pool_at(z, tag):
        return spin(W.from_z(z, dens), kk(tag, a.members), a.burn)

    def eval_loss(z):                                    # common random numbers: the same pool and noise keys for every z
        p_ = pool_at(z, 5000)
        x = p_[(jnp.arange(a.lab * Mm) % a.members)].reshape((a.lab, Mm) + p_.shape[1:])
        keys = jax.vmap(lambda i: kk(5100 + i, Mm))(jnp.arange(a.lab))
        return float(lossf(W.from_z(z, dens), x, jnp.asarray(labY), jnp.asarray(labUU), keys, lscale))

    def dist(z):
        d = np.asarray(z - zt)
        return dict(net_rms=float(np.sqrt(np.mean(d[:W.NZ_NET] ** 2))), box=[round(float(v), 3) for v in d[W.NZ_NET:]])
    starts = {"eps0.3_hyper": W.to_z({k: jnp.asarray(v) for k, v in TN.perturb_theta(
        {k: np.asarray(v) for k, v in TH.items()}, 909, 1, 0.3, hyper=True).items()}), others[0]: W.to_z(th_of(others[0]))}
    fits = {}
    for name, z0 in starts.items():
        z, st = z0, (jnp.zeros_like(z0), jnp.zeros_like(z0), 0)
        rng = np.random.default_rng(11)
        rec = dict(loss_before=eval_loss(z0), dist_before=dist(z0), trace=[])
        log(f"fit {name}: loss {rec['loss_before']:.4f}, dist {rec['dist_before']['net_rms']:.3f}")
        p_ = pool_at(z, 6000)
        for it in range(a.fit_steps):
            if it and it % a.fit_respin == 0:
                p_ = pool_at(z, 6000 + it)
            ei = rng.choice(a.lab, eb, replace=False)
            t0 = rng.integers(0, TT - T + 1, eb)
            Ys = jnp.asarray(np.stack([labY[e, t:t + T + 1] for e, t in zip(ei, t0)]))
            Us = jnp.asarray(np.stack([labUU[e, t:t + T] for e, t in zip(ei, t0)]))
            X0 = p_[jnp.asarray(rng.choice(a.members, eb * fm))].reshape((eb, fm) + p_.shape[1:])
            keys = jax.vmap(lambda e: kk(7000 + e, fm))(jnp.asarray(ei))
            l, g = vg(z, dens, X0, Ys, Us, keys, lscale)
            z, st = W.adam(z, g, st, a.fit_lr)
            rec["trace"].append(round(float(l), 5))
            if it % 10 == 9:
                log(f"  step {it + 1}: window loss {float(l):.4f}, net dist {dist(z)['net_rms']:.3f}")
        rec.update(loss_after=eval_loss(z), dist_after=dist(z))
        L[f"W_fit_{name}"] = score(w_predict(W.from_z(z, dens), 1400))
        rec["skill_after"] = skill(f"W_fit_{name}")
        log(f"fit {name}: loss {rec['loss_before']:.4f} -> {rec['loss_after']:.4f}; net dist {rec['dist_before']['net_rms']:.3f} -> "
            f"{rec['dist_after']['net_rms']:.3f}; skill {rec['skill_after']}")
        fits[name] = rec
    out["fit"] = fits
    out["fit_loss_truth"] = eval_loss(zt)
    log(f"fit loss at the truth, same keys: {out['fit_loss_truth']:.4f}")
out["seconds"] = time.time() - T0
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
with open(a.out, "w") as f:
    json.dump(out, f, indent=1)
print("wrote", a.out)
