"""binterp -- the hand-written reading of r4-bias-003 as claims, every number pulled from combined.json (study `bias`).

usage: python -B binterp.py RESULTS_DIR   -> RESULTS_DIR/interpretation.json (then bsummary.py folds it into summary.json)
Each claim: text, the numbers it rests on, and their sources (job:file:key path). Horizon index i of a 5-vector
is h = (1, 2, 4, 8, 16)[i]. Ceiling = learned_phi2's closure ceiling, family G, (V_mean - V_best) / (V_mean - V_oracle).
"""
import json
import os
import sys

R = sys.argv[1]
JOB = "r4-bias-003"
C = json.load(open(os.path.join(R, "combined.json")))
HZ = C["horizons"]
claims = []


def cfg(nm, *path):
    v = C["configs"][nm]
    for p in path:
        v = v[p]
    return v, f"{JOB}:out/combined.json:configs.{nm}." + ".".join(str(p) for p in path)


def hand(k, *path):
    v = C["hand"][k]
    for p in path:
        v = v[p]
    return v, f"{JOB}:out/combined.json:hand.{k}." + ".".join(str(p) for p in path)


def rd(v, n=3):
    return [round(float(x), n) for x in v] if isinstance(v, (list, tuple)) else round(float(v), n)


def claim(text, items):
    claims.append({"claim": text, "values": {k: rd(v[0]) for k, v in items.items()},
                   "sources": {k: v[1] for k, v in items.items()}})


A = lambda nm, k, d: cfg(nm, "agreement", k, d)
claim("With a block-only receptive field (h = 0), closure and the local-law objective rediscover block mass on their "
      "own: the learned c = 1 latent and block mass predict each other with cross-validated R^2 >= 0.93 both ways, "
      "identically across seeds (seed R^2 >= 0.997).",
      {f"{nm}.{k}": A(nm, "mass", k) for nm in ("N0_clos_c1", "L0_clos_c1", "N0_local_c1", "L0_local_c1")
       for k in ("R2_H_from_Z", "R2_Z_from_H")} |
      {f"{nm}.seed_R2": cfg(nm, "seed_agreement", "mean") for nm in ("N0_clos_c1", "L0_clos_c1", "N0_local_c1", "L0_local_c1")})
claim("Reconstruction with the nonlinear local encoder does not: at h = 0 it learns a seed-dependent feature that is "
      "not mass and is barely predictable (ceiling at h = 4 of 0.09 vs 0.77 for block mass); the linear (L) and the "
      "unconstrained (U) autoencoders at c = 1 do land on block mass (first principal component of block content).",
      {"N0_recon_c1.R2_mass_from_Z": A("N0_recon_c1", "mass", "R2_H_from_Z"),
       "N0_recon_c1.seed_R2": cfg("N0_recon_c1", "seed_agreement", "mean"),
       "N0_recon_c1.ceiling_G": cfg("N0_recon_c1", "ceiling_G"), "hand_mass.ceiling_G": hand("mass", "G", "ceiling"),
       "L0_recon_c1.R2_mass_from_Z": A("L0_recon_c1", "mass", "R2_H_from_Z"),
       "U_recon_c1.R2_mass_from_Z": A("U_recon_c1", "mass", "R2_H_from_Z")})
claim("With a halo the closure latent becomes a low-pass filtered mass field: it stays a function of block mass "
      "(R^2(Z | mass) 0.88-0.98) but block mass is no longer recoverable from it (R^2(mass | Z) falls 0.93 -> 0.61), "
      "it agrees best with the designed tent at h = 4-8 (R^2 0.93-0.97 both ways), its closure ceiling at h = 16 "
      "rises 0.16 -> 0.27 -> 0.38 -> 0.55 with halo 0, 4, 8, 16 px, while its effective dimension (participation "
      "ratio) falls 44 -> 13 and its predictable content (I_avail at h = 1) falls 214 -> 174 nats.",
      {f"{nm}.{q}": v for nm in ("N0_clos_c1", "N4_clos_c1", "N8_clos_c1", "N16_clos_c1") for q, v in (
          ("R2_Z_from_mass", A(nm, "mass", "R2_Z_from_H")), ("R2_mass_from_Z", A(nm, "mass", "R2_H_from_Z")),
          ("R2_tent_from_Z", A(nm, "tent", "R2_H_from_Z")), ("R2_Z_from_tent", A(nm, "tent", "R2_Z_from_H")),
          ("ceiling_G", cfg(nm, "ceiling_G")), ("participation_ratio", cfg(nm, "nontriv", "participation_ratio")),
          ("I_avail", cfg(nm, "I_avail")))})
claim("The hand designs keep the most predictable content per number: block mass I_avail / I_capt at h = 1 = 275 / 165 "
      "nats vs at most 266 / 163 for any learned c = 1 latent (L4_local; N arm best N0_local 246 / 146); block channel "
      "means (c = 2) 432 / 246 vs at most 404 (U_local) / 227 (N4_local) for learned c = 2 latents. Higher learned "
      "closure ceilings are bought by smoothing.",
      {"hand_mass.I_avail": hand("mass", "logdet", "I_avail"), "hand_mass.I_capt": hand("mass", "logdet", "I_capt"),
       "hand_chan.I_avail": hand("chan", "logdet", "I_avail"), "hand_chan.I_capt": hand("chan", "logdet", "I_capt"),
       "hand_mass.participation_ratio": hand("mass", "nontriv", "participation_ratio"),
       "N0_local_c1.I_avail": cfg("N0_local_c1", "I_avail"), "N0_local_c1.I_capt": cfg("N0_local_c1", "I_capt"),
       "N4_local_c2.I_avail": cfg("N4_local_c2", "I_avail"), "N4_local_c2.I_capt": cfg("N4_local_c2", "I_capt"),
       "L4_local_c1.I_avail": cfg("L4_local_c1", "I_avail"), "L4_local_c1.I_capt": cfg("L4_local_c1", "I_capt"),
       "U_local_c2.I_avail": cfg("U_local_c2", "I_avail")})
