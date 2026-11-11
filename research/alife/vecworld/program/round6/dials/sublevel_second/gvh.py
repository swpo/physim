"""gvh -- generic repair against a told-the-form hypothesis, at tiny size and GIVEN THE STATE (candidate `pro`).

    python -B gvh.py [lam] [size] [n_lab] [seed] [key=value ...]      (defaults 1.0, 64, 16, 5; rho=, DX= set the truth)

DESIGN-STAGE CHECK of the design's main risk (a generic learner repairs the public simulator from the Lab budget).
PILOT values, never to be reused as an exam. It is NOT the exam: every policy here is handed the hidden state (the
public or hidden law is run from it), so history inference plays no part; what is compared is how each policy
turns n_lab Lab episodes into a correction of the public law's response to a program it has not seen.

World: `pro` at the given dial (truth rho 0.005, DX 0.2 unless overridden). 16 members form cells for 150 ticks.
Programs: one aimed pulse of 300 nats drawn from a broad family: sign +-, duration 2 / 5 / 10 / 20 ticks, onset
0 / 4 / 8, centre offset 0 / 8 / 16 px from the focus cell in a random direction.
Lab: n_lab episodes on members 0..7 (same start may recur; ONE hidden-world future each, as an agent would see).
Test: 32 items on members 8..15 (4 programs each), 6 replicate truths each. View: focus (cell mass and catalyst
mass within 16 px of the focus point) at h = 4, 8, 16, 32; fair energy score, coordinates scaled by their SD over
the test truths.
Policies (each an ensemble of 6 futures per test item):
    pub     the public law from the projected state (P0's law, given the state)
    pub0    the same, ignoring the program
    G1      pub + a ridge on the Lab residuals (Lab outcome - pub mean) with program features (sign, duration,
            onset, offset, duration x offset), one ridge per horizon and coordinate, strength by leave-one-out
    G2      pub with a per-horizon response gain fitted on the Lab episodes: pub0 mean + g_h (pub mean - pub0 mean)
    G3      G2 with the gain a linear function of (duration, onset, offset) per horizon
    H       told the form (carrier with unknown lam, rho, DX): least squares over a 3 x 3 x 3 grid of the hidden
            law's mean response on the same Lab episodes, then the hidden law at the fitted values
    O       the hidden law at the true values (leave-one-out over the truths)
Reported: L per policy, the share of the pub-to-O gap each closes, SE by bootstrap over the 8 test members, H's
fitted values. Writes results/gvh_<tag>.json.
"""
import json
import os
import sys
import time

import jax.numpy as jnp
import numpy as np

import sublevel as SL
from sublevel import MJ, MW
import screen as SC
from vw.scoring import energy_fair, energy_loo

T0, H, HS, R = 150, 32, (4, 8, 16, 32), 6
GRID = {"lam": (0.5, 0.75, 1.0), "rho": (0.005, 0.01, 0.02), "DX": (0.05, 0.2, 0.5)}


def one_program(cfg, tg, rng, nats):
    sign = rng.choice([-1.0, 1.0])
    dur = int(rng.choice([2, 5, 10, 20]))
    onset = int(rng.choice([0, 4, 8]))
    r = float(rng.choice([0.0, 8.0, 16.0]))
    ang = rng.uniform(0, 2 * np.pi)
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


