"""stable -- the README tables of the round-5 study `slots`, printed from results/summary.json (local helper).

usage: python -B stable.py RESULTS_DIR
Every number printed here is read from summary.json (which carries the source of each row).
"""
import json
import os
import sys

R = sys.argv[1]
S = json.load(open(os.path.join(R, "summary.json")))
P, CF, OV = S["phis"], S["configs"], S["objective_values"]
HZ = S["meta"]["horizons"]
IH = [HZ.index(h) for h in (1, 4, 16)]


def f(x, n=2):
    return " - " if x is None else f"{x:.{n}f}"


def pick(v, idx=IH):
    return "-" if v is None else " / ".join(f(v[i]) for i in idx)


print("| view | objective | ARI | recall | precision | slots per object | slots present | mass R2 (mask / probe) | "
      "velocity R2 (probe) | ceiling S h=1/4/16 | predictable nats h=1/4/16 | seed ARI | closure value |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
# references
p = P["trk@mp6"]
print(f"| trk | (tracker) | 1 | 1 | 1 | 1 | - | 1 | 1 | {pick(p['ceiling'])} | {pick(p['I_capt_diag'])} | - | "
      f"{f(OV.get('trk', {}).get('set', {}).get('mean'))} |")
for nm in ("km_s3", "km_s6", "km_s6w", "grid"):
    if nm not in P:
        continue
    a, s = P[nm]["agreement"], P[nm + "@mp6"]
    print(f"| {nm} | (none) | {f(a['ari'])} | {f(a['recall'])} | {f(a['precision'])} | {f(a['slots_per_object'])} | "
          f"{f((P[nm].get('territory') or {}).get('slots_present_mean'), 1)} | {f(a['direct']['mass_R2'])} / {f(a['probe_rff']['mass_R2'])} | "
          f"{f(a['probe_rff']['vel_R2'])} | {pick(s['ceiling'])} | {pick(s['I_capt_diag'])} | - | "
          f"{f(OV.get(nm, {}).get('set', {}).get('mean'))} |")
for nm, c in CF.items():
    ph = c["phis"]
    pres = [(P[q].get("territory") or {}).get("slots_present_mean") for q in ph]
    pres = [x for x in pres if x is not None]
    tr = c.get("training") or {}
    cut = " (cut)" if tr.get("cut_by_deadline") else ""
    ceil = c.get("ceiling_mp6_S") or (c.get("ceiling") if c.get("ceiling_family") == "S" else None)
    icap = c.get("I_capt_diag_mp6_S")
    if icap is None and c.get("ceiling_family") == "S":
        import numpy as np
        icap = np.mean([P[q]["I_capt_diag"] for q in ph], 0).tolist()
    sp = (c.get("seed_pair") or {}).get("ari")
    print(f"| {nm}{cut} | {c['obj']} | {f(c['ari'])} | {f(c['recall'])} | {f(c['precision'])} | {f(c['slots_per_object'])} | "
          f"{f(sum(pres) / len(pres), 1) if pres else '-'} | {f(c['direct_mass_R2'])} / {f(c['probe_rff_mass_R2'])} | "
          f"{f(c['probe_rff_vel_R2'])} | {pick(ceil)} | {pick(icap)} | {f(sp)} | "
          f"{f(OV.get(nm, {}).get('set', {}).get('mean'))} |")
print()
print("| config | steps | checkpoint steps | tracker recall + purity on held-out trajectories, by step |")
print("|---|---|---|---|")
for nm, c in CF.items():
    tr = c.get("training")
    if not tr:
        continue
    rp = tr.get("val_tracker_recall_plus_purity_by_step") or {}
    txt = "; ".join(f"{k}: {sum(v) / len(v):.2f}" for k, v in rp.items())
    print(f"| {nm} | {tr['steps_done']} | {tr['best_step']} | {txt} |")
