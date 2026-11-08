"""bcombine -- pool the certified halves, seed stability, window statistics -> $B4_OUT/combined.json (study `bias`).

usage: python -B bcombine.py
Per Phi (a config and seed, or a hand design): the two certification halves (Phi fitted on B certified on A, and
vice versa) pooled with lphi.combine (closure ceilings for the fixed families G, L = local ridge, GL = G + local
ridge; bootstrap SE over trajectories; Gaussian log-det measures averaged over halves); non-triviality and
agreement averaged over halves. Per config: seed means, seed differences of the ceilings, and the latent agreement
between the two seeds on the same certification half (cross-validated ridge R^2, both directions). Linear windows
(L arm and the N linear part, c <= 2): cosine to the block-mass window and to the tent, share inside the block,
channel balance (raw units).
"""
import glob
import json
import os
import time

import numpy as np

import b4

CL, LP = b4.setup_paths(closure=True)
import bcert  # noqa: E402  (cv_r2)
import bwin as BW  # noqa: E402

CERT = b4.work_dir("cert")
LAT = b4.work_dir("lat")
OUT = b4.out_dir()
T0 = time.time()


def log(*a):
    b4.progress(f"[bcombine {time.time() - T0:7.1f}s] " + " ".join(str(x) for x in a))


def load_half(stem):
    d = np.load(f"{CERT}/{stem}.npz")
    js = json.load(open(f"{CERT}/{stem}.json"))
    names = [str(n) for n in d["names"]]
    ld = {k: (np.asarray(v, float) if k not in ("bestG", "q") else v) for k, v in js["ld"].items()}
    return {"err": {n: d["err"][i] for i, n in enumerate(names)}, "orac": d["orac"], "item_j": d["item_j"],
            "ld": ld, "q": js["q"]}, js


def pooled(phi):
    cA, jA = load_half(f"{phi}__certA")
    cB, jB = load_half(f"{phi}__certB")
    r = LP.combine(cA, cB)
    out = {"q": r["q"], "meta": {"A": jA["meta"], "B": jB["meta"]}}
    for fam in ("G", "L", "GL"):
        if fam in r:
            out[fam] = {"ceiling": r[fam]["ceiling"], "se": r[fam]["se"], "best": r[fam]["best"]}
    out["G_half_A_cert"], out["G_half_B_cert"] = r["G_half_A_cert"], r["G_half_B_cert"]
    out["logdet"] = {k: v for k, v in r["logdet"].items()}
    out["nontriv"] = {k: float(np.mean([jA["nontriv"][k], jB["nontriv"][k]])) for k in jA["nontriv"]}
    agr = {}
    for k in b4.HAND:
        a, b = jA["agreement"].get(k, {}), jB["agreement"].get(k, {})
        if "R2_H_from_Z" in a and "R2_H_from_Z" in b:
            agr[k] = {d: float(np.mean([a[d]["R2"], b[d]["R2"]])) for d in ("R2_H_from_Z", "R2_Z_from_H")
                      if a[d]["R2"] is not None and b[d]["R2"] is not None}
    out["agreement"] = agr
    out["tau_half_G"] = LP.tau_half(out["G"]["ceiling"])
    return out


def seed_agreement(name):
    out = {}
    for ch in b4.HALVES:
        p0, p1 = f"{LAT}/{name}_s0__cert{ch}.npz", f"{LAT}/{name}_s1__cert{ch}.npz"
        if not (os.path.exists(p0) and os.path.exists(p1)):
            continue
        Z0 = np.load(p0)["Zt"].astype(np.float64)
        Z1 = np.load(p1)["Zt"].astype(np.float64)
        g = np.repeat(np.arange(Z0.shape[0]) % 4, Z0.shape[1])
        Z0, Z1 = Z0.reshape(-1, Z0.shape[-1]), Z1.reshape(-1, Z1.shape[-1])
        out[ch] = {"R2_s1_from_s0": bcert.cv_r2(Z0, Z1, g)["R2"], "R2_s0_from_s1": bcert.cv_r2(Z1, Z0, g)["R2"]}
    if out:
        out["mean"] = float(np.mean([v[k] for v in out.values() for k in v]))
    return out