def main():
    pos = [a for a in sys.argv[1:] if "=" not in a]
    kv = {k: float(v) for k, v in (a.split("=", 1) for a in sys.argv[1:] if "=" in a)}
    lam = float(pos[0]) if len(pos) > 0 else 1.0
    size = int(pos[1]) if len(pos) > 1 else 64
    n_lab = int(pos[2]) if len(pos) > 2 else 16
    seed = int(pos[3]) if len(pos) > 3 else 5
    nats, M = 300.0, 16
    truth = dict({"rho": 0.005, "DX": 0.2}, **kv, lam=lam)
    tag = f"lam{lam:g}_n{n_lab}_s{seed}" + "".join(f"_{k}{v:g}" for k, v in kv.items())
    cfg = SL.small_cfg(size)
    t_cpu = time.process_time()
    rng = np.random.default_rng(seed)
    spec_p, parts = SL.build(cfg)
    dp = MW.MapWorld(spec_p, world_seed=1).designer
    spec_h, _ = SL.build(cfg, "pro", hidden=truth)
    wh = MW.MapWorld(spec_h, world_seed=0)
    dh = wh.designer
    wg = MW.MapWorld(spec_h, world_seed=2)                  # H's simulator: the hidden law, values swapped per grid point
    dg = wg.designer
    K = parts["tracker"].K

    ens = dh.ensemble(M, seed=(78, seed))
    ens, rec0 = dh.rollout(ens, None, T=T0, rec=("L1",))
    x = {k: np.asarray(v) for k, v in ens.x.items()}
    _, tgt = SC.programs(cfg, rec0["L1"][:, -1], K, nats, np.random.default_rng(0))
    ok = [i for i in range(M) if tgt[i]["mass_t0"] > 0]
    lab_m = [i for i in ok if i < 8]
    test_m = [i for i in ok if i >= 8]
    lab = [(lab_m[j % len(lab_m)],) + one_program(cfg, tgt[lab_m[j % len(lab_m)]], rng, nats) for j in range(n_lab)]
    test = [(i,) + one_program(cfg, tgt[i], rng, nats) for i in test_m for _ in range(4)]

    def run(d, items, reps, full, zero=False):
        """focus view (n_items, reps, nh, 2) of `reps` futures per item under its program (or none)."""
        mem = np.repeat([it[0] for it in items], reps)
        xs = {k: x[k][mem] for k in (x if full else MJ.FIELDS)}
        P = np.repeat(np.stack([it[1] for it in items]), reps, axis=0)
        _, r = d.rollout(d.from_states(xs), None if zero else P, T=H, rec=("L1",))
        L1 = r["L1"][:, list(HS)].reshape(len(items), reps, len(HS), -1)
        return np.stack([SC.focus_view(L1[j], K, tgt[it[0]], size) for j, it in enumerate(items)])

    y_lab = run(dh, lab, 1, True)[:, 0]                     # (n_lab, nh, 2): what the Lab shows
    pub_lab, pub0_lab = run(dp, lab, R, False), run(dp, lab, R, False, zero=True)
    Yt = run(dh, test, R, True)                             # truths
    pub, pub0 = run(dp, test, R, False), run(dp, test, R, False, zero=True)
    sc = Yt.reshape(-1, len(HS), 2).std(0)
    sc = np.maximum(sc, 0.1 * np.median(sc[sc > 1e-9]))     # (nh, 2)
    F_lab, F_test = np.stack([it[2] for it in lab]), np.stack([it[2] for it in test])

    # G1: ridge on Lab residuals
    def ridge_fit(X, y, a):
        return np.linalg.solve(X.T @ X + a * np.eye(X.shape[1]), X.T @ y)
    Xl = np.concatenate([np.ones((n_lab, 1)), F_lab], 1)
    Xt = np.concatenate([np.ones((len(test), 1)), F_test], 1)
    res = (y_lab - pub_lab.mean(1)) / sc                    # (n_lab, nh, 2) scaled residuals
    G1 = pub.copy()
    g1_alpha = np.zeros((len(HS), 2))
    for j in range(len(HS)):
        for c in range(2):
            best = None
            for a in (0.03, 0.3, 3.0, 30.0):
                loo = 0.0
                for i in range(n_lab):
                    k = np.arange(n_lab) != i
                    loo += (Xl[i] @ ridge_fit(Xl[k], res[k, j, c], a) - res[i, j, c]) ** 2
                if best is None or loo < best[0]:
                    best = (loo, a)
            g1_alpha[j, c] = best[1]
            G1[:, :, j, c] += (Xt @ ridge_fit(Xl, res[:, j, c], best[1]))[:, None] * sc[j, c]

    # G2 / G3: response gains
    dl = (pub_lab.mean(1) - pub0_lab.mean(1)) / sc          # public response on the Lab episodes
    yl = (y_lab - pub0_lab.mean(1)) / sc
    dt_ = pub.mean(1) - pub0.mean(1)
    G2, G3 = pub.copy(), pub.copy()
    gains = []
    Zl = np.concatenate([np.ones((n_lab, 1)), np.abs(F_lab[:, 1:4])], 1)      # 1, duration, onset, offset
    Zt = np.concatenate([np.ones((len(test), 1)), np.abs(F_test[:, 1:4])], 1)
    for j in range(len(HS)):
        g = float((dl[:, j] * yl[:, j]).sum() / max((dl[:, j] ** 2).sum(), 1e-12))
        gains.append(g)
        G2[:, :, j] += ((g - 1.0) * dt_[:, j])[:, None]
        A = (Zl[:, None, :] * dl[:, j, :, None]).reshape(n_lab * 2, 4)        # y = (Z b) * d
        b = np.linalg.solve(A.T @ A + 0.3 * np.eye(4), A.T @ yl[:, j].reshape(-1))
        G3[:, :, j] += ((Zt @ b - 1.0)[:, None] * dt_[:, j])[:, None]

    # H: grid over the told form
    base = dict(wh.params)
    fits = []
    for la in GRID["lam"]:
        for rh in GRID["rho"]:
            for dx in GRID["DX"]:
                wg.params = dict(base, lam=jnp.asarray(la, jnp.float64), rho=jnp.asarray(rh, jnp.float64),
                                 DX=jnp.asarray(dx, jnp.float64))
                m = run(dg, lab, 3, True).mean(1)
                fits.append((float((((y_lab - m) / sc) ** 2).sum()), la, rh, dx))
    fits.sort()
    _, la, rh, dx = fits[0]
    wg.params = dict(base, lam=jnp.asarray(la, jnp.float64), rho=jnp.asarray(rh, jnp.float64), DX=jnp.asarray(dx, jnp.float64))
    Hh = run(dg, test, R, True)

    def es(X):
        return np.stack([energy_fair(X[:, :, j], Yt[:, :, j], sc[j]) for j in range(len(HS))], 1).sum(1)   # (n_items,)
    L = {"pub": es(pub), "pub0": es(pub0), "G1": es(G1), "G2": es(G2), "G3": es(G3), "H": es(Hh),
         "O": np.stack([energy_loo(Yt[:, :, j], sc[j]) for j in range(len(HS))], 1).sum(1)}
    tm = np.array([it[0] for it in test])
    rb = np.random.default_rng(1)

    def share(idx, k):
        return (L["pub"][idx].mean() - L[k][idx].mean()) / (L["pub"][idx].mean() - L["O"][idx].mean())
    out = {"PILOT_NEVER_REUSE_AS_EXAM": True, "what": "state-given check: generic repair of the public law against a told-the-form fit",
           "truth_pilot": {k: float(v) for k, v in truth.items()}, "size": size, "n_lab": n_lab, "seed": seed,
           "lab_members": lab_m, "test_members": test_m, "n_test_items": len(test), "R": R, "horizons": list(HS),
           "L": {k: float(v.mean()) for k, v in L.items()}, "share_of_pub_to_O_gap": {}, "G2_gain_by_horizon": gains,
           "G1_ridge_strength": g1_alpha.tolist(),
           "H_fit": {"lam": la, "rho": rh, "DX": dx, "grid": {k: list(v) for k, v in GRID.items()},
                     "best5_sse_lam_rho_DX": [list(f) for f in fits[:5]]}}
    all_idx = np.arange(len(test))
    for k in ("pub0", "G1", "G2", "G3", "H"):
        bs = []
        for _ in range(400):
            mm = rb.choice(test_m, size=len(test_m))
            bs.append(share(np.concatenate([np.flatnonzero(tm == m_) for m_ in mm]), k))
        out["share_of_pub_to_O_gap"][k] = {"value": float(share(all_idx, k)), "se_members": float(np.std(bs, ddof=1))}
    out["cpu_s_total"] = time.process_time() - t_cpu
    json.dump(out, open(os.path.join(SL.HERE, "results", f"gvh_{tag}.json"), "w"), indent=1)
    print(tag, "cpu_s", round(out["cpu_s_total"], 1), "L", {k: round(v, 3) for k, v in out["L"].items()})
    print("  share of pub-to-O gap:", {k: (round(v["value"], 3), round(v["se_members"], 3)) for k, v in out["share_of_pub_to_O_gap"].items()})
    print("  H fit", out["H_fit"]["lam"], out["H_fit"]["rho"], out["H_fit"]["DX"], "G2 gains", np.round(gains, 2).tolist())


if __name__ == "__main__":
    main()
