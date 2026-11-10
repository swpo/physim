"""scombine -- pool the certified halves of the round-5 study `slots` (see s5.py, scert.py).

usage: python -B scombine.py        -> $S5_OUT/combined.json, $S5_OUT/table.txt
Per Phi (both certification halves pooled; a learned Phi is certified on the half it was not fitted on):
  ceilings per predictor family (scert.FAMILIES) at h = 1, 2, 4, 8, 16: (V0 - V_best) / (V0 - V_oracle), the best
  predictor chosen per horizon on the pooled items; SE from 400 bootstrap resamples of trajectories (selection
  repeated inside each resample);
  predictable content: Gaussian log-det I_avail / I_capt (mean of the two halves; None when a half is singular)
  and the diagonal version (sum over coordinates of 1/2 log variance ratios, oracle ratio floored at 1e-4);
  agreement with the tracker, territory and non-triviality (mean of the halves).
Per learned config: the two seeds side by side and their agreement on the same frames (seed 0 vs seed 1 fitted on
the same half): matter-weighted ARI of the hard segmentations and cross-validated R^2 between matched slots'
certified numbers (assignment on shared matter per frame, both directions); the same ARI against km_s6.
"""
import glob
import json
import os
import time

import numpy as np
from scipy.optimize import linear_sum_assignment

import s5
import scert as SC

T0 = time.time()
CERT = s5.work_dir("cert")
LAT = s5.work_dir("lat")
PAIR = s5.work_dir("pair")
OUT = s5.out_dir()
K = s5.K
HZ = list(s5.HZ)
NB = 400


def log(*a):
    s5.progress(f"[scombine {time.time() - T0:7.1f}s] " + " ".join(str(x) for x in a))


def mean_tree(a, b):
    """Mean of two JSON trees (numbers averaged, None if either is None, other leaves from a)."""
    if isinstance(a, dict) and isinstance(b, dict):
        return {k: mean_tree(a[k], b[k]) if k in b else a[k] for k in a}
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return [mean_tree(x, y) for x, y in zip(a, b)]
    if isinstance(a, bool) or isinstance(b, bool):
        return a
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return 0.5 * (a + b)
    if a is None or b is None:
        return None
    return a


def pool_phi(phi, chs):
    js = {ch: json.load(open(f"{CERT}/{phi}__cert{ch}.json")) for ch in chs}
    layout = js[chs[0]]["layout"]
    if not all(js[ch].get("certified", True) for ch in chs):       # agreement only (scert, S5_CERT_O=refs)
        res = {"phi": phi, "layout": layout, "q": js[chs[0]]["q"], "halves": list(chs), "families": {}, "certified": False}
        for k in ("agreement", "territory", "nontriv"):
            if all(k in js[ch] for ch in chs):
                v = js[chs[0]][k]
                for ch in chs[1:]:
                    v = mean_tree(v, js[ch][k])
                res[k] = v
        res["meta"] = {ch: {k: v for k, v in js[ch]["meta"].items() if k not in ("cfg",)} for ch in chs}
        res["cfg"] = js[chs[0]]["meta"].get("cfg")
        res["cert_seconds"] = [js[ch]["seconds"]["total"] for ch in chs]
        return res
    nz = {ch: np.load(f"{CERT}/{phi}__cert{ch}.npz") for ch in chs}
    names = sorted(set.intersection(*[set(str(n) for n in nz[ch]["names"]) for ch in chs]))
    err = {nm: np.concatenate([nz[ch]["err"][list(nz[ch]["names"]).index(nm)] for ch in chs]) for nm in names}
    orac = np.concatenate([nz[ch]["orac"] for ch in chs])
    ij = np.concatenate([nz[ch]["item_j"] + i * s5.J_CERT for i, ch in enumerate(chs)])
    uj = np.unique(ij)
    rng = np.random.default_rng(0)
    boots = [np.concatenate([np.flatnonzero(ij == u) for u in rng.choice(uj, uj.size, replace=True)]) for _ in range(NB)]
    allidx = np.arange(len(ij))
    res = {"phi": phi, "layout": layout, "q": js[chs[0]]["q"], "halves": list(chs), "n_items": int(len(ij)),
           "n_eff": [js[ch]["n_eff"] for ch in chs], "families": {}}

    def fam_stats(idx, nms):
        V0, Vu = err["mean"][idx].mean(0), orac[idx].mean(0)
        Vs = np.stack([err[nm][idx].mean(0) for nm in nms])
        return (V0 - Vs.min(0)) / (V0 - Vu), Vs.argmin(0), V0, Vu, Vs.min(0)
    for fam, nms in SC.FAMILIES[layout].items():
        nms = [nm for nm in nms if nm in err]
        c, arg, V0, Vu, Vb = fam_stats(allidx, nms)
        se = np.std([fam_stats(b, nms)[0] for b in boots], 0)
        res["families"][fam] = {"ceiling": c, "se": se, "best": [nms[a] for a in arg], "V0": V0, "V_oracle": Vu, "V_best": Vb,
                                "members": nms}
        # diagonal information, per half then averaged
        ia, ic = [], []
        for ch in chs:
            nml = [str(n) for n in nz[ch]["names"]]
            Vc, Vo = nz[ch]["Vc"], nz[ch]["Vc_orac"]
            Vm = Vc[nml.index("mean")]
            ok = Vm > 1e-12
            ia.append([0.5 * np.log(Vm[hi][ok[hi]] / np.maximum(Vo[hi][ok[hi]], 1e-4 * Vm[hi][ok[hi]])).sum() for hi in range(len(HZ))])
            ic.append([0.5 * np.log(Vm[hi][ok[hi]] / np.maximum(Vc[nml.index(nms[arg[hi]])][hi][ok[hi]], 1e-4 * Vm[hi][ok[hi]])).sum()
                       for hi in range(len(HZ))])
        res["families"][fam]["I_capt_diag"] = np.mean(ic, 0)
        res["I_avail_diag"] = np.mean(ia, 0)
    V = {nm: err[nm].mean(0) for nm in names}
    res["V"] = V
    res["V_oracle"] = orac.mean(0)
    ld = js[chs[0]]["ld"]
    for ch in chs[1:]:
        ld = mean_tree(ld, js[ch]["ld"])
    res["logdet"] = ld
    for k in ("agreement", "territory", "nontriv"):
        if all(k in js[ch] for ch in chs):
            v = js[chs[0]][k]
            for ch in chs[1:]:
                v = mean_tree(v, js[ch][k])
            res[k] = v
    res["meta"] = {ch: {k: v for k, v in js[ch]["meta"].items() if k not in ("cfg",)} for ch in chs}
    res["cfg"] = js[chs[0]]["meta"].get("cfg")
    res["cert_seconds"] = [js[ch]["seconds"]["total"] for ch in chs]
    return res


