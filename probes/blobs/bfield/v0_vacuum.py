"""v0_vacuum.py — vacuum exactness WITH b-dynamics on (all 3 sources).
No blob: u=v=w=u0, b=0. Sources must vanish on vacuum; b must stay 0, u stay u0.
Also: saw static field + dynamics: background must stay exact (isok exactness)."""
import sys, os, json
import numpy as np
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import sim

out = []
for src in ("s1", "s2", "s3"):
    r = sim.run(tau=5.7, gamma=0.03, tau_b=50.0, D_b=0.5, source=src,
                T=200.0, blobs=(), allow_empty=True, rec_tu=50.0, save_fields=True)
    u, v, w, bd = r["fields"]
    out.append(dict(source=src, max_dev_u=float(np.abs(u - r["u0"]).max()),
                    max_abs_b=float(np.abs(bd).max()), status=r["status"],
                    tu_per_s=round(r["tu_per_s"], 2)))
# with static saw too (machine C1 analogue, dynamics on)
r = sim.run(tau=5.7, gamma=0.03, tau_b=50.0, D_b=0.5, source="s2",
            eps=0.0005, kind="saw", frac=0.85, n_teeth=1,
            T=200.0, blobs=(), allow_empty=True, rec_tu=50.0, save_fields=True)
u, v, w, bd = r["fields"]
out.append(dict(source="s2+saw", max_dev_u=float(np.abs(u - r["u0"]).max()),
                max_abs_b=float(np.abs(bd).max()), status=r["status"]))
rec = dict(id="V0_vacuum_exact", kind="control_vacuum", detail=out,
           verdict="pass" if all(o["max_dev_u"] < 1e-10 and o["max_abs_b"] < 1e-10
                                 for o in out) else "FAIL")
sim.append_result(rec)
print(json.dumps(rec, indent=1))
