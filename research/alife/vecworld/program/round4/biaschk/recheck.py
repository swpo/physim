"""Independent recomputation of the r4-bias-003 headline numbers (checker of round-4 study `bias`).

usage: python -I -B recheck.py OUT_DIR BIAS_RESULTS_DIR RESULT_JSON
OUT_DIR = jobs/r4-bias-003/out extracted from origin/gpu-jobs (git archive origin/gpu-jobs jobs/r4-bias-003 | tar -x).
Own code (does not import the study modules): pooled closure ceilings G and GL from items/*.npz (per-item errors of
learned_phi2's fixed family, both certification halves), seed means and seed differences; half/seed averages of the
per-half Gaussian log-det measures, agreement R^2 and participation ratio from cert/*.json (the latents themselves
stayed on the pod, so log-dets, agreement R^2 and seed R^2 can only be re-averaged, not recomputed); cosines of the
learned linear windows (raw units) to the block-mass window from windows/*.npz. Compares with combined.json.
"""
import glob
import json
import os
import sys

import numpy as np

O = sys.argv[1]                   # .../jobs/r4-bias-003/out
RES = sys.argv[2]                 # repo results dir (combined.json, summary.json)
C = json.load(open(os.path.join(RES, "combined.json")))
FAMG = ["mean", "persistence", "ar1", "ridge_p1", "ridge_p2", "ridge_p4", "ridge_p8", "knn"]
NJ = 32


def load_items(phi, h):
    d = np.load(f"{O}/items/{phi}__cert{h}.npz")
    names = [str(n) for n in d["names"]]
    return {n: d["err"][i].astype(np.float64) for i, n in enumerate(names)}, d["orac"].astype(np.float64), d["item_j"]


def ceiling(phi, fam="G"):
    eA, oA, jA = load_items(phi, "A")
    eB, oB, jB = load_items(phi, "B")
    err = {n: np.concatenate([eA[n], eB[n]]) for n in eA if n in eB}
    orac = np.concatenate([oA, oB])
    names = [n for n in FAMG if n in err] + (["lridge"] if fam == "GL" and "lridge" in err else [])
    V0 = err["mean"].mean(0)
    Vu = orac.mean(0)
    Vb = np.min(np.stack([err[n].mean(0) for n in names]), 0)
    return (V0 - Vb) / (V0 - Vu)


def cert(phi, h):
    return json.load(open(f"{O}/cert/{phi}__cert{h}.json"))


def ld(phi, key):
    return np.mean([np.asarray(cert(phi, h)["ld"][key], float) for h in "AB"], 0)


def agr(phi, k, d):
    return float(np.mean([cert(phi, h)["agreement"][k][d]["R2"] for h in "AB"]))


def pr(phi):
    return float(np.mean([cert(phi, h)["nontriv"]["participation_ratio"] for h in "AB"]))


stems = sorted({os.path.basename(p).rsplit("__cert", 1)[0] for p in glob.glob(f"{O}/cert/*.json")})
cfgs = sorted({s.rsplit("_s", 1)[0] for s in stems if not s.startswith("hand_")})
hands = [s[5:] for s in stems if s.startswith("hand_")]
n_files = len(glob.glob(f"{O}/cert/*.json"))
R = {"n_phi": len(stems), "n_cert_files": n_files, "n_configs": len(cfgs), "cfg": {}, "hand": {}}
maxdev = {"ceiling_G": 0.0, "ceiling_GL": 0.0, "I_avail": 0.0, "I_capt": 0.0, "agreement": 0.0, "pr": 0.0}
for c in cfgs:
    s = [f"{c}_s0", f"{c}_s1"]
    cg = np.array([ceiling(p) for p in s])
    cgl = np.array([ceiling(p, "GL") for p in s])
    row = {"ceiling_G": cg.mean(0), "seed_diff": cg[0] - cg[1], "ceiling_GL": cgl.mean(0),
           "I_avail": np.mean([ld(p, "I_avail") for p in s], 0), "I_capt": np.mean([ld(p, "I_capt") for p in s], 0),
           "pr": float(np.mean([pr(p) for p in s])),
           "agr": {k: {d: float(np.mean([agr(p, k, d) for p in s])) for d in ("R2_H_from_Z", "R2_Z_from_H")} for k in hands}}
    R["cfg"][c] = row
    cc = C["configs"][c]
    maxdev["ceiling_G"] = max(maxdev["ceiling_G"], float(np.abs(row["ceiling_G"] - np.asarray(cc["ceiling_G"])).max()))
    maxdev["ceiling_GL"] = max(maxdev["ceiling_GL"], float(np.abs(row["ceiling_GL"] - np.asarray(cc["ceiling_GL"])).max()))
    maxdev["I_avail"] = max(maxdev["I_avail"], float(np.abs(row["I_avail"] - np.asarray(cc["I_avail"])).max()))
    maxdev["I_capt"] = max(maxdev["I_capt"], float(np.abs(row["I_capt"] - np.asarray(cc["I_capt"])).max()))
    maxdev["pr"] = max(maxdev["pr"], abs(row["pr"] - cc["nontriv"]["participation_ratio"]))
    for k in hands:
        for d in ("R2_H_from_Z", "R2_Z_from_H"):
            maxdev["agreement"] = max(maxdev["agreement"], abs(row["agr"][k][d] - cc["agreement"][k][d]))
