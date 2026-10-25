"""Continue a saved fed state (t=60000) with the substrate feed cut (F=0) or kept, for T steps.
Logs cells (phi>0.5 components holding >= 20 particles, periodic), particles and totals every 250 steps,
and saves 6 snapshots of phi, M and particle positions."""
import sys, json, pickle, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife/collective/contrib/20261025T1931-c23-audit-b42-metabolic')
sys.path.insert(0, '/home/user/physim/research/alife')
import world_audit as A
sys.path.insert(0, '/home/user/physim/research/alife/collective/contrib/20261025T1430-c14-pcell-mwall-b42-claim')
from genealogy import cells_of
st, F, T, out = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
s = pickle.load(open(st, 'rb')); A.P['F'] = F
rows, snaps = [], []
for k in range(T + 1):
    if k % 250 == 0:
        C = cells_of(s)
        rows.append(dict(t=int(s['t']), cells=len(C), N=int(len(s['py'])), S=float(s['S'].mean()), L=float(s['L'].sum()), M=float(s['M'].sum()),
                         phi_area=int((s['phi'] > 0.5).sum())))
    if k in (0, 500, 1000, 2000, 4000, T):
        snaps.append((int(s['t']), s['phi'].copy(), s['M'].copy(), np.stack([s['py'], s['px']], 1).copy()))
    if k < T:
        s = A.Wm.step(s)
json.dump(rows, open(out + '.json', 'w'))
pickle.dump(snaps, open(out + '_snaps.pkl', 'wb'))
print(json.dumps([(r['t'], r['cells'], r['N']) for r in rows[::4]]))
