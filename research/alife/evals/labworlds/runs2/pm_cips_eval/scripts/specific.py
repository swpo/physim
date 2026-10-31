"""Item 3 from the suite ensembles: for each mechanism ablation and each case it ran on, (a) the score ratio to
independent_native per sensor (from scores.json), and (b) the program-specific response difference
  RMS over nodes and score times of ((abl_prog - abl_sham) - (nat_prog - nat_sham)) / native spread,
with ensemble means (natives: independent_native + band_native (if any) + truths) and the native spread
(across-member sd of the sham natives), per sensor and field. Also the native response itself (nat_prog - nat_sham)."""
import sys, json, numpy as np
from pathlib import Path
OUT = Path("/home/user/evalwork/pm_cips_eval")
world = sys.argv[1]
d = OUT / f"suite_{world}"
suite = json.loads((d / "suite.json").read_text())
fields = suite["declaration"]["fields"]
TIMES = [0, 2, 5, 8, 10, 12, 15, 20, 22, 25, 30, 35, 40, 45, 50]
ti = [TIMES.index(t) for t in [2, 5, 8, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50]]
fam = {c["request"]["id"]: c["family"] for c in suite["cases"]}
cid = {v: k for k, v in fam.items()}


def load(p):
    with np.load(p) as z:
        return [z[f"query{i}"] for i in range(3)]


def natives(c):
    xs = [load(d / "controls" / c / "independent_native.npz"), load(d / "truth" / f"{c}.npz")]
    if (d / "controls" / c / "band_native.npz").exists():
        xs.append(load(d / "controls" / c / "band_native.npz"))
    return [np.concatenate([x[q] for x in xs]) for q in range(3)]


sham = cid["sham"]
nat_sham = natives(sham)
spread = [nat_sham[q][:, ti].std(axis=0, ddof=1) for q in range(3)]           # (t, ports, slots)
sp = {(q, p): float(np.sqrt((spread[q][:, p] ** 2).mean())) + 1e-15 for q in range(3) for p in range(len(fields))}
S = {c: json.loads((d / "controls" / c / "scores.json").read_text()) for c in fam if (d / "controls" / c / "scores.json").exists()}
res = {}
for k in suite["controls"]:
    if not k.startswith("ablate_"):
        continue
    ab_sham_p = d / "controls" / sham / f"{k}.npz"
    for c, f in fam.items():
        p = d / "controls" / c / f"{k}.npz"
        if not p.exists() or c not in S or k not in S[c]:
            continue
        g = {x["id"]: x["energy_score"] for x in S[c][k]["joint_energy"]}
        g0 = {x["id"]: x["energy_score"] for x in S[c]["independent_native"]["joint_energy"]}
        sens = {s: round(float(np.mean([g[x] for x in g if x.startswith(s + "/")]) / np.mean([g0[x] for x in g0 if x.startswith(s + "/")])), 2)
                for s in ("device0", "device1", "global")}
        row = dict(program=f, score_ratio=round(S[c][k]["joint_energy_equal_group_mean"] / S[c]["independent_native"]["joint_energy_equal_group_mean"], 2),
                   score_ratio_by_sensor=sens)
        if f != "sham" and ab_sham_p.exists():
            A, As, N = load(p), load(ab_sham_p), natives(c)
            spec, resp = {}, {}
            for q, s in enumerate(("device0", "device1", "global")):
                dif = (A[q][:, ti].mean(0) - As[q][:, ti].mean(0)) - (N[q][:, ti].mean(0) - nat_sham[q][:, ti].mean(0))
                nr = N[q][:, ti].mean(0) - nat_sham[q][:, ti].mean(0)
                spec[s] = {fl: round(float(np.sqrt((dif[:, i] ** 2).mean()) / sp[(q, i)]), 1) for i, fl in enumerate(fields)}
                resp[s] = {fl: round(float(np.sqrt((nr[:, i] ** 2).mean()) / sp[(q, i)]), 1) for i, fl in enumerate(fields)}
            row["response_difference_sd"] = spec
            row["native_response_sd"] = resp
        res[f"{k}:{f}"] = row
(d / "specificity.json").write_text(json.dumps(res, indent=1))
for k, r in res.items():
    line = f"{k:28s} ratio {r['score_ratio']:8.2f}  d0/d1/gl {r['score_ratio_by_sensor']['device0']:.2f}/{r['score_ratio_by_sensor']['device1']:.2f}/{r['score_ratio_by_sensor']['global']:.2f}"
    if "response_difference_sd" in r:
        line += "  resp.diff max d0/d1/gl " + "/".join(f"{max(r['response_difference_sd'][s].values()):.1f}" for s in ("device0", "device1", "global"))
        line += "  native resp max " + "/".join(f"{max(r['native_response_sd'][s].values()):.1f}" for s in ("device0", "device1", "global"))
    print(line)
