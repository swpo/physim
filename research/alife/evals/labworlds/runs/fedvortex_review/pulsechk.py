"""Reviewer check of one pulse case: om, amp 0.03, dur 20, at the negative body centre of the seed-0 t=500 state.
Regenerates the prepared state independently and compares it with the battery's prep_s0.npz."""
import importlib.util, json, os, sys, time
import numpy as np
from scipy import ndimage
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import ops
ops.WORKERS = 1
os.environ["WORLD_P"] = "{}"
sp = importlib.util.spec_from_file_location("w", "/home/user/physim/research/alife/collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py")
W = importlib.util.module_from_spec(sp); sp.loader.exec_module(W)
D = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/out/"
t0 = time.time()
s = W.init(0, (128, 128))
for i in range(25000): s = W.step(s)
z = np.load(D + "prep_s0.npz")
print("prep t", round(s["t"], 3), "max|dom| vs battery prep", float(np.abs(s["om"] - z["om"]).max()), "max|dY|", float(np.abs(s["Y"] - z["Y"]).max()), f"{time.time()-t0:.0f}s")
info = json.load(open(D + "prep_s0.json"))
cy, cx = info["sites"]["centre_n"]
H = Wd = 128
yy, xx = np.mgrid[0:H, 0:Wd]
dy = (yy - cy + 64) % 128 - 64; dx = (xx - cx + 64) % 128 - 64
bump = np.exp(-(dy ** 2 + dx ** 2) / 8.0)
def nbodies(om):
    m = np.abs(om) > 0.06
    lab, n = ndimage.label(np.tile(m, (3, 3)), structure=np.ones((3, 3)))
    k = 0
    for i, sl in enumerate(ndimage.find_objects(lab)):
        if 128 <= sl[0].start < 256 and 128 <= sl[1].start < 256 and (lab[sl] == i + 1).sum() >= 6:
            k += 1
    return k
mask0 = (s["om"] < -0.06) & (np.sqrt(dy ** 2 + dx ** 2) < 8)
print("target pixels", int(mask0.sum()), "bodies at prep", nbodies(s["om"]))
import copy
tw = copy.deepcopy(s); pu = copy.deepcopy(s); dt = s["par"]["dt"]
iy, ix = int(round(cy)) % 128, int(round(cx)) % 128
for k in range(1, 1001):            # 20 t
    pu["om"] = pu["om"] + 0.03 * dt * bump
    pu = W.step(pu); tw = W.step(tw)
    if k % 100 == 0:
        near = np.sqrt(dy ** 2 + dx ** 2) < 8
        negp = int(((pu["om"] < -0.06) & near).sum()); posp = int(((pu["om"] > 0.06) & near).sum())
        print(f"t={k*dt:.0f} site om {pu['om'][iy,ix]:+.3f} twin {tw['om'][iy,ix]:+.3f} | within 8px: neg px {negp} pos px {posp} (twin neg {int(((tw['om']<-0.06)&near).sum())}) | max|om| {np.abs(pu['om']).max():.3f} Y_site {pu['Y'][iy,ix]:.2f} | bodies {nbodies(pu['om'])}/{nbodies(tw['om'])}")
d = pu["om"] - tw["om"]; ch = np.abs(d) > 0.03; R = np.sqrt(dy ** 2 + dx ** 2)
print("t=20 changed px", int(ch.sum()), "max dist", float(R[ch].max()) if ch.any() else 0, f"total {time.time()-t0:.0f}s")
