"""ccombine -- pool the certified halves, seed stability, window statistics -> $B5_OUT/combined.json (study `bias2`).

usage: python -B ccombine.py          (B5_WORLD)
Per Phi (a config and seed, or a hand design): the two certification halves (Phi fitted on B certified on A, and
vice versa) pooled with lphi.combine (closure ceilings for the fixed families G, L = local ridge, GL = G + local
ridge; bootstrap SE over trajectories; Gaussian log-det measures averaged over halves), the persistence ceiling,
non-triviality and agreement averaged over halves. Per config: seed means, seed differences of the ceilings, and
the latent agreement between the two seeds on the same certification half (per-block linear readout and round 4's
global ridge, both directions).
"""
import glob
import json
import os
import time

import numpy as np

import c5

CL, LP = c5.setup_paths(closure=True)
import ccert  # noqa: E402  (agreement metrics)
import cwin as CW  # noqa: E402

CERT = c5.work_dir("cert")
LAT = c5.work_dir("lat")
OUT = c5.out_dir()
T0 = time.time()
DIRS = ("H_from_Z", "Z_from_H")


def log(*a):
    c5.progress(f"[ccombine {time.time() - T0:7.1f}s] " + " ".join(str(x) for x in a))


def load_half(stem):
    d = np.load(f"{CERT}/{stem}.npz")
    js = json.load(open(f"{CERT}/{stem}.json"))
    names = [str(n) for n in d["names"]]
    ld = {k: (np.asarray(v, float) if k not in ("bestG", "q") else v) for k, v in js["ld"].items()}
    return {"err": {n: d["err"][i] for i, n in enumerate(names)}, "orac": d["orac"], "item_j": d["item_j"],
            "ld": ld, "q": js["q"]}, js


