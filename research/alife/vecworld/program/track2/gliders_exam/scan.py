"""scan -- part (a): parameter headroom scan on the gliders wind world (sigma_w = 0.05).

One-at-a-time design: each candidate hidden parameter (gworld docstring) is set to the lower and the
upper edge of its declared prior box (others at default), plus a null setting (all default).
Per setting (keys shared by all settings: a paired design):
  1. 3 members from the declared initial law + 50 burn-in ticks under theta, then 30 free ticks:
     viability and level-1/2 statistics (objects, speed, mass, rg, fusions + fissions).
  2. 6 branch states x_P: each member at t = 0 (end of burn-in) and t = 30. Programs: no input for the
     t = 0 states (class a); a regional push (class d, 300 nats over 4 ticks, direction random per state,
     on the 4 x 4 blocks around the heaviest 2 x 2 group of the visible coarse view) for the t = 30 states.
  3. From each state: R = 4 truths under theta and m = 4 controls under theta_0 (prior mean = default),
     fresh noise, H = 8 ticks, the same program.
Headroom (the theta-plug-in deficit, EXAM 4.5): per horizon h and level,
    deficit_h = mean_states[ES_fair(controls, truths) - ES_loo(truths)] / D_h
with D_h = S_clim - S_oracle of the default world (refs_closure.json): the OES that a predictor with the
true state but theta set to the prior mean loses. The null setting gives its noise floor.
usage: python -B scan.py [names...]   (resumable; results/scan/<name>.npz, results/scan.json)
"""
import json
import os
import sys
import time

import jax
import jax.numpy as jnp
import numpy as np

import gworld as GW
from vw.scoring import energy_fair, energy_loo
from vw.world import make_key, member_keys

sys.path.insert(0, GW.ACT)
from viability import traj_stats  # noqa: E402

OUT = os.path.join(GW.RES, "scan")
os.makedirs(OUT, exist_ok=True)
JSON = os.path.join(GW.RES, "scan.json")

# declared prior boxes (lo, hi) for the scan; default = centre
PRIOR = {"lR": (0.85, 1.15), "dm": (-0.25, 0.25), "ls": (0.85, 1.15), "lh": (0.85, 1.15), "lA": (0.75, 1.25),
         "n": (1.5, 2.5), "gw": (0.7, 1.3),
         **{f"dm_{g}": (-0.25, 0.25) for g in GW.GROUPS}, **{f"ls_{g}": (0.85, 1.15) for g in GW.GROUPS}}
J, TW, NS_, R, M, HB = 3, 30, 6, 4, 4, 8
HS = [1, 2, 4, 8]
C_PUSH = 300.0
SIG = GW.SIGMA_W


def theta_of(name):
    if name == "null":
        return {}
    par, edge = name.rsplit("@", 1)
    lo, hi = PRIOR[par]
    return {par: lo if edge == "lo" else hi}


def to_params(th):
    """theta dict incl. per-group ls (ls_g) -> params."""
    th = dict(th)
    lsg = {k: th.pop(k) for k in list(th) if k.startswith("ls_")}
    p = GW.theta_to_params(th)
    if lsg:
        s = np.asarray(p["s"], float).copy()
        for k, v in lsg.items():
            s[GW.GROUPS[k[3:]]] *= v
        p["s"] = jnp.asarray(s)
    return p


def settings():
    out = ["null"]
    for k in PRIOR:
        out += [f"{k}@lo", f"{k}@hi"]
    return out


