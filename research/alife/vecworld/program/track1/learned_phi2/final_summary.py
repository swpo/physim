"""Write results/summary.json: run metadata, every number the report claims (each with its source), the
full certification table, the paired differences and the Pareto front (from summarize.py's output).

usage: python -B summarize.py && python -B final_summary.py
"""
import json
import os

OUT = "/home/user/evalwork/vecworld/program/track1/learned_phi2"
RAW = f"{OUT}/results/summary_raw.json"
s = json.load(open(RAW))
T = s["table"]
C = {(c["a"], c["b"], c["family"]): c for c in s["paired_differences"]}
HZ = s["data"]["horizons"]
H8 = HZ.index(8)
H16 = HZ.index(16)
H4 = HZ.index(4)
claims = []


def src(name):
    return f"{OUT}/results/cert/{name}.json"


def cl(cid, statement, value, source, se=None):
    claims.append({"id": cid, "statement": statement, "value": value, "se": se, "source": source})


def ceil(name, fam="c_G"):
    return T[name][fam]


# 1. reference ceilings
for nm in ("L1", "pool1", "pool2", "pool3", "tent1", "tent3", "box4_1", "pmom3", "LL_closG4_c1", "LL_closG4_c3",
           "LM_closL4_c3", "LH_closG4_c1", "LH_closG4_c3", "GL_closG4_c1", "GM_closG4_c3", "LM_recon_c1", "LM_recon_c3",
           "LL_recon_c3", "lpca1", "lpca3", "pool3w", "LL_pib4_c3", "LM_pib4_c3", "GM_pib4_c3", "GL_pib4_c3"):
    cl(f"ceiling_G.{nm}", f"closure ceiling c(tau), tau = {HZ}, fixed global family G, Phi2 = {nm}",
       ceil(nm), src(nm), T[nm]["c_G_se"])
    if "c_GL" in T[nm]:
        cl(f"ceiling_GL.{nm}", f"closure ceiling with the local ridge added (family GL), Phi2 = {nm}", ceil(nm, "c_GL"), src(nm),
           T[nm]["c_GL_se"])
    cl(f"content.{nm}", "linear R^2 of the level-1 frame from z; participation ratio; within-trajectory variance fraction",
       {"R2_level1_from_z": T[nm]["R2_level1_from_z"], "participation_ratio": T[nm]["participation_ratio"],
        "r_dyn": T[nm]["r_dyn"]}, src(nm))
for nm in ("L1", "pool3", "tent1", "LH_closG4_c1"):
    cl(f"tau_half.{nm}", "first horizon with c_G < 0.5 (log interpolation; null = not below 0.5 by 16)", T[nm]["tau_half_G"], src(nm))

# 2. paired differences used in the report
for key in [("LL_closG4_c1", "pool1", "G"), ("LM_closG4_c1", "pool1", "G"), ("LL_recon_c1", "pool1", "G"),
            ("lpca1", "pool1", "G"), ("LL_closL4_c1", "LL_closG4_c1", "G"), ("LL_closL4_c3", "LL_closG4_c3", "G"),
            ("LM_closL4_c3", "LM_closG4_c3", "G"), ("LM_closL4_c2", "LM_closG4_c2", "G"), ("LL_closG4_c3", "pool3", "G"),
            ("LL_closG4_c3", "pool3w", "G"), ("LM_closL4_c3", "pool3w", "G"), ("pool3w", "pool3", "G"),
            ("LL_closG4_c2", "LL_recon_c2", "G"), ("LL_closG4_c3", "LL_recon_c3", "G"), ("LM_closL4_c3", "LM_recon_c3", "G"),
            ("LM_closL4_c1", "LM_recon_c1", "G"),
            ("LH_closG4_c1", "pool1", "G"), ("LH_closG4_c1", "tent1", "G"), ("tent1", "pool1", "G"), ("box4_1", "pool1", "G"),
            ("tent1", "box4_1", "G"), ("LH_closG4_c1", "LH_recon_c1", "G"), ("LH_closG4_c3", "pool3", "G"),
            ("LH_closG4_c3", "LH_recon_c3", "G"), ("GL_closG4_c1", "pool1", "G"), ("GL_closG4_c1", "LH_closG4_c1", "G"),
            ("GM_closG4_c3", "LL_closG4_c3", "G"), ("pool3", "L1", "G"), ("tent1", "L1", "G"), ("LH_closG4_c1", "L1", "G"),
            ("LL_closG4_c3", "L1", "G"), ("pool3", "L1", "GL"), ("tent1", "L1", "GL"),
            ("LH_closG4_c1", "pool1", "G+rmlp"), ("LM_closL4_c3", "LM_recon_c3", "G+rmlp")]:
    c = C.get(key)
    if c is not None:
        cl(f"diff.{key[0]}-{key[1]}.{key[2]}", f"c({key[0]}) - c({key[1]}) per horizon {HZ}, family {key[2]}, paired bootstrap "
           "over 36 trajectories (1000 resamples)", c["diff"], f"{OUT}/results/cert/{key[0]}__cert[AB].npz, {key[1]}__cert[AB].npz",
           c["se"])

# 3. local-head versus global-head: largest |difference| at tau <= 16 over all widths and both encoders
mx = 0.0
for k, c in C.items():
    if k[2] == "G" and "closL4" in k[0] and "closG4" in k[1]:
        mx = max(mx, max(abs(x) for x in c["diff"]))
