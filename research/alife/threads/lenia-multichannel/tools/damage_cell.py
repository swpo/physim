import sys, numpy as np
from scipy import ndimage
from PIL import Image
sys.path.insert(0,'threads/lenia-multichannel/tools'); sys.path.insert(0,'.')
from quick import rgb
from labkit.world import load_world
W=load_world(sys.argv[1]); size=int(sys.argv[2]); pre=int(sys.argv[3]); post=int(sys.argv[4]); seed=int(sys.argv[5]) if len(sys.argv)>5 else 0
s=W.init(seed,(size,size))
for _ in range(pre): s=W.step(s)
A0=s["A"].copy()
m=A0.sum(0); lab,n=ndimage.label(ndimage.gaussian_filter(m,1)>0.3); areas=ndimage.sum(np.ones_like(m),lab,range(1,n+1))
# pick component with median area
k=int(np.argsort(areas)[len(areas)//2])+1
cy,cx=ndimage.center_of_mass(lab==k); area=areas[k-1]
print("cells",n,"areas",sorted(areas.astype(int)),"chosen",k,area)
rows=[]
for frac,mode in eval(sys.argv[7]):
    s["A"]=A0.copy()
    yy,xx=np.mgrid[:size,:size]
    mask=lab==k
    if mode=='half':
        # erase a slab covering frac of the cell from one side
        proj=(xx-cx); thr=np.quantile(proj[mask],1-frac); hole=mask&(proj>=thr)
    elif mode=='core':
        r=np.sqrt(frac*area/np.pi); hole=mask&((yy-cy)**2+(xx-cx)**2<=r*r)
    else: hole=np.zeros_like(mask)
    s["A"][:,hole]=0
    tiles=[]; 
    for t in range(post+1):
        if t%(post//6)==0:
            c=np.roll(np.roll(s["A"],size//2-int(cy),1),size//2-int(cx),2)[:,size//2-20:size//2+20,size//2-20:size//2+20]
            tiles.append(np.pad(rgb(c),((1,1),(1,1),(0,0)),constant_values=60))
        if t<post: s=W.step(s)
    Afin=np.roll(np.roll(s["A"],size//2-int(cy),1),size//2-int(cx),2)[:,size//2-20:size//2+20,size//2-20:size//2+20]
    print(mode,frac,"erased",int(hole.sum()),"of",int(area),"final local mass",round(float(Afin.sum()),1))
    rows.append(np.concatenate(tiles,1))
Image.fromarray(np.kron(np.concatenate(rows,0),np.ones((3,3,1),dtype=np.uint8))).save(sys.argv[6] if len(sys.argv)>6 else 'dmg.png')
