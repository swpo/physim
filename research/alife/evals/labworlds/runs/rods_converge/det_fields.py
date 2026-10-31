"""Per-field breakdown of the deterministic space screen (zero noise, dt arg, n = 128 / 192 / 256), readouts at
0, 1 and 5 tu: rms over slots of (difference / scale) for each field and group, against the noisy member spread of
that field (the same spread ensemble as det.py). Also body counts and areas (world units^2) at 5 tu."""
import copy, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from scipy import ndimage
import rc
from det import scales_from

dt = float(sys.argv[1]) if len(sys.argv) > 1 else 0.05
MARKS = [0.0, 1.0, 5.0]
z = np.load(rc.OUT / "spread_dt005.npz")
ens = {g: z[g] for g in rc.GROUPS}
sc = scales_from(ens)
R = {}
areas = {}
for n in (128, 192, 256):
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
        R[n, mk] = rc.readouts(np.stack([st[f] for f in rc.FIELDS]), devs, rc.L_BOX / n)
    lab, nb = ndimage.label(st["phi"] > 0)
    a = np.bincount(lab.ravel())[1:] * (rc.L_BOX / n) ** 2
    areas[n] = dict(n_components=int(nb), median_area_wu2=round(float(np.median(a[a >= 6])), 1),
                    phi_max=round(float(st["phi"].max()), 3), c_max=round(float(st["c"].max()), 3),
                    s_max=round(float(st["s"].max()), 3), cargo_total_wu2=round(float(st["c"].sum() * (rc.L_BOX / n) ** 2), 1))
rows = []
for mk in MARKS:
    ti = max(int(mk) - 1, 0)
    for g in rc.GROUPS:
        for i, f in enumerate(rc.FIELDS):
            X = ens[g][:, ti, i] / (sc[g][i] if g == "global" else sc[g][i])
            sp = np.mean([np.sqrt(((X[a] - X[b]) ** 2).mean()) for a in range(8) for b in range(8) if a != b])
            d = lambda n1, n2: float(np.sqrt((((R[n1, mk][g][i] - R[n2, mk][g][i]) / (sc[g][i])) ** 2).mean()))
            rows.append(dict(t=mk, group=g, field=f, spread_at_1tu_or_t=round(float(sp), 4),
                             r128_192=round(d(128, 192) / sp, 2), r192_256=round(d(192, 256) / sp, 2)))
res = dict(dt=dt, rows=rows, state_at_5tu=areas)
(rc.OUT / f"det_fields_dt{dt:g}.json").write_text(json.dumps(res, indent=1))
for r in rows:
    print(r)
print(json.dumps(areas, indent=1))
