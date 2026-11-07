"""Drift of candidate invariants over short free runs of the collective worlds (numpy, as claimed, no added noise).

fed vortices: mean omega (circulation density), sum |omega|; CIPS: int e at turnover d=0.003 and d=0;
phase membrane: int phi, int (S+K+L); rods: mean phi. Writes invariants.json.
"""
import importlib.util
import json
import os
import sys

import numpy as np

LAB = "/home/user/physim/research/alife"
C = LAB + "/collective/contrib"
sys.path.insert(0, LAB)
OUT = "/home/user/evalwork/vecworld/program/inventory/invariants.json"


def load(tag, path, wp=None):
    os.environ["WORLD_P"] = json.dumps(wp or {})
    spec = importlib.util.spec_from_file_location("w_" + tag, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    if hasattr(m, "ops"):
        m.ops.WORKERS = 1
    return m


def run(m, n, probes, seed=0):
    s = m.init(seed, tuple(m.META["size"]))
    rec = {k: [float(f(s))] for k, f in probes.items()}
    for i in range(n):
        s = m.step(s)
        if (i + 1) % (n // 4) == 0:
            for k, f in probes.items():
                rec[k].append(float(f(s)))
    return rec


res = {}
v = load("v", C + "/20261027T0845-c53-fed-vortex-selection-claim/world.py", {"eps": 0.2, "mut_dt": 50.0})
res["fed_vortex (4000 steps = 80 t)"] = run(v, 4000, {"mean_omega": lambda s: s["om"].mean(),
                                                      "sum_abs_omega": lambda s: np.abs(s["om"]).sum(),
                                                      "sum_Y": lambda s: s["Y"].sum()})
cp = "/home/user/swpo/residency-environments/scripts/physim/labworlds/worlds/cips_iso.py"
for d in (0.003, 0.0):
    c = load("c%g" % d, cp, {"d": d})
    res[f"cips d={d} (1000 steps = 100 t)"] = run(c, 1000, {"int_e": lambda s: s["e"].sum(), "int_F": lambda s: s["F"].sum()})
pm = load("pm", LAB + "/threads/autopoiesis/worlds/phase_membrane/world.py")
res["phase_membrane (800 steps = 800 t)"] = run(pm, 800, {"int_phi": lambda s: s["phi"].sum(),
                                                          "int_SKL": lambda s: (s["S"] + s["K"] + s["L"]).sum()})
r = load("r", C + "/20261026T0505-c34-nematic-marangoni/world.py")
res["rods (400 steps = 20 t)"] = run(r, 400, {"mean_phi": lambda s: s["phi"].mean(), "sum_c": lambda s: s["c"].sum()})
for k, v_ in res.items():
    print(k, {kk: [round(x, 6) for x in vv] for kk, vv in v_.items()})
json.dump(res, open(OUT, "w"), indent=1)
