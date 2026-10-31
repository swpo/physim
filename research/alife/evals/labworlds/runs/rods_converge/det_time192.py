"""Deterministic dt screen at 192^2 (zero noise, dt 0.05 vs 0.025, readouts at 1, 2, 5, 10 tu), distances against the
member spread of the 192^2 native sham ensemble (dt 0.05, seed 606) at the same times, with the same scales as
det.py (spread_dt005, 128^2) so the ratios are comparable with det_time.json."""
import copy, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import rc
from det import scales_from, rms

MARKS = [1.0, 2.0, 5.0, 10.0]
n = 192
z = np.load(rc.OUT / "spread_dt005.npz")
sc = scales_from({g: z[g] for g in rc.GROUPS})
e = np.load(rc.OUT / "ens_sham_dt0.05_n192_s606.npz")
R = {}
for dt in (0.05, 0.025):
    s, info = rc.prepared(n=n, dt=dt)
    devs = rc.devices(info)
    m = rc.world(dt=dt, n=n, noise=0.0).load()
    st = copy.deepcopy(s)
    per_tu = int(round(2.5 / dt))
    done = 0
    for mk in MARKS:
        k = int(round(mk * per_tu))
        for _ in range(k - done):
            st = m.step(st)
        done = k
        R[dt, mk] = rc.readouts(np.stack([st[f] for f in rc.FIELDS]), devs, rc.L_BOX / n)
rows = []
for mk in MARKS:
    for g in rc.GROUPS:
        X = e[g][:, int(mk) - 1]
        sp = np.mean([rms(X[i], X[j], g, sc) for i in range(8) for j in range(8) if i != j])
        d = rms(R[0.05, mk][g], R[0.025, mk][g], g, sc)
        rows.append(dict(t=mk, group=g, spread192=round(float(sp), 4), ratio_dt005_vs_dt0025=round(d / sp, 3)))
(rc.OUT / "det_time_n192.json").write_text(json.dumps(rows, indent=1))
for r in rows:
    print(r)
