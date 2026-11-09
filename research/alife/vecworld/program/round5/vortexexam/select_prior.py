"""select_prior -- read results/analysis1.json (job 1), pick the hidden parameters and write prior.json (public).

Selection rule (written before job 1 returned):
  eligible   a candidate whose two box edges are viable for every scanned member (finite fields, no tracker
             overflow, 3 <= N <= K - 1 from tick 20 on).
  families   selection {eps}; mutation {mut128}; fuel {kF, e, kY}; flow {nu, adv}; growth {k, mu, wi};
             label {kl, dl, Dl}. Within a family the eligible member with the largest level-2 headroom
             (min over the two edges of the mean theta-plug-in deficit over h = 8, 16, 32 ticks).
  chosen     eps (the study's question: the selection coefficient), then the two other families with the largest
             such headroom: d = 3 hidden parameters (the design is 192-384 theta points). If eps is not eligible
             over [0, 0.4] its box is narrowed by hand and the reason is recorded.
  prior      uniform on the scanned box of each chosen parameter, conditioned on the public viability rule
             (estimated in job 2 from the design episodes as p_v(theta)).
The exam shape (episode length, program ticks, horizons) and the public scaling constants are set here from job 1's
law runs: sc_N, sc_s = standard deviations of N and s_b over members and ticks >= 100 at eps = 0.2; history-channel
centres and scales = means and standard deviations over the scan's null members (ticks >= 100).
usage: python -B select_prior.py JOB1_OUT_DIR [--H 64] [--names a,b,c] [--why "..."]
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402

import vxlib as VX  # noqa: E402

FAMILY = {"eps": "selection", "mut128": "mutation", "kF": "fuel", "e": "fuel", "kY": "fuel", "nu": "flow", "adv": "flow",
          "k": "growth", "mu": "growth", "wi": "growth", "kl": "label", "dl": "label", "Dl": "label"}
SHAPE = {64: dict(T_ep=284, prog_ticks=[100, 150, 200, 250]), 96: dict(T_ep=344, prog_ticks=[120, 180, 240, 300]),
         128: dict(T_ep=404, prog_ticks=[130, 210, 290, 370])}

ap = argparse.ArgumentParser()
ap.add_argument("job_out")
ap.add_argument("--H", type=int, default=0)
ap.add_argument("--names", default="")
ap.add_argument("--why", default="")
ap.add_argument("--n-min", type=float, default=3.0)
args = ap.parse_args()
A = json.load(open(os.path.join(HERE, "results", "analysis1.json")))
scan = A["scan"]
H = args.H or scan["H"]
table = scan["table"]
best = {}
for p, t in table.items():
    f = FAMILY[p]
    if not t["viable_both"]:
        continue
    if f not in best or t["L2_min_edge"] > table[best[f]]["L2_min_edge"]:
        best[f] = p
rule = sorted([p for f, p in best.items() if f != "selection"], key=lambda p: -table[p]["L2_min_edge"])[:2]
chosen = (["eps"] if "eps" in table else []) + rule
manual = False
if args.names:
    chosen, manual = args.names.split(","), True
box = {p: table[p]["box"] for p in chosen}

# public constants from job 1
Z = np.load(os.path.join(args.job_out, "scan_main.npz"))
S = Z["S"].astype(float)[0]                                   # null members (J, T, 12)
ix = {n: i for i, n in enumerate(VX.S1_NAMES)}
cen, scl = {}, {}
for k in ("N", "s_b", "fb_mass", "fb_mean", "fb_sd", "mixed", "log_mass_tot", "log_mass_mean", "speed_mean", "turnover"):
    v = S[:, 99:, ix[k]]
    cen[k] = round(float(v.mean()), 3)
    scl[k] = round(float(max(v.std(), 0.05)), 3)
law = np.load(os.path.join(args.job_out, "law.npz"))
e02 = int(np.argmin(np.abs(law["eps"] - 0.2)))
Sl = law["S"].astype(float)[e02]
sc_N = round(float(Sl[:, 99:, ix["N"]].std()), 3)
sc_s = round(float(max(Sl[:, 99:, ix["s_b"]].std(), 0.05)), 3)
N_ref = round(float(Sl[:, 99:, ix["N"]].mean()), 2)
out = {"PILOT_NEVER_REUSE_AS_EXAM": True, "H": H, "names": chosen, "lo": [box[p][0] for p in chosen],
       "hi": [box[p][1] for p in chosen], "c_prog": 200.0, "hs": [8, 16, 32], **SHAPE[H],
       "viability": {"n_min": args.n_min, "t_from": 20,
                     "rule": "fields finite, no tracker overflow, n_min <= N <= K - 1 at every state from t_from on"},
       "const": {"centre": cen, "scale": scl, "sc_N": sc_N, "sc_s": sc_s, "N_ref": N_ref},
       "selection": {"rule_choice": (["eps"] if "eps" in table else []) + rule, "manual_override": manual, "why": args.why,
                     "family_best": best,
                     "headroom_L2_min_edge": {p: table[p]["L2_min_edge"] for p in table},
                     "headroom_L1_mean_edges": {p: table[p]["L1_mean_edges"] for p in table},
                     "viable_both": {p: table[p]["viable_both"] for p in table},
                     "scan_H": scan["H"], "source": "results/analysis1.json scan.table (job r5-vortexexam-002)"},
       "mutation": "mut128 = time between mutation events per 128 x 128 px of box (declared per unit area); "
                   f"at {H} x {H} px the interval is mut128 x {VX.area_factor(H, H):g}",
       "program_mix": {"classes": list(VX.PROGRAM_CLASSES), "nats": 200.0, "u_max": VX.U_MAX,
                       "doc": "vxlib.make_program"}}
json.dump(out, open(os.path.join(HERE, "prior.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