cl("closL_vs_closG.max_abs_diff", "largest |c(closL) - c(closG)| over c = 1, 2, 3, LL and LM, tau 1..16 (family G)", mx,
   f"{OUT}/results/summary.json:paired_differences")

# 4. local ridge versus global family: GL - G at tau = 8 for every grid latent
gain = {nm: round(r["c_GL"][H8] - r["c_G"][H8], 4) for nm, r in T.items() if r.get("c_GL") and not nm.endswith("_rmlp")}
cl("local_predictor_gain_tau8", "c_GL(8) - c_G(8): what the fixed local ridge adds over the global family, per grid latent",
   {"min": min(gain.values()), "max": max(gain.values()), "L1": gain["L1"], "pool3": gain["pool3"], "tent1": gain["tent1"],
    "n_negative": sum(v < 0 for v in gain.values()), "n": len(gain)}, f"{OUT}/results/summary.json:table")

# 5. alignments of local linear encoders to reference subspaces (mean of the two fits)
for nm in ("LL_closG1_c1", "LL_closG4_c1", "LL_closG16_c1", "LL_closG1_c3", "LL_closG4_c3", "LL_closG16_c3", "LL_recon_c1",
           "LL_recon_c3", "lpca1", "lpca3", "ltica1_1", "LL_closL4_c3", "rand_s3_0", "rand_p1_0"):
    cl(f"alignment.{nm}", "span alignment tr(Pi_W Pi_P)/c of the 12 x c window to P3 (pooling), P1 (total mass), Pmom9 "
       "(zeroth + first moments of each channel), Pmm3 (zeroth + first moments of total mass), lpca_same_c",
       T[nm]["alignment"], src(nm))
for nm in ("LH_closG4_c1", "LH_closG16_c1", "LH_recon_c1", "LH_closG4_c3"):
    cl(f"halo_inner_share.{nm}", "share of the squared window weight on the inner 2 x 2 blocks of the 4 x 4 halo window "
       "(tent [.5,1,1,.5]^2: 0.64; uniform 4 x 4: 0.25; no halo: 1)", T[nm].get("halo_inner_power_share"), src(nm))

# 6. stack: Prop. 6 split (Gaussian proxies, nats, total over the latent)
for nm in ("pool3", "tent1", "LL_closG4_c3", "LH_closG4_c1", "LH_closG4_c3", "pmom3"):
    cl(f"prop6.{nm}", "gammaY = Gamma_Y(Z) proxy (level-1 past beyond level-2 past), inherit = I(x; z_t+h | y_<=t), "
       "gapX_r2 = gammaY + inherit (ridge_p2 base); nats per horizon", {k: T[nm].get(k) for k in ("gammaY", "inherit", "gapX_r2")},
       src(nm))

# 7. training diagnostics
mins = {nm: min(r["train"][h]["min_rel_eig_latent_cov"] for h in ("A", "B")) for nm, r in T.items() if "train" in r}
cl("collapse_check.min_rel_eig", "smallest eigenvalue / mean eigenvalue of the raw latent covariance over every learned Phi2 "
   "(collapse would give ~0)", min(mins.values()), f"{OUT}/results/train_info.json")
cl("closure_val_loss_c3", "best validation closure loss (whitened latent, tau* = 4) per fit half: GM vs GL vs LL vs LM",
   {nm: [T[nm]["train"][h]["val_best"] for h in ("A", "B")] for nm in ("GM_closG4_c3", "GL_closG4_c3", "LL_closG4_c3", "LM_closL4_c3")},
   f"{OUT}/results/train_info.json; {OUT}/logs/run_all.log")

meta = {
    "what": s["what"], "data": s["data"], "families": s["families"], "ceiling_definition": s["ceiling_definition"],
    "sizes": {"phi2_certified": len([k for k in T if not k.endswith("_rmlp")]), "phi2_with_rmlp": len([k for k in T if k.endswith("_rmlp")]),
              "learned_encoders_trained": 2 * len([k for k in T if "train" in T[k] and not k.endswith("_rmlp")]),
              "train_pairs_per_fit": "15 trajectories x 296-300 ticks (about 4.4k); 3 trajectories for early stopping",
              "steps": {"LL": 5000, "LH": 5000, "LM": 2000, "GM": 2000, "GL": 2000}, "batch": 256,
              "seeds": "one seed (0) per encoder and fit half; the two fit halves are independent fits"},
    "cpu": {"main_run_cpu_s": 2404, "extra_run1_cpu_s_approx": 490, "extra_run2_cpu_s": 292, "pilots_cpu_s_approx": 720,
            "total_cpu_h_approx": round((2404 + 490 + 292 + 720) / 3600, 2), "core": 2, "threads": 1,
            "sources": [f"{OUT}/logs/run_all.log", f"{OUT}/logs/run_extra.log", f"{OUT}/logs/run_extra2.log"]},
    "logdet_caveat": "Gaussian log-det measures (I_capt, I_avail, c_info, gapX) are dominated by exactly conserved directions "
                     "(total mass) for every mass-pooling Phi2 and are singular (null) for box4_1; treat them as secondary",
}
out = {"meta": meta, "claims": claims, "table": T, "paired_differences": s["paired_differences"],
       "pareto_closure_vs_content": s["pareto_closure_vs_content"]}
json.dump(out, open(f"{OUT}/results/summary.json", "w"), indent=1)
os.remove(RAW)
print("wrote", f"{OUT}/results/summary.json", len(claims), "claims")
