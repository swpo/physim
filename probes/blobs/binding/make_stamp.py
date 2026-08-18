import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/binding")
from sim import relax_single

WPs = {
 "D_64": dict(Dv=6.0, tau=4.0, k3=1.5, k4=1.0),
 "C_46": dict(Dv=4.0, tau=6.0, k3=1.5, k4=1.0),
 "B_66": dict(Dv=6.0, tau=6.0, k3=1.5, k4=1.0),
 "M0":   dict(Dv=1.0, tau=3.0, k3=1.0, k4=1.5),
}
name = sys.argv[1]
res = relax_single(L=64.0, dx=1.0, T=2000.0, **WPs[name])
if res["status"] != "ok":
    print(json.dumps(dict(name=name, status=res["status"]))); sys.exit()
np.savez_compressed(f"/tmp/stamp_{name}.npz", du=res["du"], dv=res["dv"], dw=res["dw"],
                    u0=res["u0"], thr=res["thr"], area_px=res["area_px"],
                    t_relax=res["t_relax"] if res["t_relax"] is not None else -1)
print(json.dumps(dict(name=name, status="ok", area=res["area_px"],
                      peak=round(res["peak"],3), t_relax=res["t_relax"])))