def _mean(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    return np.mean(np.asarray(vals, float), 0)


def pooled(phi):
    cA, jA = load_half(f"{phi}__certA")
    cB, jB = load_half(f"{phi}__certB")
    r = LP.combine(cA, cB)
    out = {"q": r["q"], "meta": {"A": jA["meta"], "B": jB["meta"]}}
    for fam in ("G", "L", "GL"):
        if fam in r:
            out[fam] = {"ceiling": r[fam]["ceiling"], "se": r[fam]["se"], "best": r[fam]["best"]}
    V0 = np.concatenate([cA["err"]["mean"], cB["err"]["mean"]]).mean(0)
    Vp = np.concatenate([cA["err"]["persistence"], cB["err"]["persistence"]]).mean(0)
    Vu = np.concatenate([cA["orac"], cB["orac"]]).mean(0)
    out["persistence_ceiling"] = (V0 - Vp) / (V0 - Vu)
    out["oracle_share_of_V0"] = Vu / V0
    out["G_half_A_cert"], out["G_half_B_cert"] = r["G_half_A_cert"], r["G_half_B_cert"]
    out["logdet"] = {k: v for k, v in r["logdet"].items()}
    out["nontriv"] = {k: _mean([jA["nontriv"][k], jB["nontriv"][k]]) for k in jA["nontriv"] if k != "block_autocorr"}
    out["nontriv"]["block_autocorr"] = {h: _mean([jA["nontriv"]["block_autocorr"][h], jB["nontriv"]["block_autocorr"][h]])
                                        for h in jA["nontriv"]["block_autocorr"]}
    agr = {}
    for k in c5.agree_targets():
        a, b = jA["agreement"].get(k, {}), jB["agreement"].get(k, {})
        if "error" in a or "error" in b or not a or not b:
            continue
        agr[k] = {m: {d: _mean([a[m][d], b[m][d]]) for d in DIRS} for m in ccert.MODES}
    out["agreement"] = agr
    out["tau_half_G"] = LP.tau_half(out["G"]["ceiling"])
    return out


def seed_agreement(name, c):
    out = {}
    for ch in c5.HALVES:
        p0, p1 = f"{LAT}/{name}_s0__cert{ch}.npz", f"{LAT}/{name}_s1__cert{ch}.npz"
        if not (os.path.exists(p0) and os.path.exists(p1)):
            continue
        Z0 = np.load(p0)["Zt"].astype(np.float64)[:, ::ccert.TSTRIDE]
        Z1 = np.load(p1)["Zt"].astype(np.float64)[:, ::ccert.TSTRIDE]
        g = np.repeat(np.arange(Z0.shape[0]) % 4, Z0.shape[1])
        Z0, Z1 = Z0.reshape(-1, Z0.shape[-1]), Z1.reshape(-1, Z1.shape[-1])
        gb = np.repeat(g, ccert.NB)
        b0, b1 = ccert.block_rows(Z0, c).reshape(-1, c), ccert.block_rows(Z1, c).reshape(-1, c)
        out[ch] = {"loc1_s1_from_s0": ccert.local_r2(b0, b1, gb), "loc1_s0_from_s1": ccert.local_r2(b1, b0, gb),
                   "glob_s1_from_s0": ccert.cv_r2(Z0, Z1, g), "glob_s0_from_s1": ccert.cv_r2(Z1, Z0, g)}
    if out:
        halves = list(out.values())
        for m in ("loc1", "glob"):
            vals = [v[k] for v in halves for k in v if k.startswith(m) and v[k] is not None]
            out[f"{m}_mean"] = float(np.mean(vals)) if vals else None
    return out


def agg_agreement(ss):
    out = {}
    for k in c5.agree_targets():
        if not all(k in x["agreement"] for x in ss):
            continue
        out[k] = {m: {d: _mean([x["agreement"][k][m][d] for x in ss]) for d in DIRS} for m in ccert.MODES}
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
    log("pooled", len(P), "phis; missing", len(missing), missing[:5])
    cfgs = {}
    for nm, e, h, o, c in [(n, "L", hh, "rand", cc) for n, hh, cc in c5.RANDOM] + c5.configs():
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
        row["persistence_ceiling"] = np.mean([x["persistence_ceiling"] for x in ss], 0)
        row["oracle_share_of_V0"] = np.mean([x["oracle_share_of_V0"] for x in ss], 0)
        row["I_capt"] = np.mean([x["logdet"]["I_capt"] for x in ss], 0)
        row["I_avail"] = np.mean([x["logdet"]["I_avail"] for x in ss], 0)
        row["nontriv"] = {k: _mean([x["nontriv"][k] for x in ss]) for k in ss[0]["nontriv"] if k != "block_autocorr"}
        row["nontriv"]["block_autocorr"] = {hh: _mean([x["nontriv"]["block_autocorr"][hh] for x in ss])
                                            for hh in ss[0]["nontriv"]["block_autocorr"]}
        row["agreement"] = agg_agreement(ss)
        row["seed_agreement"] = seed_agreement(nm, c)
        row["tau_half_G"] = LP.tau_half(row["ceiling_G"])
        tr = os.path.join(OUT, "train", f"{nm}.json")
        if os.path.exists(tr):
            infos = json.load(open(tr))
            row["train"] = {"val_init": [i["val_init"] for i in infos], "val_best": [i["val_best"] for i in infos],
                            "best_step": [i["best_step"] for i in infos], "steps": infos[0]["steps"],
                            "whitening": infos[0]["whitening"], "min_rel_eig_latent_cov": [i["min_rel_eig_latent_cov"] for i in infos]}
            if "field_shares" in infos[0]:
                keys = list(infos[0]["field_shares"][0]["share"])
                row["field_shares"] = [{k: float(np.mean([i["field_shares"][ch]["share"][k] for i in infos])) for k in keys}
                                       for ch in range(c)]
                row["field_shares_replicas"] = [[i["field_shares"][ch]["share"] for i in infos] for ch in range(c)]
                row["field_corr_with_z"] = [{k: float(np.mean([abs(i["field_shares"][ch]["corr_with_z"][k]) for i in infos])) for k in keys}
                                            for ch in range(c)]
        cfgs[nm] = row
    hand = {k: P[f"hand_{k}"] for k, _ in c5.hand_names() if f"hand_{k}" in P}
    wins = {}
    for p in sorted(glob.glob(os.path.join(OUT, "windows", "*.npz"))):
        try:
            wins[os.path.basename(p)[:-4]] = CW.window_stats(np.load(p), list(c5.FIELDS))
        except Exception as exc:
            wins[os.path.basename(p)[:-4]] = {"error": repr(exc)}
    c5.jdump({"world": c5.WORLD, "fields": list(c5.FIELDS), "phis": P, "configs": cfgs, "hand": hand, "windows": wins,
              "missing": missing, "horizons": c5.HZ, "agree_targets": c5.agree_targets(),
              "layout": {"J_CERT": c5.J_CERT, "J_EXTRA_requested": c5.J_EXTRA, "T": c5.T, "TEST": c5.TEST, "TB": c5.TB,
                         "R_BR": c5.R_BR, "BURN": c5.BURN, "STRIDE": c5.STRIDE, "tiny": c5.TINY}},
             os.path.join(OUT, "combined.json"), indent=None)
    best = lambda r: max(((k, v["loc1"]["H_from_Z"]) for k, v in r["agreement"].items()                # noqa: E731
                          if k.endswith("_h0") and v["loc1"]["H_from_Z"] is not None), key=lambda kv: kv[1], default=("-", float("nan")))
    lines = ["config | G ceiling h=1,2,4,8,16 | PR | best block design by loc1 R2(H|Z) | seed loc1 R2"]
    for nm, r in cfgs.items():
        b = best(r)
        sa = r["seed_agreement"].get("loc1_mean")
        lines.append(f"{nm} | {np.round(r['ceiling_G'], 3).tolist()} | {r['nontriv']['participation_ratio']:.1f} | "
                     f"{b[0]} {b[1]:.3f} | {sa if sa is None else round(sa, 3)}")
    for k, r in hand.items():
        lines.append(f"hand_{k} | {np.round(r['G']['ceiling'], 3).tolist()} | {float(r['nontriv']['participation_ratio']):.1f}")
    with open(os.path.join(OUT, "table.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    log("written combined.json and table.txt;", len(cfgs), "configs,", len(hand), "hand designs,", len(wins), "windows")
    if not cfgs or not hand:
        raise SystemExit("nothing certified")


if __name__ == "__main__":
    main()
