"""Collect results/cert/*.json and results/train_info.json into results/summary.json, with paired
bootstrap differences (over the 36 trajectories) for the comparisons the report makes.

usage: python -B summarize.py
"""
import glob
import json
import os
import sys

sys.path.insert(0, "/home/user/evalwork/vecworld/program/track1/learned_phi2")
import numpy as np  # noqa: E402

import lphi as L  # noqa: E402
import run as R  # noqa: E402

CD = R.CERT_DIR
HZ = L.HZ


def load_items(name):
    out = {}
    for h, off in (("A", 0), ("B", L.NJ)):
        d = np.load(f"{CD}/{name}__cert{h}.npz")
        out[h] = {"err": {k[4:]: d[k].astype(np.float64) for k in d.files if k.startswith("err_")},
                  "orac": d["orac"], "ij": d["item_j"] + off}
    names = sorted(set(out["A"]["err"]) & set(out["B"]["err"]))
    return {"err": {nm: np.concatenate([out["A"]["err"][nm], out["B"]["err"][nm]]) for nm in names},
            "orac": np.concatenate([out["A"]["orac"], out["B"]["orac"]]),
            "ij": np.concatenate([out["A"]["ij"], out["B"]["ij"]])}


def fam_names(it, fam):
    G = [nm for nm in L.FAM_G if nm in it["err"]]
    if fam == "G":
        return G
    if fam == "GL":
        return G + ["lridge"] if "lridge" in it["err"] else None
    if fam == "L":
        return ["lridge"] if "lridge" in it["err"] else None
    if fam == "G+rmlp":
        return G + ["rmlp"] if "rmlp" in it["err"] else None


def ceil(it, names, idx):
    V0 = it["err"]["mean"][idx].mean(0)
    Vu = it["orac"][idx].mean(0)
    Vb = np.min(np.stack([it["err"][nm][idx].mean(0) for nm in names]), 0)
    return (V0 - Vb) / (V0 - Vu)


def paired(a, b, fam="G", n_boot=1000, seed=1):
    """c(a) - c(b) per horizon with a paired bootstrap SE over trajectories (same items)."""
    ia, ib = load_items(a), load_items(b)
    assert np.array_equal(ia["ij"], ib["ij"])
    na, nb = fam_names(ia, fam), fam_names(ib, fam)
    if na is None or nb is None:
        return None
    ij = ia["ij"]
    allx = np.arange(len(ij))
    d0 = ceil(ia, na, allx) - ceil(ib, nb, allx)
    rng = np.random.default_rng(seed)
    uj = np.unique(ij)
    pos = {u: np.flatnonzero(ij == u) for u in uj}
    ds = []
    for _ in range(n_boot):
        idx = np.concatenate([pos[u] for u in rng.choice(uj, uj.size, replace=True)])
        ds.append(ceil(ia, na, idx) - ceil(ib, nb, idx))
    se = np.std(ds, 0)
    return {"a": a, "b": b, "family": fam, "diff": d0, "se": se, "z": d0 / np.maximum(se, 1e-12)}


def r3(x):
    return None if x is None else np.round(np.asarray(x, float), 4).tolist()


