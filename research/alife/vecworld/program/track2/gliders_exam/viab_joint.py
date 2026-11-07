"""viab_joint -- viability of the chosen 4-parameter prior box at its 16 corners and its centre.

One member per corner (and 1 at the centre), declared initial law + 50 burn-in ticks + 100 free ticks
under the corner's theta with background wind sigma_w = 0.05 and no input; keys shared by all members
(a paired design). Viability rule (EXAM 6.3, broadened): finite field, never fewer than 2 tracked bodies,
mean count in [4, 12], median speed of continuing bodies >= 0.5 px per tick, max A_sum < 10, and at most
25% of ticks with all K = 12 tracker slots full (beyond that the objects view drops bodies).
Output: results/viab_joint.json (+ viab_joint.npz, float32 population records).
"""
import itertools
import json
import os
import sys
import time

import jax.numpy as jnp
import numpy as np

import gworld as GW
from vw.world import make_key, member_keys

sys.path.insert(0, GW.ACT)
from viability import traj_stats  # noqa: E402

T = 100


def viability(names, pts, k, RN=None):
    """Run each theta in pts (one member each, keys k (B,)) through init + burn-in + T ticks, no input;
    return (rows, pop) with the rule of the module docstring. Public code: the agent can rerun it."""
    B = len(pts)
    RN = RN or GW.Runner()
    P = GW.stack_params([GW.theta_to_params(dict(zip(names, map(float, v)))) for v in pts])
    sig = jnp.full((B,), GW.SIGMA_W)
    A, m = RN.init_burn(P, k, sig)
    y, ext, glob, A1, _ = RN.run(P, A, m, GW.dyn_keys(k), jnp.zeros((B,), jnp.int64), jnp.zeros((B, T, GW.NW)), sig)
    y, ext, glob, A1 = (np.asarray(a) for a in (y, ext, glob, A1))
    pop = GW.population(y)
    rows = []
    for b in range(B):
        try:
            st = traj_stats(y[b, :, GW.NC:], ext[b], glob[b])
        except Exception:                                   # no continuing bodies
            st = {k: float("nan") for k in ("speed_median", "mass_median", "rg_median", "fusions_per100",
                                            "fissions_per100")}
        c = pop[b, :, 0]
        r = {"theta": dict(zip(names, map(float, pts[b]))),
             "finite": bool(np.isfinite(y[b]).all() and np.isfinite(A1[b]).all()),
             "count_min": float(c.min()), "count_max": float(c.max()), "count_mean": float(c.mean()),
             "speed_median": st["speed_median"], "mass_median": st["mass_median"], "rg_median": st["rg_median"],
             "fusions_per100": st["fusions_per100"], "fissions_per100": st["fissions_per100"],
             "A_sum_max_end": float(A1[b].sum(0).max()),
             "frac_ticks_at_slot_cap": float((c >= GW.K).mean()),
             "tracked_mass_frac_median": float(np.median(pop[b, :, 1]) / A1[b].sum())}
        r["viable"] = bool(r["finite"] and r["count_min"] >= 2 and 4 <= r["count_mean"] <= 12
                           and r["speed_median"] >= 0.5 and r["A_sum_max_end"] < 10
                           and r["frac_ticks_at_slot_cap"] <= 0.25)
        rows.append(r)
    return rows, pop


def main():
    pr = json.load(open(os.path.join(GW.RES, "prior.json")))
    names, lo, hi = pr["names"], np.array(pr["lo"]), np.array(pr["hi"])
    corners = [np.where(np.array(c) == 1, hi, lo) for c in itertools.product((0, 1), repeat=len(names))]
    pts = corners + [(lo + hi) / 2]
    B = len(pts)
    t0 = time.time()
    k = member_keys(make_key(6161, 1), 1)[np.zeros(B, int)]
    rows, pop = viability(names, pts, k)
    for b, r in enumerate(rows):
        r["corner"] = b < len(corners)
        print(b, r["viable"], {k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items() if k != "theta"},
              flush=True)
    out = {"names": names, "lo": lo.tolist(), "hi": hi.tolist(), "T_after_burn_in": T, "members": B,
           "member_ticks": B * (GW.BURN + T), "seconds": time.time() - t0, "points": rows,
           "all_viable": all(r["viable"] for r in rows)}
    json.dump(out, open(os.path.join(GW.RES, "viab_joint.json"), "w"), indent=1)
    np.savez_compressed(os.path.join(GW.RES, "viab_joint.npz"), pop=pop.astype(np.float32))


if __name__ == "__main__":
    main()
