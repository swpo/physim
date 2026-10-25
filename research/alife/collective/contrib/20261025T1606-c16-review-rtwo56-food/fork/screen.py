import sys, os, json, numpy as np, importlib.util, time
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy import ndimage
wp, out, seed, T = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
spec = importlib.util.spec_from_file_location('w', wp); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, w.META['size']); dt = w.META['dt']
n = int(T/dt); NP=int(os.environ.get("NP","6")); T0=float(os.environ.get("T0","0")); snaps = np.linspace(int(T0/dt), n, NP+1).astype(int)[1:]
imgs = []; log = []
t0=time.time()
for i in range(1, n+1):
    s = w.step(s)
    if i % int(10/dt) == 0:
        A = s['A']; lab, k = ndimage.label(ndimage.gaussian_filter(A[0],1) > 0.15, structure=np.ones((3,3)))
        log.append((i*dt, k, A[0].sum(), A[1].sum(), s['F'].mean(), s['F'].min()))
    if i in snaps:
        imgs.append((i*dt, np.stack([np.clip(s['A'][1],0,1), np.clip(s['A'][0],0,1), np.clip(s['F']/max(s['F'].max(),1e-9),0,1)],-1)))
nc=min(len(imgs),6); nr=(len(imgs)+5)//6; fig, ax = plt.subplots(nr, nc, figsize=(3*nc, 3.2*nr), squeeze=False)
for a,(t,im) in zip(ax.ravel(), imgs):
    a.imshow(im); a.set_title(f't={t:.0f}'); a.axis('off')
fig.suptitle(f"{os.environ.get('WORLD_P','')} seed{seed}  R=A1 shell G=A0 core B=F/maxF", fontsize=8)
plt.tight_layout(); plt.savefig(out+'.png', dpi=70)
json.dump(log, open(out+'.json','w'))
L=np.array(log); print(out, f"{time.time()-t0:.0f}s", 'cores', L[::max(1,len(L)//8),1].astype(int).tolist(), 'Fmean %.3f Fmin %.3f'%(L[-1,4],L[-1,5]), 'A0 %.0f A1 %.0f'%(L[-1,2],L[-1,3]))
