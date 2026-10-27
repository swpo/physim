"""Do the brief deep stalls in rod speed coincide with axial heading reversals? Split-born rods, 10 t window speed,
25 t window axial velocity for reversals (dead band +-0.003 L/t, as axial.py). Dip = local minimum of speed below DIP.
Reports the fraction of dips with a reversal within +-K frames, against random frames of the same rods.
usage: dips.py rods.json [...]"""
import sys, json
import numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/paperexp/marangoni-bistability")
import states as S
FT = 2.5; DIP = 0.002; K = 4; rng = np.random.default_rng(3)
hit = n = 0; rhit = rn = 0; ndip_time = 0; T = 0
for p in sys.argv[1:]:
    d = json.load(open(p))
    for t in d["tracks"]:
        if t["birth"] != "split" or t["n"] < 30: continue
        y = np.array(t["y"]); x = np.array(t["x"]); L = np.median(t["L4"]); ax = np.array(t["ax"], float); nn = t["n"]
        for k in range(1, nn):
            if ax[k] @ ax[k - 1] < 0: ax[k] = -ax[k]
        k2 = np.arange(2, nn - 2); sp = np.hypot(y[k2 + 2] - y[k2 - 2], x[k2 + 2] - x[k2 - 2]) / (4 * FT) / L
        k5 = np.arange(5, nn - 5); u = ((y[k5 + 5] - y[k5 - 5]) * ax[k5, 0] + (x[k5 + 5] - x[k5 - 5]) * ax[k5, 1]) / (10 * FT) / L
        st = S.schmitt(u, -0.003, 0.003); rev = set((k5[np.nonzero(np.diff(st))[0]]).tolist())
        mins = [k2[i] for i in range(1, len(sp) - 1) if sp[i] < DIP and sp[i] <= sp[i - 1] and sp[i] <= sp[i + 1]]
        for m in mins:
            if 5 + K <= m <= nn - 6 - K:
                n += 1; hit += any(abs(m - r) <= K for r in rev)
        for m in rng.integers(5 + K, nn - 5 - K, size=max(1, len(mins))):
            rn += 1; rhit += any(abs(m - r) <= K for r in rev)
        ndip_time += len(mins); T += nn * FT
print(f"dips (local minima < {DIP} L/t): {n}; with an axial reversal within +-{K * FT:g} t: {hit / max(n, 1):.2f}; random frames: {rhit / max(rn, 1):.2f} (n {rn}); dips per rod per 100 t {100 * ndip_time / T:.2f}")