def main():
    stems = sorted(os.path.basename(p)[:-5] for p in glob.glob(f"{CERT}/*.json"))
    phis = sorted({s.rsplit("__cert", 1)[0] for s in stems})
    P, missing = {}, []
    for phi in phis:
        if f"{phi}__certA" in stems and f"{phi}__certB" in stems:
            try:
                P[phi] = pooled(phi)
            except Exception as exc:
                missing.append((phi, repr(exc)))
        else:
            missing.append((phi, "one half missing"))
    log("pooled", len(P), "phis; missing", len(missing))
    cfgs = {}
    for nm, e, h, o, c in [(n, "L", hh, "rand", cc) for n, hh, cc in b4.RANDOM] + b4.configs():
        ss = [P.get(f"{nm}_s{s}") for s in (0, 1)]
        ss = [x for x in ss if x is not None]
        if not ss:
            continue
        row = {"enc": e, "h": h, "obj": o, "c": c, "n_seeds": len(ss)}
        for fam in ("G", "GL"):
            cs = np.array([x[fam]["ceiling"] for x in ss if fam in x])
            if len(cs):
                row[f"ceiling_{fam}"] = cs.mean(0)
                row[f"ceiling_{fam}_se_mean"] = np.mean([x[fam]["se"] for x in ss if fam in x], 0)
                if len(cs) == 2:
                    row[f"ceiling_{fam}_seed_diff"] = cs[0] - cs[1]
        row["I_capt"] = np.mean([x["logdet"]["I_capt"] for x in ss], 0)
        row["I_avail"] = np.mean([x["logdet"]["I_avail"] for x in ss], 0)
        row["nontriv"] = {k: float(np.mean([x["nontriv"][k] for x in ss])) for k in ss[0]["nontriv"]}
        row["agreement"] = {k: {d: float(np.mean([x["agreement"][k][d] for x in ss if k in x["agreement"] and d in x["agreement"][k]]))
                                for d in ("R2_H_from_Z", "R2_Z_from_H")} for k in b4.HAND if all(k in x["agreement"] for x in ss)}
        row["seed_agreement"] = seed_agreement(nm)
        row["tau_half_G"] = LP.tau_half(row["ceiling_G"])
        cfgs[nm] = row
    hand = {k: P[f"hand_{k}"] for k in b4.HAND if f"hand_{k}" in P}
    wins = {}
    for p in sorted(glob.glob(os.path.join(OUT, "windows", "*.npz"))):
        try:
            wins[os.path.basename(p)[:-4]] = BW.window_stats(np.load(p))
        except Exception as exc:
            wins[os.path.basename(p)[:-4]] = {"error": repr(exc)}
    b4.jdump({"phis": P, "configs": cfgs, "hand": hand, "windows": wins, "missing": missing,
              "horizons": b4.HZ, "layout": {"J_CERT": b4.J_CERT, "J_EXTRA": b4.J_EXTRA, "T": b4.T, "TEST": b4.TEST,
                                            "TB": b4.TB, "R_BR": b4.R_BR, "tiny": b4.TINY}},
             os.path.join(OUT, "combined.json"))
    lines = ["config | G ceiling h=1,2,4,8,16 | seed diff | R2(mass|Z) R2(Z|mass) | R2(view|Z) | seed R2"]
    for nm, r in cfgs.items():
        a = r["agreement"]
        lines.append(f"{nm} | {np.round(r['ceiling_G'], 3).tolist()} | {np.round(r.get('ceiling_G_seed_diff', np.zeros(5)), 3).tolist()} | "
                     f"{a.get('mass', {}).get('R2_H_from_Z', float('nan')):.3f} {a.get('mass', {}).get('R2_Z_from_H', float('nan')):.3f} | "
                     f"{a.get('view', {}).get('R2_H_from_Z', float('nan')):.3f} | {r['seed_agreement'].get('mean', float('nan')):.3f}")
    for k, r in hand.items():
        lines.append(f"hand_{k} | {np.round(r['G']['ceiling'], 3).tolist()}")
    with open(os.path.join(OUT, "table.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    log("written combined.json and table.txt;", len(cfgs), "configs,", len(hand), "hand designs,", len(wins), "windows")


if __name__ == "__main__":
    main()
