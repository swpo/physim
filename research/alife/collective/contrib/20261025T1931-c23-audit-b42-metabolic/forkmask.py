"""From the saved fed state, keep the substrate feed F(1-S) only OUTSIDE cells (mode=out: phi<1/2, the bodies must
import substrate by diffusion) or only INSIDE them (mode=in). Implemented by running the claimed step and removing the
feed term on the excluded pixels (feed used S before the step). Logs as fork.py."""
import sys, json, pickle, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife/collective/contrib/20261025T1931-c23-audit-b42-metabolic')
import world_audit as A
sys.path.insert(0, '/home/user/physim/research/alife/collective/contrib/20261025T1430-c14-pcell-mwall-b42-claim')
from genealogy import cells_of
st, mode, T, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
s = pickle.load(open(st, 'rb')); F = A.P['F']
rows, snaps = [], []
for k in range(T + 1):
    if k % 250 == 0:
        C = cells_of(s); ins = s['phi'] > 0.5
        rows.append(dict(t=int(s['t']), cells=len(C), N=int(len(s['py'])), S_in=float(s['S'][ins].mean()) if ins.any() else None,
                         S_out=float(s['S'][~ins].mean()), phi_area=int(ins.sum()), M=float(s['M'].sum()), ymean=float(s['y'].mean()) if len(s['y']) else None))
    if k in (0, 1000, 2500, 5000, T):
        snaps.append((int(s['t']), s['phi'].copy(), s['M'].copy(), s['S'].copy()))
    if k < T:
        S0 = s['S'].copy(); excl = (s['phi'] > 0.5) if mode == 'out' else (s['phi'] <= 0.5)
        s = A.Wm.step(s)
        s['S'] = np.maximum(s['S'] - F * (1 - S0) * excl, 0)
json.dump(rows, open(out + '.json', 'w')); pickle.dump(snaps, open(out + '_snaps.pkl', 'wb'))
print(json.dumps([(r['t'], r['cells'], r['N'], r['phi_area']) for r in rows[::4]]))
