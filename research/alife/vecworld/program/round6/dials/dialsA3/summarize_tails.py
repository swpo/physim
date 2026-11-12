"""summarize_tails -- study dialsA3: results/summary.json from what survived job r6-dialsa3-001 (CPU, seconds).

The job was cut by the platform (infra_error, no output file collected; DEVIATIONS entry 2). What survives is the
runner's heartbeat tails of progress.txt in the committed versions of origin/gpu-jobs:jobs/r6-dialsa3-001/status.json,
reconstructed in results/job/progress_from_heartbeats.txt, and the final status.json. This script parses them:
- the job's own first look after N = 8 (a3_stats.first_look on the complete N = 8 scores of the 16 truths, which runs
  a3_stats.criteria: the declared verdict, its parts, sigma_G, rho_G, the zero-point pairs, H's recovery and t) and
  every policy's skill against K and O at eta 0 and 4 (3 decimals). The runner's scrubber replaced keys containing
  "@" by "<ssh-target>"; they are restored by position, since a3_stats.skills lists the policies in sorted order and
  the policies present after N = 8 are known (asserted against the keys that were not replaced);
- the presmoke's stop rule and speed guard, the truths, the law switch's zero point, family rates, base-net rungs,
  the nets' hash, the fine-tune picks' flags;
- ratios derived from the 3-decimal skills (labelled; skill = (L(K) - L) / (L(K) - L(O)) with means over truths,
  so a ratio of skill differences is the ratio of mean-L differences the criteria use, up to rounding).
Standard errors, bounds, medians and leave-one-truth-out ranges need the per-item scores, which were lost: they are
reported as lost, never estimated.

usage: python -B summarize_tails.py [--job results/job] [--out results/summary.json]
"""
from __future__ import annotations

import argparse
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--job", default=os.path.join(HERE, "results", "job"))
ap.add_argument("--out", default=os.path.join(HERE, "results", "summary.json"))
args = ap.parse_args()
JID = "r6-dialsa3-001"
PROG = os.path.join(args.job, "progress_from_heartbeats.txt")
SRC_P = f"{JID}: status.json heartbeat tails (results/job/progress_from_heartbeats.txt)"
lines = open(PROG).read().splitlines()
status = json.load(open(os.path.join(args.job, "status.json")))
REDACT = "<ssh-target>"


def find(pat, first=False):
    hits = [ln for ln in lines if re.search(pat, ln)]
    if not hits:
        return None
    return hits[0] if first else hits[-1]


def after(line, marker):
    return line[line.index(marker) + len(marker):]


def restore(pairs, expected):
    """pairs: [(key, value)] in the order printed (sorted names); expected: the names present. Returns a dict."""
    exp = sorted(expected)
    assert len(pairs) == len(exp), (len(pairs), exp)
    out = {}
    for (k, v), name in zip(pairs, exp):
        if k != REDACT:
            assert k == name, (k, name)
        else:
            assert "@" in name, name
        out[name] = v
    return out


def first_look(line, budgets=(8,)):
    js = after(line, ": ", ) if False else line[line.index("{"):]
    obj = json.loads(js, object_pairs_hook=lambda p: p)            # keep duplicate keys in order
    top = dict(obj)
    res = {}
    for k, v in obj:
        if k.startswith("eta") and isinstance(v, list):
            names = [kk for kk, _ in v]
            fixed = [kk for kk in names if kk != REDACT]
            n_red = names.count(REDACT)
            res[k] = (v, fixed, n_red)
    return top, res


def pairs_to_dict(p):
    return {k: (pairs_to_dict(v) if isinstance(v, list) and v and isinstance(v[0], tuple) else v) for k, v in p}


S = {"study": "round6/dials/dialsA3: the zero-point rerun of the reopened gliders exam (dialsA2)",
     "PILOT_NEVER_REUSE_AS_EXAM": True,
     "declared": "DECLARED.md (commit 3e9026c7b, 03:01 UTC 12 Nov 2026, before any code or request)",
     "how_this_file_was_made": "summarize_tails.py from results/job/progress_from_heartbeats.txt (the runner's heartbeat "
                               "tails in the 19 committed versions of origin/gpu-jobs:jobs/r6-dialsa3-001/status.json, "
                               "results/job/heartbeat_commits.txt) and results/job/status.json; the job's output files "
                               "were lost (DEVIATIONS entry 2)"}

