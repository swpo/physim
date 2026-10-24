import sys, json, numpy as np
from scipy import ndimage
sys.path.insert(0,'.'); sys.path.insert(0,'threads/lenia-multichannel/tools')
from labkit.world import load_world
from quick import rgb
from PIL import Image
W=load_world(sys.argv[1]); size=int(sys.argv[2]); steps=int(sys.argv[3])
s=W.init(0,(size,size))
for _ in range(steps-20): s=W.step(s)
A1=s["A"].copy()
for _ in range(20): s=W.step(s)
A2=s["A"].copy()
def comps(A):
    m=ndimage.gaussian_filter(A.sum(0),1,mode='wrap')>0.15
    lab,n=ndimage.label(m); return lab,n
l1,n1=comps(A1); l2,n2=comps(A2)
c1=np.array(ndimage.center_of_mass(np.ones_like(l1),l1,range(1,n1+1)))
c2=np.array(ndimage.center_of_mass(np.ones_like(l2),l2,range(1,n2+1)))
a2=ndimage.sum(np.ones_like(l2),l2,range(1,n2+1))
out=[]
for j in range(n2):
    if a2[j]<30: continue
    d=np.hypot(*(c1-c2[j]).T); i=np.argmin(d)
    out.append((d[i],j,a2[j]))
out.sort()
print("n comps",len(out)); print("speeds px/20steps:", [round(o[0],1) for o in out])
def enc_crop(lab,j,A):
    cy,cx=[int(round(v)) for v in ndimage.center_of_mass(lab==j+1)]
    h=16; H=A.shape[1]
    sh=lambda X,ax0: np.roll(np.roll(X,H//2-cy,ax0),H//2-cx,ax0+1)
    crop=(sh(A,1)*sh(lab==j+1,0)[None])[:,H//2-h:H//2+h,H//2-h:H//2+h]
    return crop
def val2ch(v):
    if v==0: return '.'
    if v<25: return chr(ord('A')+v-1)
    return chr(ord('p')+(v-25)//24)+chr(ord('A')+(v-25)%24)
enc=lambda a: '$'.join(''.join(val2ch(int(v)) for v in r) for r in np.rint(a*255).astype(int))+'!'
slow=enc_crop(l2,out[0][1],A2); fast=enc_crop(l2,out[-1][1],A2)
json.dump({"slow":[enc(c) for c in slow],"fast":[enc(c) for c in fast]},open(sys.argv[4],'w'))
Image.fromarray(np.kron(np.concatenate([rgb(slow),rgb(fast)],1),np.ones((6,6,1),dtype=np.uint8))).save(sys.argv[4].replace('.json','.png'))
