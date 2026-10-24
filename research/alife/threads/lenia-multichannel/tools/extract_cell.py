import sys, json, numpy as np
from scipy import ndimage
sys.path.insert(0,'.')
from labkit.world import load_world
W=load_world(sys.argv[1]); s=W.init(0,(128,128))
for _ in range(1000): s=W.step(s)
A=s["A"]; m=A.sum(0)
lab,n=ndimage.label(ndimage.gaussian_filter(m,1)>0.05)
areas=ndimage.sum(np.ones_like(m),lab,range(1,n+1)); k=int(np.argsort(areas)[len(areas)//2])+1
cy,cx=[int(round(v)) for v in ndimage.center_of_mass(lab==k)]
h=20
crop=np.roll(np.roll(A,64-cy,1),64-cx,2)[:,64-h:64+h,64-h:64+h]*(np.roll(np.roll(lab==k,64-cy,0),64-cx,1)[64-h:64+h,64-h:64+h])
def val2ch(v):
    if v==0: return '.'
    if v<25: return chr(ord('A')+v-1)
    return chr(ord('p')+(v-25)//24)+chr(ord('A')+(v-25)%24)
def enc(a):
    rows=[]
    for r in np.rint(a*255).astype(int):
        rows.append(''.join(val2ch(int(v)) for v in r))
    return '$'.join(rows)+'!'
print(json.dumps([enc(c) for c in crop]))
print('mass',crop.sum(), file=sys.stderr)