claim("A shared local rule (local law) is at least as good a bias as the global closure head at every receptive field: "
      "higher captured predictive information at h = 1 and equal or higher ceilings, and closer to block mass.",
      {f"{nm}.{q}": v for nm in ("N0_clos_c1", "N0_local_c1", "N4_clos_c1", "N4_local_c1", "N16_clos_c1", "N16_local_c1")
       for q, v in (("I_capt", cfg(nm, "I_capt")), ("ceiling_G", cfg(nm, "ceiling_G")),
                    ("R2_mass_from_Z", A(nm, "mass", "R2_H_from_Z")))})
claim("Locality is what lets closure find mass: the unconstrained encoder trained for closure is less closed than block "
      "mass at every horizon, agrees with it poorly and is seed-unstable.",
      {"U_clos_c1.ceiling_G": cfg("U_clos_c1", "ceiling_G"), "hand_mass.ceiling_G": hand("mass", "G", "ceiling"),
       "U_clos_c1.R2_mass_from_Z": A("U_clos_c1", "mass", "R2_H_from_Z"),
       "U_clos_c1.seed_R2": cfg("U_clos_c1", "seed_agreement", "mean")})
claim("The predictive bottleneck lands in between: partly mass, less closed than block mass beyond h = 2.",
      {f"{nm}.{q}": v for nm in ("N0_pib_c1", "N16_pib_c1") for q, v in (
          ("ceiling_G", cfg(nm, "ceiling_G")), ("R2_mass_from_Z", A(nm, "mass", "R2_H_from_Z")),
          ("seed_R2", cfg(nm, "seed_agreement", "mean")))})
claim("Extra width (c = 2, 4) adds content that is less closed: the mass is still contained (R^2(mass | Z) >= 0.93 "
      "for N0 closure) but most of the latent is not mass, the second channel is not the per-channel block mass "
      "(R^2(Z | channel means) 0.51 for N0_clos_c2), and the h = 16 ceiling falls with width.",
      {f"{nm}.{q}": v for nm in ("N0_clos_c1", "N0_clos_c2", "N0_clos_c4") for q, v in (
          ("ceiling_G", cfg(nm, "ceiling_G")), ("R2_mass_from_Z", A(nm, "mass", "R2_H_from_Z")),
          ("R2_Z_from_mass", A(nm, "mass", "R2_Z_from_H")), ("R2_Z_from_chan", A(nm, "chan", "R2_Z_from_H")))})
om = {nm: r["agreement"]["objmass"]["R2_H_from_Z"] for nm, r in C["configs"].items() if "objmass" in r["agreement"]}
best = max(om, key=om.get)
claim("No bias at c <= 4 finds the object view: the best learned latent explains the object mass field no better "
      "than block mass does.",
      {f"{best}.R2_objmass_from_Z": A(best, "objmass", "R2_H_from_Z"),
       "hand_mass.R2_objmass_from_Z": hand("mass", "agreement", "objmass", "R2_H_from_Z")})
claim("Closure-type latents are seed-stable and so are their ceilings (largest seed difference of the G ceiling over "
      "all c = 1 closure/local configs and horizons is 0.014); nonlinear reconstruction is not (seed R^2 0.08-0.87).",
      {"max_abs_seed_diff_clos_local_c1": (max(abs(x) for nm, r in C["configs"].items()
                                               if r["c"] == 1 and r["obj"] in ("clos", "local") for x in r["ceiling_G_seed_diff"]),
                                           f"{JOB}:out/combined.json:configs.*_(clos|local)_c1.ceiling_G_seed_diff"),
       "N4_recon_c1.seed_R2": cfg("N4_recon_c1", "seed_agreement", "mean"),
       "N8_recon_c1.seed_R2": cfg("N8_recon_c1", "seed_agreement", "mean")})
claims.append({"claim": "Cost of the study (billed): r4-bias-001 $0.81 (cancelled), r4-bias-002 $1.13 (cancelled), "
                        "r4-bias-003 $6.01 (done); pod hours 0.396 + 0.447 + 1.951 = 2.79.",
               "values": {"r4-bias-001": 0.8082, "r4-bias-002": 1.1261, "r4-bias-003": 6.0058, "total": 7.9401,
                          "pod_hours": [0.396, 0.447, 1.951]},
               "sources": {"billed": "origin/gpu-jobs:jobs/<job_id>/status.json:cost.billed_usd",
                           "pod_hours": "origin/gpu-jobs:LEDGER.md (pod hours column)"}})
json.dump(claims, open(os.path.join(R, "interpretation.json"), "w"), indent=1)
print(len(claims), "claims")
for c in claims:
    print("-", c["claim"][:100])