# ---- job record
pods = status.get("pods") or []
p0 = pods[0] if pods else {}
S["job"] = {"id": JID, "source": f"{JID}: status.json [state], [message], [cost], [pods], [history]",
            "state": status.get("state"), "message": status.get("message"), "cost": status.get("cost"),
            "cap_usd": status.get("cap_usd"), "ref": (status.get("bundle") or {}).get("ref"),
            "pod": {k: p0.get(k) for k in ("provider", "gpu", "data_center", "rate_usd_hr", "created_at", "ready_at",
                                           "terminated_at", "billed_usd")},
            "history": status.get("history"), "review": (status.get("review") or {}).get("summary"),
            "outputs_collected": "none (manifest.json: files [], transfer 0 bytes)"}

# ---- presmoke
sr = find(r"presmoke stop rule")
m = re.search(r"r = ([-+.\d]+) \+- ([.\d]+) .* rung (\d+)\), threshold ([.\d]+) -> (\w+); by rung (\{.*\})", sr)
S["presmoke"] = {"source": SRC_P + " [presmoke stop rule line]",
                 "stop_rule": {"r_trueformC_minus_publicC_eta0": float(m.group(1)), "se": float(m.group(2)),
                               "read_at_rung": int(m.group(3)), "threshold": float(m.group(4)),
                               "decision": m.group(5), "by_rung": json.loads(m.group(6)),
                               "unit": "L(K) - L(public-form C), truth 0, score half, 3 seeds (DECLARED A3-4)"}}
gl = find(r"speed guard")
mg = re.search(r"required ([.\d]+) min, everything ([.\d]+) min, left ([.\d]+) min -> (\w+); estimates (\{.*\})", gl)
S["presmoke"]["speed_guard"] = {"required_min": float(mg.group(1)), "everything_min": float(mg.group(2)),
                                "left_min": float(mg.group(3)), "decision": mg.group(4),
                                "estimates_seconds": json.loads(mg.group(5)), "source": SRC_P + " [speed guard line]"}
zl = find(r'"max_abs_xw0_minus_gworld"')
S["presmoke"]["law_switch_zero_point"] = json.loads(zl[zl.index("{"):])
pl = find(r"first look final", first=True)
top, res = first_look(pl)
pre_sk = {}
for eta, (pairs, fixed, n_red) in res.items():
    exp = fixed + [n for n in ("Dnet@8", "Dridge@8", "FT@8", "H@8", "H_mix@8", "RES@8", "RESfix@8", "S@8", "Dnet@32",
                               "Dridge@32", "FT@32", "H@32", "H_mix@32", "RES@32", "RESfix@32", "S@32", "CFT@8",
                               "CFT_blind@8", "CFT@32", "CFT_blind@32")
                   if (eta == "eta4" or not n.startswith("CFT"))]
    if len(exp) != len(pairs):
        exp = exp[:len(pairs)]
    try:
        pre_sk[eta] = restore(pairs, exp)
    except AssertionError:
        pre_sk[eta] = {"raw": pairs}
S["presmoke"]["first_look_skill_vs_O_one_truth"] = {"source": SRC_P + " [presmoke 'first look final' line]",
                                                     "note": "presmoke sizes (192-point families, 6,000-step nets, "
                                                             "truth 0 only); not a result", **pre_sk}

# ---- what ran
tl = find(r"truths 0-15")
mt = re.search(r"truths 0-15: (\[\[.*\]\]) \((\d+)/(\d+) candidates viable, .*distance to dialsA2's truths and draws ([.\d]+)\)", tl)
fam = {}
for ln in lines:
    mf = re.search(r"family (\w+): (\d+) points x (\d+) episodes, (\d+)s, last chunk (\d+) member-ticks/s", ln)
    if mf and int(mf.group(2)) >= 768:
        fam[mf.group(1)] = {"points": int(mf.group(2)), "episodes_per_point": int(mf.group(3)),
                            "seconds": int(mf.group(4)), "member_ticks_per_s_last_chunk": int(mf.group(5))}
S["what_ran"] = {"source": SRC_P, "backend": "gpu (cuda:0), jax 0.12.0.1, x64 world, float32 nets",
                 "truths": json.loads(mt.group(1)), "truths_viable_of_candidates": [int(mt.group(2)), int(mt.group(3))],
                 "truths_min_maxabs_distance_to_dialsA2_truths_and_seed_6601_draws": float(mt.group(4)),
                 "families_full_pass": fam,
                 "member_ticks_planned_full_pass": int(re.search(r"member-ticks planned ([\d,]+)",
                                                                  find(r"16 truths x eta")).group(1).replace(",", "")),
                 "stages_done": "presmoke (all stages once), families, worlds (16 truths x eta 0, 4), inference, base "
                                "nets 24k-192k, N = 8 (FT, CFT, RES, S, H, H_mix, blind C), D(8)",
                 "stages_lost": "N = 32 (cut by the platform during its fine-tunes) and the eta 1 and 2 arm (never "
                                "started); every output file"}