for k in hands:
    p = f"hand_{k}"
    R["hand"][k] = {"ceiling_G": ceiling(p), "ceiling_GL": ceiling(p, "GL"), "I_avail": ld(p, "I_avail"),
                    "I_capt": ld(p, "I_capt"), "pr": pr(p),
                    "agr": {kk: {d: agr(p, kk, d) for d in ("R2_H_from_Z", "R2_Z_from_H")} for kk in hands}}
    hc = C["hand"][k]
    maxdev["ceiling_G"] = max(maxdev["ceiling_G"], float(np.abs(R["hand"][k]["ceiling_G"] - np.asarray(hc["G"]["ceiling"])).max()))
    maxdev["I_avail"] = max(maxdev["I_avail"], float(np.nanmax(np.abs(R["hand"][k]["I_avail"] - np.asarray(hc["logdet"]["I_avail"], dtype=float)))))
print("phis", R["n_phi"], "cert files", R["n_cert_files"], "configs", R["n_configs"], "hands", hands)
print("max |mine - combined.json|:", {k: f"{v:.2e}" for k, v in maxdev.items()})
maxdev = {k: float(f"{v:.3g}") for k, v in maxdev.items()}

f3 = lambda v: np.round(np.asarray(v, float), 3).tolist()
H = R["hand"]
K = R["cfg"]
print("\n== claim 1/2/3/6 rows: ceiling_G | I_avail h1 | I_capt h1 | PR | mass H|Z, Z|H | tent H|Z, Z|H | chan Z|H | seed diff max")
for c in ["N0_clos_c1", "N4_clos_c1", "N8_clos_c1", "N16_clos_c1", "L0_clos_c1", "N0_local_c1", "L0_local_c1",
          "N0_recon_c1", "L0_recon_c1", "U_recon_c1", "U_clos_c1", "N0_pib_c1", "N0_clos_c2", "N0_clos_c4", "rand8_c1"]:
    r = K[c]
    a = r["agr"]
    print(c, f3(r["ceiling_G"]), round(r["I_avail"][0], 1), round(r["I_capt"][0], 1), round(r["pr"], 1),
          round(a["mass"]["R2_H_from_Z"], 3), round(a["mass"]["R2_Z_from_H"], 3), "| tent",
          round(a["tent"]["R2_H_from_Z"], 3), round(a["tent"]["R2_Z_from_H"], 3), "| chanZ|H", round(a["chan"]["R2_Z_from_H"], 3),
          "| sd", round(float(np.abs(r["seed_diff"]).max()), 3))
for k in hands:
    h = H[k]
    print("hand", k, f3(h["ceiling_G"]), round(h["I_avail"][0], 1), round(h["I_capt"][0], 1), round(h["pr"], 1),
          "objmass H|Z", round(h["agr"]["objmass"]["R2_H_from_Z"], 3))
print("hand mass<->tent agreement:", {d: round(H["mass"]["agr"]["tent"][d], 3) for d in ("R2_H_from_Z", "R2_Z_from_H")},
      "mass<->view:", {d: round(H["mass"]["agr"]["view"][d], 3) for d in ("R2_H_from_Z", "R2_Z_from_H")})

learned = [c for c in cfgs if not c.startswith("rand")]
print("\n== claim 4: max I_avail / I_capt at h=1 among learned latents by width")
for w in (1, 2, 4):
    cs = [c for c in learned if c.endswith(f"_c{w}")]
    ia = max(cs, key=lambda c: K[c]["I_avail"][0])
    ic = max(cs, key=lambda c: K[c]["I_capt"][0])
    print(f"c={w}", len(cs), "configs; I_avail max", ia, round(K[ia]["I_avail"][0], 1), "; I_capt max", ic, round(K[ic]["I_capt"][0], 1))
    nar = [c for c in cs if c.startswith("N")]
    ia = max(nar, key=lambda c: K[c]["I_avail"][0])
    print("   N arm I_avail max", ia, round(K[ia]["I_avail"][0], 1), round(K[ia]["I_capt"][0], 1))

