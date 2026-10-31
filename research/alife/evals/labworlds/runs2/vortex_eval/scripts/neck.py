import json, sys, numpy as np
sys.path.insert(0, "/home/user/evalwork/vortex_eval/scripts")
import common as C, design as D
T = int(sys.argv[1]); near = [float(x) for x in sys.argv[2].split(",")]
s = D.load_state(f"{C.OUT}/prep/state_s31_t{T}.pkl")
lab, bs = D.bodies(s["om"])
b = min(bs, key=lambda q: np.hypot(D.wrap(q["cy"] - near[0]), D.wrap(q["cx"] - near[1])))
m = lab == b["label"]; yy, xx = np.indices((128, 128))
dy = D.wrap(yy[m] + 0.5 - b["cy"]); dx = D.wrap(xx[m] + 0.5 - b["cx"]); w = np.abs(s["om"][m])
ev, evec = np.linalg.eigh(np.cov(np.stack([dy, dx]), aweights=w)); ax = evec[:, 1]
proj = dy * ax[0] + dx * ax[1]
bins = np.arange(np.floor(proj.min()), np.ceil(proj.max()) + 1, 1.0)
prof = np.array([w[(proj >= a) & (proj < a + 1)].max() if ((proj >= a) & (proj < a + 1)).any() else 0 for a in bins[:-1]])
print("body", {k: round(v, 2) if isinstance(v, float) else v for k, v in b.items()}, "axis", ax.round(3), "aspect", round(float(np.sqrt(ev[1] / ev[0])), 2))
print("profile (max |om| per 1-unit slice along the axis):")
print(" ".join(f"{a:+.0f}:{p:.3f}" for a, p in zip(bins[:-1], prof)))
