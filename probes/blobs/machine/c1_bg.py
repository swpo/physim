"""C1: isok-mode background exactness — no-blob saw world must stay at u0."""
import sys, os, json
import numpy as np
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import sim

out = []
for eps in (0.005, 0.01):
    r = sim.run(tau=5.7, eps=eps, kind="saw", frac=0.85, n_teeth=1,
                T=300.0, blobs=[], allow_empty=True, rec_tu=50.0,
                save_fields=True)
    u, v, w = r["fields"]
    dev = float(np.max(np.abs(u - r["u0"])))
    out.append(dict(eps=eps, max_dev_u=dev, status=r["status"]))
    print("eps", eps, "max|u-u0| =", dev)

rec = dict(id="C1_bg_exact", kind="control_bg", detail=out,
           verdict="pass" if all(o["max_dev_u"] < 1e-9 for o in out) else "FAIL")
sim.append_result(rec)
print(json.dumps(rec["verdict"]))