print("\n== claim 5: local vs clos (ceiling diff local - clos per horizon; I_capt h1 local, clos; SE mean)")
for e in ("N", "L"):
    for hh in (0, 4, 8, 16):
        lo, cl = K[f"{e}{hh}_local_c1"], K[f"{e}{hh}_clos_c1"]
        se = np.asarray(C["configs"][f"{e}{hh}_clos_c1"]["ceiling_G_se_mean"])
        print(f"{e}{hh}", f3(lo["ceiling_G"] - cl["ceiling_G"]), round(lo["I_capt"][0], 1), round(cl["I_capt"][0], 1), "se", f3(se))
print("U_clos - hand_mass ceiling:", f3(K["U_clos_c1"]["ceiling_G"] - H["mass"]["ceiling_G"]))

print("\n== claim 7: max R2(objmass | Z) over learned configs")
best = sorted(learned, key=lambda c: -K[c]["agr"]["objmass"]["R2_H_from_Z"])[:5]
print([(c, round(K[c]["agr"]["objmass"]["R2_H_from_Z"], 4)) for c in best], "hand_mass", round(H["mass"]["agr"]["objmass"]["R2_H_from_Z"], 4),
      "hand_chan", round(H["chan"]["agr"]["objmass"]["R2_H_from_Z"], 4), "hand_view", round(H["view"]["agr"]["objmass"]["R2_H_from_Z"], 4))

print("\n== claim 8: max |seed diff| of G ceiling")
for sel, nm in ((lambda c: c.endswith("_c1") and ("_clos" in c or "_local" in c), "c1 clos/local (all arms incl. U, clos1/16)"),
                (lambda c: c.endswith("_c1") and ("_clos" in c or "_local" in c) and not c.startswith("U"), "c1 clos/local N+L"),
                (lambda c: ("_clos" in c or "_local" in c), "all widths clos/local")):
    cs = [c for c in learned if sel(c)]
    m = max(cs, key=lambda c: np.abs(K[c]["seed_diff"]).max())
    print(nm, len(cs), "configs: max", round(float(np.abs(K[m]["seed_diff"]).max()), 4), m)
sa = {c: C["configs"][c]["seed_agreement"]["mean"] for c in learned if "_recon_" in c and c.startswith("N")}
print("N recon seed R2 (from combined.json, latents not returned):", {c: round(v, 3) for c, v in sorted(sa.items())})

print("\n== windows: cos to block-mass window (raw units), own computation")
for c in ["L0_clos_c1", "L0_local_c1", "L0_recon_c1", "L8_clos_c1", "N0_clos_c1"]:
    v = []
    for p in sorted(glob.glob(f"{O}/windows/{c}_s*__fit*.npz")):
        d = np.load(p)
        W = d["W"].astype(float) / d["sd"].astype(float)[None, :, None, None]
        h = int(d["h"])
        m = np.zeros(W.shape[1:])
        m[:, h:h + 16, h:h + 16] = 1
        v.append(abs((W[0] * m).sum()) / (np.linalg.norm(W[0]) * np.linalg.norm(m)))
    print(c, len(v), np.round(v, 3).tolist(), "mean", round(float(np.mean(v)), 3))

def js(o):
    if isinstance(o, dict):
        return {k: js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, np.ndarray)):
        return [js(v) for v in (o.tolist() if isinstance(o, np.ndarray) else o)]
    if isinstance(o, (float, np.floating)):
        return round(float(o), 5) if np.isfinite(o) else None
    return o


outj = {"source": "origin/gpu-jobs:jobs/r4-bias-003/out (items/*.npz, cert/*.json, windows/*.npz)",
        "n_phi": R["n_phi"], "n_cert_files": R["n_cert_files"], "n_configs": R["n_configs"],
        "max_abs_dev_vs_combined_json": {k: f"{v:.2e}" for k, v in maxdev.items()},
        "configs": {c: {"ceiling_G": r["ceiling_G"], "ceiling_G_seed_diff": r["seed_diff"], "I_avail": r["I_avail"],
                        "I_capt": r["I_capt"], "participation_ratio": r["pr"], "agreement": r["agr"]} for c, r in K.items()},
        "hand": {k: {"ceiling_G": h["ceiling_G"], "I_avail": h["I_avail"], "I_capt": h["I_capt"], "participation_ratio": h["pr"],
                     "agreement": h["agr"]} for k, h in H.items()}}
json.dump(js(outj), open(sys.argv[3], "w"), indent=1)