nl = find(r"nets.npz sha256")
S["what_ran"]["nets_npz_sha256"] = nl.split("sha256 ")[1].strip() if nl else None

# ---- training
base = []
for ln in lines:
    mb = re.search(r"base (\d+): best steps (\[[\d, ]+\]) best val (\[[\d., ]+\]) rule met (\w+)", ln)
    if mb:
        base.append({"steps": int(mb.group(1)), "best_step": json.loads(mb.group(2)), "best_val": json.loads(mb.group(3)),
                     "rule_met": mb.group(4) == "True", "net_order": ["P0", "P1", "P2", "T0", "T1", "T2"]})
curve = []
for ln in lines:
    mc = re.search(r"net\[base (\d+)\] step (\d+)/\d+ train ([.\d]+) val (\[[^\]]+\])", ln)
    if mc:
        curve.append({"rung": int(mc.group(1)), "step": int(mc.group(2)), "train": float(mc.group(3)),
                      "val": [round(x, 4) for x in json.loads(mc.group(4))]})
ft = find(r"N=8: FT\|eta0")
S["training"] = {"source": SRC_P,
                 "base_rungs_surviving": base,
                 "base_rule": "unmet at every rung that survives; 24,000 and 48,000 rungs' best-step lines fell between "
                              "heartbeats, but the ladder went on to 96,000 and 192,000, so neither met the rule (R9); "
                              "at 192,000 (the declared maximum) the true-form nets' best steps exceed 153,600: "
                              "not converged by the rule (DEVIATIONS entry 3)",
                 "base_curve_points_surviving": curve,
                 "ft_N8_line": ft[ft.index("N=8:"):] if ft else None,
                 "D8": "1,200 steps, no doubling followed (the next stage was N = 32), so D(8) met the rule at 1,200"}

# ---- the job's first look after N = 8: the declared criteria
fl = find(r"first look after N=8")
top, res = first_look(fl)
EXP = {"eta0": ["Cpub", "Ctrue", "Ctrue_blind", "Dnet@8", "Dridge@8", "FT@8", "H@8", "H_mix@8", "K", "O", "P0", "RES@8",
                "RESfix@8", "S@8"],
       "eta4": ["CFT@8", "CFT_blind@8", "Cpub", "Ctrue", "Ctrue_blind", "Dnet@8", "Dridge@8", "FT@8", "H@8", "H_mix@8",
                "K", "O", "P0", "RES@8", "RESfix@8", "S@8"]}
sk = {eta: restore(res[eta][0], EXP[eta]) for eta in ("eta0", "eta4")}
topd = {k: (pairs_to_dict(v) if isinstance(v, list) else v) for k, v in top.items() if not k.startswith("eta")}
S["headline"] = {"source": SRC_P + " ['first look after N=8' line, written by a3_stats.first_look -> a3_stats.criteria "
                                   "on the complete N = 8 scores of 16 truths at eta 0 and 4]",
                 "verdict": topd["verdict"], "verdict_parts": topd["parts"], "T1_sigma_G": topd["sigma_G"],
                 "T2_rho_G": topd["rho_G"], "T3_H_recovery": topd.get("H_recovery"), "T3_t": topd.get("H_t"),
                 "zero_point": topd["zero_point"], "zero_point_tolerance": 0.02,
                 "zero_point_in_rule": ["trueformC_vs_publicC", "Gstar_vs_S", "H_vs_S"],
                 "lost": "SE, one-sided 90% bounds, medians over truths, leave-one-truth-out ranges, G* and C picks, "
                         "T4's and T5's numbers (their verdicts are in verdict_parts); per-item scores were not collected"}
S["skill_vs_O_N8"] = {"source": SRC_P + " ['first look after N=8' line; '<ssh-target>' keys restored by sorted order]",
                      "definition": "(L(K) - L) / (L(K) - L(O)), L mean over 16 truths, 3 seeds, `score` items, 8-16 ticks",
                      **sk}


# ---- derived from the 3-decimal skills (reported; not criteria; rounding error about 0.002 / denominator)
def r3(x):
    return round(x, 3)


