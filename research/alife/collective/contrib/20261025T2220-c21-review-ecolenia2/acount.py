"""(c21) Species cell counts from labkit metrics (species n_comp series; frame = 2 t): first time A reaches 20
cells, A mean over t=100-400, B mean over t>=300. usage: acount.py metrics.json [...]"""
import sys, json, numpy as np
for fn in sys.argv[1:]:
    m = json.load(open(fn)); su = m["summary"]; dtf = su["time"] / (su["frames"] - 1)
    a = np.array(m["species"]["A"]["n_comp"]); b = np.array(m["species"]["B"]["n_comp"]); t = np.arange(len(a)) * dtf
    t20 = t[np.argmax(a >= 20)] if (a >= 20).any() else None
    print(f"{fn}: A reaches 20 cells at t={t20}; A mean t=100-400 {a[(t >= 100) & (t <= 400)].mean():.1f}; A at t=600 {a[int(600 / dtf)]}; B mean t>=300 {b[t >= 300].mean():.1f}")
