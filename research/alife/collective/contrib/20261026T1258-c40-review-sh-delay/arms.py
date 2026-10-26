import os, sys, json, importlib.util, numpy as np
from scipy import ndimage as ndi
out = []
for kap, tau in [(0.3, 5), (0.15, 10), (0.6, 5), (1.0, 5), (0.3, 20), (1.5, 10), (0.6, 20), (1.0, 20)]:
    for v0 in (1, 0):
        wp = dict(N=128, L=80, r=-0.4, b=2, PYR=1, INIT="spot", kap=kap, tau=tau, V0=v0)
        os.environ["WORLD_P"] = json.dumps(wp)
        spec = importlib.util.spec_from_file_location("w", "world_v0.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
        s = w.init(3, w.META["size"])
        for _ in range(5000): s = w.step(s)
        n = ndi.label(ndi.gaussian_filter(s["u"], 1.5) > 0.4)[1]
        out.append({"kap": kap, "tau": tau, "kap_tau": kap * tau, "v_start": "0" if v0 else "u", "spots_t500": int(n), "umax": round(float(s["u"].max()), 3)})
        print(out[-1], flush=True)
json.dump(out, open("arms_v0_vs_vu.json", "w"), indent=0)