def ari_frames(C):
    """C (..., K, K) matter-weighted contingency -> ARI per frame (pair weights w_p w_q)."""
    a, b, N = C.sum(-1), C.sum(-2), C.sum((-2, -1))
    ex = (a ** 2).sum(-1) * (b ** 2).sum(-1) / np.maximum(N ** 2, 1e-30)
    den = 0.5 * ((a ** 2).sum(-1) + (b ** 2).sum(-1)) - ex
    return np.where(den > 1e-9, ((C ** 2).sum((-2, -1)) - ex) / np.maximum(den, 1e-9), 1.0)


def seed_pair(cfgname, ch):
    """Seed 0 vs seed 1 of one config on certification half ch (both fitted on the other half)."""
    p = f"{PAIR}/{cfgname}_s0__vs_{cfgname}_s1__cert{ch}.npz"
    if not os.path.exists(p):
        return None
    C = np.load(p)["C"].astype(np.float64)
    out = {"ari": float(ari_frames(C).mean())}
    lat = [f"{LAT}/{cfgname}_s{s}__cert{ch}.npz" for s in (0, 1)]
    if not all(os.path.exists(x) for x in lat):
        return out
    Z = [np.load(x)["Zt"].astype(np.float64) for x in lat]
    d = Z[0].shape[-1] // K
    Z = [z.reshape(z.shape[:2] + (K, d)) for z in Z]
    if d == 12:
        Z = [z[..., list(s5.MP6)] for z in Z]
    X, Y, g = [], [], []
    for j in range(C.shape[0]):
        for t in range(0, C.shape[1], 4):
            r, c = linear_sum_assignment(-C[j, t])
            ok = C[j, t][r, c] > s5.M_MIN
            X.append(Z[0][j, t, r[ok]])
            Y.append(Z[1][j, t, c[ok]])
            g.append(np.full(int(ok.sum()), j % 4))
    X, Y, g = np.concatenate(X), np.concatenate(Y), np.concatenate(g)

    def r2(A, B):
        s = B.std(0)
        keep = s > 1e-9 * max(float(s.max()), 1e-30)
        R2, _ = SC.cv_ridge(A, (B[:, keep] - B[:, keep].mean(0)) / s[keep], g)
        return float(np.mean(R2))
    out.update(n_pairs=int(len(X)), R2_s1_from_s0=r2(X, Y), R2_s0_from_s1=r2(Y, X))
    return out