def run_setting(RN, name, refs):
    t0 = time.time()
    th = theta_of(name)
    p_th, p_0 = to_params(th), to_params({})
    Pj = GW.stack_params([p_th] * J)
    k_init = member_keys(make_key(5150, 1), J)
    sig = jnp.full((J,), SIG)
    A0, m0 = RN.init_burn(Pj, k_init, sig)
    y, ext, glob, A1, m1 = RN.run(Pj, A0, m0, GW.dyn_keys(k_init), jnp.zeros((J,), jnp.int64),
                                  jnp.zeros((J, TW, GW.NW)), sig)
    y, ext, glob = np.asarray(y), np.asarray(ext), np.asarray(glob)
    finite = bool(np.isfinite(y).all() and np.isfinite(np.asarray(A1)).all())
    stats = []
    for j in range(J):
        try:
            stats.append(traj_stats(y[j, :, GW.NC:], ext[j], glob[j]))
        except Exception as e:                      # e.g. no continuing slots
            stats.append({"error": repr(e)})
    pop = GW.population(y)                                                  # (J, TW+1, 3)
    Asum_max = float(np.asarray(A1).sum(1).max())
    # branch states: (member, t=0) class a; (member, t=TW) class d
    Ast = jnp.concatenate([A0, A1]); mst = jax.tree_util.tree_map(lambda a, b: jnp.concatenate([a, b]), m0, m1)
    yst = np.concatenate([y[:, 0], y[:, -1]])
    U = np.zeros((NS_, HB, GW.NW))
    rng = np.random.default_rng(99)
    angles = rng.uniform(0, 2 * np.pi, NS_)
    for s in range(J, NS_):
        U[s] = GW.regional_push(yst[s, :GW.NC], angles[s], C_PUSH, SIG, H=HB)
    nats = [GW.nats_of(U[s]) for s in range(NS_)]
    nb = R + M
    idx = np.repeat(np.arange(NS_), nb)
    Pb = GW.stack_params([p_th if (i % nb) < R else p_0 for i in range(NS_ * nb)])
    kb = member_keys(make_key(5150, 2), NS_ * nb)
    Ab = Ast[idx]
    mb = jax.tree_util.tree_map(lambda a: a[idx], mst)
    yb, extb, globb, _, _ = RN.run(Pb, Ab, mb, GW.dyn_keys(kb), jnp.zeros((NS_ * nb,), jnp.int64),
                                   jnp.asarray(U[idx]), jnp.full((NS_ * nb,), SIG))
    yb = np.asarray(yb).reshape(NS_, nb, HB + 1, -1)
    sc = np.load(os.path.join(GW.RES, "scales.npz"))
    res = {"name": name, "theta": th, "finite": finite, "A_sum_max_end": Asum_max, "stats": stats,
           "count_min": float(pop[..., 0].min()), "count_max": float(pop[..., 0].max()),
           "count_mean": float(pop[..., 0].mean()), "speed_mean": float(pop[..., 2].mean()),
           "push_nats": nats, "deficit": {}, "member_ticks": int(J * (GW.BURN + TW) + NS_ * nb * HB)}
    for lev, f, s_ in ((1, GW.coarse, sc["level1"]), (2, GW.population, sc["level2"])):
        for h in HS:
            Yt = f(yb[:, :R, h]); Xc = f(yb[:, R:, h])
            es_c = energy_fair(Xc, Yt, s_)
            es_o = energy_loo(Yt, s_)
            d = (es_c - es_o) / refs[f"level{lev}"][str(h)]["D"]
            res["deficit"][f"L{lev}h{h}"] = {"mean": float(d.mean()), "se": float(d.std(ddof=1) / np.sqrt(NS_)),
                                             "class_a": float(d[:J].mean()), "class_d": float(d[J:].mean()),
                                             "per_state": d.tolist()}
    res["seconds"] = time.time() - t0
    np.savez_compressed(os.path.join(OUT, f"{name}.npz"), y=y.astype(np.float32), ext=ext.astype(np.float32),
                        glob=glob.astype(np.float32), yb=yb.astype(np.float32), U=U.astype(np.float32))
    return res


def main():
    refs = json.load(open(os.path.join(GW.RES, "refs_closure.json")))
    names = sys.argv[1:] or settings()
    done = json.load(open(JSON)) if os.path.exists(JSON) else {"prior_boxes": PRIOR, "settings": {}}
    RN = GW.Runner()
    for nm in names:
        if nm in done["settings"]:
            continue
        r = run_setting(RN, nm, refs)
        done["settings"][nm] = r
        json.dump(done, open(JSON + ".tmp", "w"), indent=1)
        os.replace(JSON + ".tmp", JSON)
        dd = r["deficit"]
        print(f"{nm:10s} {r['seconds']:6.1f}s count {r['count_min']:.0f}-{r['count_max']:.0f} "
              f"speed {r['speed_mean']:.2f} | L1 h1..8 " + " ".join(f"{dd[f'L1h{h}']['mean']:+.3f}" for h in HS)
              + " | L2 h8 " + f"{dd['L2h8']['mean']:+.3f}", flush=True)


if __name__ == "__main__":
    main()
