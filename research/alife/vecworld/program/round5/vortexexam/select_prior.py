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
What happened (10 Nov): job 1's branch file (the truths and controls behind the plug-in deficit) held the level-1
rasters and, at 40 MB, stayed on the runner (20 MB git limit per file), so the rule's headroom was not available
when the prior had to be fixed. The same rule is applied to a PROXY from the scan's main runs: for each edge, the
largest |z| of the paired shift (12 members, keys shared with the null setting) of the level-2 trajectory statistics
N (ticks 100-400), s_b early (ticks 100-250) and s_b late (ticks 250-400); headroom proxy = min over the two edges.
The plug-in deficits are recomputed inside job 2 (job1.py --scan-only, compact outputs) and reported next to this
choice. Two further departures, both decided before job 2 ran and recorded in prior.json: d = 4 instead of 3 (job 1
measured 444 member-ticks/s at 128^2, so the design is 768-1024 theta points, not 192-384), and the fourth parameter
is the mutation interval mut128 rather than the next family by the proxy (growth, k): the study's question is the
level-2 law, whose two constants are set by selection (eps) and mutation (mut128).
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
Jm = scan["J"]
if "table" in scan:
    table = scan["table"]
    key, basis = "L2_min_edge", "plug-in deficit (scan branches)"
else:                                             # proxy from the main runs (module docstring)
    table = {}
    for p, bx in scan["box"].items():
        zz = []
        for edge in ("lo", "hi"):
            sh = scan["shift"][f"{p}@{edge}"]
            zz.append(max(abs(sh[k]["z_paired"]) for k in ("N", "s_b_early", "s_b_late")))
        table[p] = {"box": bx, "proxy_lo": zz[0], "proxy_hi": zz[1], "proxy_min_edge": min(zz),
                    "viable_both": all(scan["viability"][f"{p}@{e}"]["viable_members"] == Jm for e in ("lo", "hi"))}
    key, basis = "proxy_min_edge", "proxy: max |paired z| of N, s_b early, s_b late over the main runs (no branches)"
best = {}
for p, t in table.items():
    f = FAMILY[p]
    if not t["viable_both"]:
        continue
    if f not in best or t[key] > table[best[f]][key]:
        best[f] = p
ranked = sorted([p for f, p in best.items() if f != "selection"], key=lambda p: -table[p][key])
rule = ranked[:2]
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
    tt = np.arange(99, S.shape[1])
    v = S[:, tt[tt % 40 != 0] if k == "turnover" else tt, ix[k]]     # turnover: 0 at job 1's chunk starts, dropped
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
       "selection": {"rule_choice_d3": (["eps"] if "eps" in table else []) + rule, "ranked_other_families": ranked,
                     "basis": basis, "manual_override": manual, "why": args.why, "family_best": best,
                     "headroom": {p: round(table[p][key], 3) for p in table},
                     "viable_both": {p: table[p]["viable_both"] for p in table},
                     "scan_H": scan["H"], "scan_J": Jm,
                     "source": "results/analysis1.json scan (job r5-vortexexam-002, scan_main.npz)"},
       "mutation": "mut128 = time between mutation events per 128 x 128 px of box (declared per unit area); "
                   f"at {H} x {H} px the interval is mut128 x {VX.area_factor(H, H):g}",
       "program_mix": {"classes": list(VX.PROGRAM_CLASSES), "nats": 200.0, "u_max": VX.U_MAX,
                       "doc": "vxlib.make_program"}}
json.dump(out, open(os.path.join(HERE, "prior.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