def main():
    info = json.load(open(f"{L.RES}/train_info.json"))
    certs = {}
    for f in sorted(glob.glob(f"{CD}/*.json")):
        nm = os.path.basename(f)[:-5]
        certs[nm] = json.load(open(f))
    table = {}
    for nm, r in certs.items():
        row = {"q": r["q"], "c_G": r3(r["G"]["ceiling"]), "c_G_se": r3(r["G"]["se"]), "best_G": r["G"]["best"],
               "tau_half_G": r.get("tau_half_G")}
        if "GL" in r:
            row.update(c_GL=r3(r["GL"]["ceiling"]), c_GL_se=r3(r["GL"]["se"]), c_L=r3(r["L"]["ceiling"]),
                       best_GL=r["GL"]["best"], tau_half_GL=r.get("tau_half_GL"))
        if "G+rmlp" in r:
            row.update(c_Grmlp=r3(r["G+rmlp"]["ceiling"]), c_Grmlp_se=r3(r["G+rmlp"]["se"]), best_Grmlp=r["G+rmlp"]["best"])
        row["c_G_cert_on_A"], row["c_G_cert_on_B"] = r3(r["G_half_A_cert"]), r3(r["G_half_B_cert"])
        ld = r["logdet"]
        for k in ("I_capt", "I_avail", "c_info", "gapX", "gammaY", "inherit", "gapX_r2", "I_capt_local"):
            if k in ld:
                row[k] = r3(ld[k])
        row["I1_capt_nats"] = ld["I_capt"][0]          # None when a log-det is singular (exactly conserved direction)
        row["I1_capt_nats_per_dim"] = None if ld["I_capt"][0] is None else ld["I_capt"][0] / r["q"]
        pa, pb = r["per_half"]["A"], r["per_half"]["B"]
        for k in ("r_dyn", "participation_ratio", "R2_level1_from_z", "R2_pool3_from_z", "R2_z_from_pool3"):
            if k in pa:
                row[k] = round(0.5 * (pa[k] + pb[k]), 4)
        if "halo_window" in pa:
            row["halo_inner_power_share"] = round(0.5 * (pa["halo_window"]["inner_power_share"] + pb["halo_window"]["inner_power_share"]), 4)
        if "alignment" in pa:
            row["alignment"] = {k: round(0.5 * (pa["alignment"][k] + pb["alignment"][k]), 4) for k in pa["alignment"]}
            row["alignment_per_fit_half"] = {"fitB_certA": pa["alignment"], "fitA_certB": pb["alignment"]}
        tr = {h: info.get(f"{nm.replace('_rmlp', '')}__fit{h}") for h in ("A", "B")}
        if tr["A"] and "val_best" in tr["A"]:
            row["train"] = {h: {k: tr[h][k] for k in ("val_init", "val_best", "seconds", "min_rel_eig_latent_cov", "steps", "lr", "wd")}
                            for h in ("A", "B")}
        if tr["A"] and "eigenvalues" in tr["A"]:
            row["fit_eigenvalues"] = {h: r3(tr[h]["eigenvalues"]) for h in ("A", "B")}
        table[nm] = row

    comps = []

    def add(a, b, fam="G"):
        if a in certs and b in certs:
            p = paired(a, b, fam)
            if p is not None:
                comps.append({k: (r3(v) if isinstance(v, np.ndarray) else v) for k, v in p.items()})
    for c in (1, 2, 3):
        for fam in ("G", "GL"):
            for a in (f"LL_closG4_c{c}", f"LL_closL4_c{c}", f"LM_closG4_c{c}", f"LM_closL4_c{c}", f"LL_recon_c{c}",
                      f"LM_recon_c{c}", f"lpca{c}"):
                add(a, f"pool{c}", fam)
            add(f"LL_closL4_c{c}", f"LL_closG4_c{c}", fam)
            add(f"LM_closL4_c{c}", f"LM_closG4_c{c}", fam)
            add(f"LL_closG4_c{c}", f"LL_recon_c{c}", fam)
            add(f"LM_closL4_c{c}", f"LM_recon_c{c}", fam)
        add(f"GM_closG4_c{c}", f"LL_closG4_c{c}", "G")
        add(f"GL_closG4_c{c}", f"LL_closG4_c{c}", "G")
        add(f"GM_recon_c{c}", f"gpca{16 * c}", "G")
        add(f"gpca{16 * c}", f"pool{c}", "G")
    for fam in ("G", "GL"):
        add("LH_closG4_c1", "LL_closG4_c1", fam)
        add("LH_closG4_c1", "pool1", fam)
        add("LH_closG16_c1", "LL_closG16_c1", fam)
        add("LH_closG4_c3", "LL_closG4_c3", fam)
        add("LH_closG4_c1", "LH_recon_c1", fam)
        add("LH_closG4_c3", "LH_recon_c3", fam)
        add("pool3w", "pool3", fam)
        add("LH_closG4_c1", "tent1", fam)
        add("tent1", "pool1", fam)
        add("box4_1", "pool1", fam)
        add("tent1", "box4_1", fam)
        add("tent3", "pool3", fam)
        add("LH_closG4_c3", "pool3", fam)
        add("LH_closG4_c3", "tent3", fam)
        add("LH_recon_c1", "pool1", fam)
        add("tent1", "L1", fam)
        add("LH_closG4_c1", "L1", fam)
        add("LH_closG4_c3", "L1", fam)
        add("pool2w", "pool2", fam)
        add("LL_closG4_c3", "pool3w", fam)
        add("LM_closL4_c3", "pool3w", fam)
        add("LL_closG4_c2", "pool2w", fam)
        add("LM_closL4_c2", "pool2w", fam)
    add("GL_closG4_c1", "LH_closG4_c1", "G")
    add("GL_closG4_c1", "pool1", "G")
    for a, b in (("LM_closL4_c3", "LM_recon_c3"), ("LM_closL4_c1", "LM_recon_c1"), ("pool3", "L1"), ("LL_closG4_c3", "pool3"),
                 ("GL_closG4_c1", "pool1"), ("LH_closG4_c1", "pool1"), ("LH_closG4_c1", "tent1"), ("LH_closG4_c3", "pool3"),
                 ("tent1", "L1"), ("LH_closG4_c1", "L1")):
        add(a, b, "G+rmlp")
    for fam in ("G", "GL"):
        add("pmom3", "pool3", fam)
        add("LL_closG4_c3", "pmom3", fam)
        add("LM_closL4_c3", "pmom3", fam)
        for p in ("pool1", "pool2", "pool3", "pmom3", "LL_closG4_c3", "LM_closL4_c3", "LL_closG4_c1", "LL_recon_c3"):
            add(p, "L1", fam)
    # closure-versus-content Pareto front (content = linear R^2 of the level-1 frame from z, in-sample)
    def front(key, hi=3):
        pts = [(nm, r["R2_level1_from_z"], r[key][hi]) for nm, r in table.items()
               if key in r and r[key] is not None and not nm.endswith("_rmlp") and nm != "L1"]
        nd = [p for p in pts if not any((o[1] >= p[1] and o[2] >= p[2]) and (o[1] > p[1] or o[2] > p[2]) for o in pts)]
        return sorted([{"name": n, "R2_level1": round(x, 4), "c": round(y, 4)} for n, x, y in nd], key=lambda d: d["R2_level1"])
    pareto = {"G_tau8": front("c_G"), "GL_tau8_grid_only": front("c_GL"), "G_tau4": front("c_G", 2)}
    summary = {
        "what": "E1 on real nonlinear data (no new simulation): learned level-2 coarse-grainings Phi2 of the gliders "
                "block view (8 x 8 x 3 level-1 grid) under reconstruction, closure (global or local head) and "
                "predictive-IB objectives, against block pooling and PCA; certified with one fixed predictor family",
        "data": {"source": ["/home/user/evalwork/vecworld/vw1/fresh/closure/results/sim_A.npz",
                            "/home/user/evalwork/vecworld/vw1/fresh/closure/results/sim_B.npz"],
                 "trajectories": 36, "ticks": 301, "test_states": 144, "replicates_R": 6, "horizons": HZ,
                 "cross_fitting": "Phi2 fitted on one file's 18 base trajectories (15 train / 3 early-stopping), "
                                  "certified on the other file's 72 test states; halves pooled"},
        "families": {"G": L.FAM_G, "L": ["lridge (3x3 neighbourhood, 2 lags, shared weights)"],
                     "GL": "G + lridge (grid latents only)", "G+rmlp": "G + fresh residual MLP (1 seed), subset only"},
        "ceiling_definition": "c = (V0 - V_best)/(V0 - V_oracle), per-coordinate standardised MSE, V_oracle from the 6 replicates "
                              "(closure_lib.closure_ext with horizons 1..16, mlp off)",
        "table": table,
        "paired_differences": comps,
        "pareto_closure_vs_content": pareto,
    }
    json.dump(L.jsonable(summary), open(f"{L.RES}/summary_raw.json", "w"), indent=1)
    print("wrote", f"{L.RES}/summary_raw.json", len(table), "Phi2,", len(comps), "comparisons")


if __name__ == "__main__":
    main()