e0, e4 = sk["eta0"], sk["eta4"]
Cp0 = e0["Cpub"]
C4 = max(e4["Ctrue"], e4["CFT@8"])
P4 = e4["P0"]
der = {"note": "derived here from 3-decimal skills; a ratio of skill differences equals the ratio of mean-L "
               "differences; C at eta 4 taken as the better of Ctrue and CFT@8 (the job picks per truth and seed on "
               "`sel`); reported, never criteria",
       "eta0_in_units_of_K_minus_publicC": {n: r3((Cp0 - e0[n]) / Cp0) for n in
                                            ("Ctrue", "P0", "S@8", "FT@8", "RES@8", "Dnet@8", "Dridge@8", "H@8",
                                             "H_mix@8", "Ctrue_blind")},
       "eta0_note": "each value is L(policy) - L(public-form C) over L(K) - L(public-form C); negative = better than "
                    "the public-form C",
       "eta4_s_P0_to_C_share_of_K_to_C": r3((C4 - P4) / C4),
       "eta4_recovery_of_P0_to_C": {n: r3((e4[n] - P4) / (C4 - P4)) for n in
                                    ("H@8", "H_mix@8", "RES@8", "RESfix@8", "FT@8", "S@8", "Cpub", "Dnet@8",
                                     "Dridge@8")},
       "eta4_T4_blind_loss_share_approx": r3((C4 - min(e4["Ctrue_blind"], e4["CFT_blind@8"])) / C4),
       "eta4_L_publicC_minus_L_trueform_net_in_K_minus_C": r3((e4["Ctrue"] - e4["Cpub"]) / C4),
       "eta0_skill_gap_trueform_minus_publicC_carried_to_eta4_reading": {
           "note": "a reading written after the results (untested): if the true-form net's eta-0 advantage over the "
                   "public-form net (a training-family effect, A3 README) carried to eta 4, a like-for-like C would "
                   "have skill C4 - (Ctrue0 - Cpub0); sigma_G and rho_G recomputed with it, G* approximated by RES@8 (skill 0.378; the job's sigma_G 0.337 implies a G* skill of 0.377)",
           "skill_C_like_for_like": r3(C4 - (e0["Ctrue"] - e0["Cpub"])),
           "sigma_G": r3((C4 - (e0["Ctrue"] - e0["Cpub"]) - e4["RES@8"]) / (C4 - (e0["Ctrue"] - e0["Cpub"]))),
           "rho_G": r3((e4["RES@8"] - P4) / (C4 - (e0["Ctrue"] - e0["Cpub"]) - P4))}}
S["derived_from_skills"] = der

# ---- dialsA2 beside
try:
    A2 = json.load(open(os.path.join(os.path.dirname(HERE), "dialsA2", "results", "summary.json")))
    h2 = A2["headline"]
    ck = A2.get("checker", {}).get("recomputation", {})
    S["dialsA2_quoted"] = {"source": "../dialsA2/results/summary.json [headline], [reported], [checker] (job r6-dialsa2-001)",
                           "verdict": h2["verdict"], "verdict_parts": h2["verdict_parts"],
                           "T1_sigma_G": h2["T1_sigma_G"]["value"], "T2_rho_G": h2["T2_rho_G"]["value"],
                           "T3_H_recovery": h2["T3_H_recovery"]["value"], "T3_t": h2["T3_t"],
                           "T4_blind_loss_share": h2["T4_blind_loss_share"]["value"],
                           "zero_point": {k: v.get("value") for k, v in h2["zero_point"].items() if isinstance(v, dict)},
                           "s_P0_to_C_eta4": A2["reported"]["s_P0_to_C_share_of_K_to_C_eta4"]["value"],
                           "skill_vs_O": A2["reported"]["skill_vs_oracle"],
                           "eta0_diagnosis_checker": ck.get("eta0_diagnosis_numbers"),
                           "presmoke_pair_at_500_steps": "+0.234 +- 0.034 (DECLARED.md header, computed from "
                                                         "r6-dialsa2-001 presmoke/scores.npz)"}
except Exception as exc:                                         # noqa: BLE001
    S["dialsA2_quoted"] = f"not available: {exc!r}"

os.makedirs(os.path.dirname(args.out), exist_ok=True)
with open(args.out, "w") as f:
    json.dump(S, f, indent=1)
print(json.dumps({"verdict": S["headline"]["verdict"], "parts": S["headline"]["verdict_parts"],
                  "zero_point": S["headline"]["zero_point"], "sigma_G": S["headline"]["T1_sigma_G"],
                  "rho_G": S["headline"]["T2_rho_G"], "derived": der["eta0_in_units_of_K_minus_publicC"]}))
