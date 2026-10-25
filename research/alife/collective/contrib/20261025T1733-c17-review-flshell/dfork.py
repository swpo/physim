"""starve-one-daughter fork in fl_shell (gamma 0) / fl_forager. usage: dfork.py seed T_fork T_after out [CUT]
Runs from noise to T_fork, finds the closest pair of bodies (a fresh division, both >= 40% of the larger), then runs
two branches for T_after: fed twin, and food set to 0 (moved elsewhere, ledger kept) in a disk of r=RAD around the
starved daughter, re-centred on it every step. Records per-sample mass of both daughters (tracked by nearest centroid)."""
import sys, os, json, copy, numpy as np, importlib.util
from scipy import ndimage
seed, Tf, Ta, out = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
RAD = float(os.environ.get('RAD', '9'))
spec = importlib.util.spec_from_file_location('w', 'world.py'); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
dt = w.META['dt']; s = w.init(seed, w.META['size'])
H, W = w.META['size']; yy, xx = np.mgrid[:H, :W]
def comps(A):
    m = ndimage.gaussian_filter(A.sum(0), 1, mode='wrap') > 0.15
    lab, k = ndimage.label(m)
    # periodic merge of labels across edges
    for a, b in zip(lab[0], lab[-1]):
        if a and b and a != b: lab[lab == b] = a
    for a, b in zip(lab[:, 0], lab[:, -1]):
        if a and b and a != b: lab[lab == b] = a
    ids = [i for i in np.unique(lab) if i]
    out = []
    for i in ids:
        mm = lab == i; ys, xs = np.nonzero(mm)
        cy = (np.angle(np.exp(2j*np.pi*ys/H).mean()) / (2*np.pi) * H) % H; cx = (np.angle(np.exp(2j*np.pi*xs/W).mean()) / (2*np.pi) * W) % W
        out.append((cy, cx, float(A[:, mm].sum()), mm))
    return out
def pd(a, b): return np.hypot(min(abs(a[0]-b[0]), H-abs(a[0]-b[0])), min(abs(a[1]-b[1]), W-abs(a[1]-b[1])))
t = 0.0
while True:   # advance until a fresh division: the closest comparable pair is within DMAX px (first check at Tf)
    for _ in range(int(round((Tf if t == 0 else 5) / dt))): s = w.step(s)
    t = Tf if t == 0 else t + 5
    cs = comps(s['A'])
    pairs = sorted((pd(a, b), i, j) for i, a in enumerate(cs) for j, b in enumerate(cs) if i < j and min(a[2], b[2]) >= 0.4*max(a[2], b[2]))
    pairs = [p for p in pairs if p[0] >= float(os.environ.get('DMIN', '18'))]
    if pairs and pairs[0][0] < float(os.environ.get('DMAX', '28')): break
d, i, j = pairs[0]; Tf = t
def far(q): return min([pd(cs[q], cs[r]) for r in range(len(cs)) if r not in (i, j)] or [999])
cut, sis = (i, j) if far(i) >= far(j) else (j, i)
print('fork t', Tf, 'bodies', len(cs), 'pair dist %.1f' % d, 'masses %.1f %.1f' % (cs[cut][2], cs[sis][2]), flush=True)
def track(st, p0, q0, starve):
    p, q = np.array(p0[:2]), np.array(q0[:2]); rec = []
    for n in range(int(round(Ta/dt))):
        if starve:
            dd = np.hypot(np.minimum(abs(yy-p[0]), H-abs(yy-p[0])), np.minimum(abs(xx-p[1]), W-abs(xx-p[1])))
            mask = dd < RAD; mv = st['phi'][mask].sum(); st['phi'][mask] = 0; st['phi'][~mask] += mv / (~mask).sum()
        st = w.step(st)
        if n % 10 == 0:
            cc = comps(st['A']); r = [n*dt + Tf]
            for pos in (p, q):
                if cc:
                    k = int(np.argmin([pd(pos, c) for c in cc])); dk = pd(pos, cc[k])
                    if dk < 10: pos[:] = cc[k][:2]; r.append(cc[k][2])
                    else: r.append(0.0)
                else: r.append(0.0)
            rec.append(r + [float(st['A'].sum() + st['phi'].sum())])
            if n % 50 == 0: snaps.append((n*dt+Tf, np.concatenate([st['A'], st['phi'][None], st['S'][None]]).astype(np.float16), p.copy(), q.copy()))
    return np.array(rec)
res = {}
for arm in ('fed', 'cut'):
    snaps = []
    st = copy.deepcopy(s)
    R = track(st, cs[cut], cs[sis], arm == 'cut')
    res[arm] = R; np.savez_compressed(f'{out}_{arm}.npz', R=R, X=np.array([x[1] for x in snaps]), t=np.array([x[0] for x in snaps]), P=np.array([x[2] for x in snaps]), Q=np.array([x[3] for x in snaps]))
    print(arm, 'starved-daughter mass t0 %.1f end %.1f; sister t0 %.1f end %.1f; ledger drift %.2e' % (R[0,1], R[-1,1], R[0,2], R[-1,2], (R[-1,3]-R[0,3])/R[0,3]), flush=True)
