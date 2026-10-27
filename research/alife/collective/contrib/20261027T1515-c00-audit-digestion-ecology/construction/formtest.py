"""Do predators form from the t=2000 noise with NO digestion (k2 = 0 from t=2000, written taxis on)?
usage: formtest.py STATE_t2000.npz SEED OUT.json [T]   (state saved just before the predator noise is added)"""
import sys, os, json
sys.path.insert(0, '/home/user/physim/research/alife'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from arms import load, label_p
import world_dump as WD
w = WD.w
s = load(sys.argv[1], int(sys.argv[2])); s["par"]["k2"] = 0.0
T = float(sys.argv[4]) if len(sys.argv) > 4 else 2000.0; dt = s["par"]["dt"]; n = int(round(T / dt)); ev = int(round(100 / dt))
rows = []; snaps = []
for i in range(n + 1):
    if i % ev == 0:
        F = w.fields(s); La, na = label_p(F[0]); Lb, nb = label_p(F[1])
        rows.append(dict(t=s["t"], n_prey=na, n_pred=nb, max_cb=float(F[1].max()), q_max=float(F[4].max()),
                         pred_on_prey_frac=float(np.mean([(La[Lb == j] > 0).mean() for j in range(1, nb + 1)])) if nb else None))
        if i % (5 * ev) == 0: snaps.append(F[[0, 1]].astype(np.float32))
    if i < n: s = w.step(s)
json.dump(dict(rows=rows), open(sys.argv[3], "w"))
np.savez_compressed(sys.argv[3].replace(".json", "_snaps.npz"), snaps=np.array(snaps))
for r in rows[::4]: print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})
