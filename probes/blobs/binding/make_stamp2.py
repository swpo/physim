import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/binding")
from sim import relax_single
p = json.loads(sys.argv[1])
res = relax_single(L=64.0, dx=1.0, T=2000.0, **p)
assert res["status"] == "ok", res["status"]
np.savez_compressed(sys.argv[2], du=res["du"], dv=res["dv"], dw=res["dw"],
                    u0=res["u0"], thr=res["thr"], area_px=res["area_px"],
                    t_relax=(res["t_relax"] if res["t_relax"] is not None else -1))
print(json.dumps(dict(area=res["area_px"], peak=round(res["peak"],4), t_relax=res["t_relax"])))
