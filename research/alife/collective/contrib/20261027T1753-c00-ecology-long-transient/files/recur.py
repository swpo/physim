"""c00: translation-invariant recurrence test for regular (periodic, locked or rigidly translating) late dynamics.
For render frames (400 t apart), descriptor = Fourier amplitudes |FFT| of the prey and predator fields (mean removed;
invariant to translation). D(t, t') = || A_t - A_t' || / || A_t ||, both kinds stacked.
Rmin(t) = min over earlier frames t' with 800 <= t - t' <= 24000 of D(t, t'). A regular state (rigid translation,
periodic orbit, pulsing lattice) returns close to an earlier frame, so Rmin is small; an irregular churn does not.
Reported: median Rmin over each 6000-t window (from t=8000, so 24000 t of history is not required early on), and
t_regular = start of the first window after which every window's median Rmin stays below THR to the end.
usage: recur.py <pack> [...]   (writes <pack>/recur.json)"""
import sys, json, numpy as np
THR = 0.2
def desc(F):
    v = []
    for ch in (0, 1):
        x = F[ch].astype(np.float64); x = x - x.mean(); v.append(np.abs(np.fft.rfft2(x)).ravel())
    return np.concatenate(v)
for pk in sys.argv[1:]:
    pk = pk.rstrip('/')
    z = np.load(f"{pk}/frames.npz"); R = z["render"]; rf = z["render_f"] * 100.0
    A = np.stack([desc(F) for F in R]); nA = np.linalg.norm(A, axis=1) + 1e-12
    rows = []
    for k in range(len(rf)):
        if rf[k] < 8000: continue
        js = [j for j in range(k) if 800 <= rf[k] - rf[j] <= 24000 and rf[j] >= 3000]
        if not js: continue
        d = np.linalg.norm(A[js] - A[k], axis=1) / nA[k]
        j = int(np.argmin(d)); rows.append({"t": float(rf[k]), "Rmin": round(float(d[j]), 4), "lag": float(rf[k] - rf[js[j]])})
    t = np.array([r["t"] for r in rows]); Rm = np.array([r["Rmin"] for r in rows])
    wins = {}
    for t0 in range(6000, 48000, 6000):
        s = (t >= t0) & (t < t0 + 6000) if t0 + 6000 < 48000 else (t >= t0) & (t <= 48000)
        if s.any(): wins[t0] = round(float(np.median(Rm[s])), 4)
    keys = sorted(wins); treg = None
    for i, k0 in enumerate(keys):
        if all(wins[k] < THR for k in keys[i:]): treg = float(max(k0, 8000)); break
    late = t > 36000
    out = {"pack": pk, "thr": THR, "Rmin_median_by_window": wins, "t_regular": treg,
           "Rmin_median_last_12000": round(float(np.median(Rm[late])), 4),
           "lag_median_last_12000": float(np.median([r["lag"] for r in rows if r["t"] > 36000])), "rows": rows}
    json.dump(out, open(f"{pk}/recur.json", "w"))
    print(pk.split('/')[-1], "Rmin by window", list(wins.values()), "t_regular", treg, "lag~", out["lag_median_last_12000"])
