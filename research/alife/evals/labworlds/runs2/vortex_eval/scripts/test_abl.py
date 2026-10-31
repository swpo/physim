"""Base-equivalence of fv_ablations at defaults, then the rod's sham under candidate division controls."""
import dataclasses, json, sys, pickle
import numpy as np
sys.path.insert(0, "/home/user/evalwork/vortex_eval/scripts")
import common as C, design as D
from physim import labworld as LW
ABL = "/home/user/evalwork/vortex_eval/scripts/fv_ablations.py"
s = D.load_state(f"{C.OUT}/prep/state_s31_t580.pkl")
# 1) equivalence at defaults (noise-free, 200 steps)
wb = C.world(intensity=0.0, actuators=False); wa = dataclasses.replace(wb, path=ABL)
mb, ma = wb.load(), wa.load(); C.one_worker(mb); C.one_worker(ma)
sb = mb.init(0, (128, 128)); sa = ma.init(0, (128, 128))
for k in ("om", "Y", "t"):
    sb[k] = s[k]; sa[k] = s[k]
for _ in range(200):
    sb = mb.step(sb); sa = ma.step(sa)
print("defaults identical:", np.array_equal(sb["om"], sa["om"]) and np.array_equal(sb["Y"], sa["Y"]))
site = [91.4, 122.1]
variants = json.loads(sys.argv[1])
progs = {"sham": [], "feed_neck": [dict(t=0, kind="inject", device=0, port=2, amp=3.0, dur=20.0)]}
crops = {}
for name, ov in variants.items():
    w = dataclasses.replace(C.world(derived=D.DERIVED), path=ABL, overrides=ov)
    for pn, acts in progs.items():
        o = D.oracle(s, [D.device(0, site), D.device(1, [72, 40])], world=w)
        fr, res = D.capture(o, acts, seed=4300)
        hist, ev = D.follow(fr, site)
        lab, bs = D.bodies(fr[50.0][0])
        print(name, pn, "split", D.persistent_split(hist), "n", [h.get("n") for h in hist[::5]], "circ", [round(h.get("circ", 0), 1) for h in hist[::5]],
              "| box bodies t0/t50", len(D.bodies(fr[0.0][0])[1]), len(bs), "peak t50", round(float(np.abs(fr[50.0][0]).max()), 3), flush=True)
        iy = (np.arange(-24, 24) + 91) % 128; ix = (np.arange(-24, 24) + 122) % 128
        crops[f"{name}:{pn}"] = np.stack([fr[t][0][np.ix_(iy, ix)] for t in sorted(fr) if t % 5 == 0])
np.savez_compressed(f"{C.OUT}/mech/abl_{sys.argv[2]}.npz", **crops)
