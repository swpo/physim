import numpy as np, sys
from scipy import ndimage as ndi
sp=sys.argv[1]
for s in sys.argv[2:]:
    for arm in ('up','twin'):
        d=np.load(f'{sp}/{arm}/seed{s}/frames.npz'); R=d['render']; f=d['render_f']
        out=[]
        for t in (80,120,140,160):
            i=int(np.argmin(abs(f-t))); k1,k2=R[i,0],R[i,1]; tot=k1+k2
            lab,n=ndi.label(tot>0.3*np.percentile(tot,99))
            if n==0: out.append((t*250,0,0)); continue
            s1=ndi.sum(k1,lab,range(1,n+1)); s2=ndi.sum(k2,lab,range(1,n+1)); a=ndi.sum(np.ones_like(k1),lab,range(1,n+1))
            keep=a>=20; n2=int(((s2>s1)&keep).sum()); n1=int(((s1>=s2)&keep).sum())
            out.append((t*250,n1,n2))
        print(arm,s,'(t, K1 cells, K2 cells):',out)
