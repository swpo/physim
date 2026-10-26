import json, sys, numpy as np
L = 5.0
print("run arm  window  speed  area  pol  s_rim/core  s_rim/out  cover  cargo_in/out  cargo_held")
for f in sys.argv[1:]:
    r = json.load(open(f)); print(f, "cut info:", {k: round(v, 3) if isinstance(v, float) else v for k, v in r["info"].items()})
    for k in ("cut", "twin"):
        t = np.array([a["t"] for a in r[k]]); c = np.array([[a["cx"], a["cy"]] for a in r[k]])
        d = (np.diff(c, axis=0) + L/2) % L - L/2; sp = np.hypot(*d.T) / np.diff(t)
        for a, b in ((8, 9), (9, 11), (11, 14), (14, 20)):
            m = (t > a) & (t <= b); m1 = m[1:]
            g = lambda key: np.mean([x[key] for x, mm in zip(r[k], m) if mm])
            print(f"  {k:4s} {a:2d}-{b:2d}  {sp[m1].mean():.3f}  {g('area'):.2f}  {g('pol'):.3f}  {g('rim_core'):.2f}  {g('rim_out'):.1f}  {g('cover'):.2f}  {g('cratio'):.1f}  {g('cheld'):.2f}")