def main():
    stems = sorted(os.path.basename(p)[:-5] for p in glob.glob(f"{CERT}/*__cert?.json"))
    phis = {}
    for st in stems:
        phi, ch = st.rsplit("__cert", 1)
        phis.setdefault(phi, []).append(ch)
    res, missing = {}, []
    for phi, chs in phis.items():
        try:
            res[phi] = pool_phi(phi, sorted(chs))
            if len(chs) < 2:
                missing.append(f"{phi}: only half {chs}")
        except Exception as exc:
            missing.append(f"{phi}: {exc!r}")
    log(f"pooled {len(res)} phis; problems {missing}")
    # learned configs: seeds side by side, seed stability, distance from k-means
    configs = {}
    for phi, r in res.items():
        m = next(iter(r["meta"].values()))
        if m.get("kind") != "learned" or "@" in phi:
            continue
        configs.setdefault(m["config"], {"phis": [], "obj": m["obj"], "readout": m["readout"]})["phis"].append(phi)
    for name, c in configs.items():
        sp = [seed_pair(name, ch) for ch in s5.HALVES]
        sp = [x for x in sp if x]
        if sp:
            v = sp[0]
            for x in sp[1:]:
                v = mean_tree(v, x)
            c["seed_pair"] = v
        km = []
        for phi in c["phis"]:
            for ch in s5.HALVES:
                p = f"{PAIR}/{phi}__vs_km_s6__cert{ch}.npz"
                if os.path.exists(p):
                    km.append(float(ari_frames(np.load(p)["C"].astype(np.float64)).mean()))
        c["ari_vs_km_s6"] = float(np.mean(km)) if km else None
        tj = os.path.join(OUT, "train", f"{name}.json")
        if os.path.exists(tj):
            infos = json.load(open(tj))["infos"]
            c["val_best"] = [i["val_best"] for i in infos]
            c["best_step"] = [i["best_step"] for i in infos]
            c["moved_from_kmeans"] = [i["moved_from_kmeans"] for i in infos]
            c["skipped_steps"] = infos[0]["skipped_steps_all_replicas"]
    objval = {os.path.basename(p)[:-5]: json.load(open(p)) for p in sorted(glob.glob(os.path.join(OUT, "objval", "*.json")))}
    s5.jdump({"phis": res, "configs": configs, "objval": objval, "problems": missing, "horizons": HZ,
              "size": s5.SIZE, "layout": {"J_CERT": s5.J_CERT, "J_EXTRA": s5.J_EXTRA, "T": s5.T, "test_ticks": list(s5.TEST),
                                          "TB": s5.TB, "R_BR": s5.R_BR, "seeds": s5.SEEDS}},
             os.path.join(OUT, "combined.json"))
    # readable table
    f3 = lambda v: "   -  " if v is None else f"{v:6.3f}"
    lines = ["phi                     q  fam  ceiling h=1,2,4,8,16             | ARI   rec   prec  spo  massR2 posR2 velR2 | "
             "probe(rff) mass pos vel | territ"]
    for phi in sorted(res):
        r = res[phi]
        fam = "O" if "O" in r["families"] else ("S" if "S" in r["families"] else ("GL" if "GL" in r["families"] else "-"))
        c = r["families"][fam]["ceiling"] if fam != "-" else [float("nan")] * len(HZ)
        a = r.get("agreement")
        t = r.get("territory") or {}
        ag = "".join(f3(x) for x in ((a["ari_hard_matter_weighted"], a["recall"], a["precision"], a["slots_per_object"],
                                     a["direct"]["mass_R2"], a["direct"]["pos_R2"], a["direct"]["vel_R2"]) if a else [None] * 7))
        pr = "".join(f3(x) for x in ((a["probe_rff"]["mass_R2"], a["probe_rff"]["pos_R2"], a["probe_rff"]["vel_R2"])
                                     if a and "probe_rff" in a else [None] * 3))
        lines.append(f"{phi:22s} {r['q']:3d} {fam:>3s} " + " ".join(f"{x:6.3f}" for x in c) + " |" + ag + " |" + pr + " |" +
                     f3(t.get("resultant_length")))
    lines.append("")
    lines.append("objective values (frozen readout, heads trained from scratch; mean over replicas): set, self, rec")
    for nm, o in objval.items():
        lines.append(f"{nm:22s} " + " ".join(f"{k} {np.mean(o[k]['val']):7.4f}" for k in ("set", "self", "rec") if o.get(k)))
    lines.append("")
    lines.append("seed pairs: config, ARI(s0, s1), R2(s1|s0), R2(s0|s1), ARI vs km_s6")
    for nm, c in configs.items():
        sp = c.get("seed_pair") or {}
        lines.append(f"{nm:22s} {f3(sp.get('ari'))} {f3(sp.get('R2_s1_from_s0'))} {f3(sp.get('R2_s0_from_s1'))} {f3(c.get('ari_vs_km_s6'))}")
    open(os.path.join(OUT, "table.txt"), "w").write("\n".join(lines) + "\n")
    log("written combined.json and table.txt;", len(res), "phis,", len(configs), "learned configs")


if __name__ == "__main__":
    main()
