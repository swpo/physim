import sys, glob, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
d=sys.argv[1]; out=sys.argv[2]; fs=sorted(glob.glob(d+"/e_*.npy")); t0=float(sys.argv[3]) if len(sys.argv)>3 else 0
fs=[f for f in fs if int(f[-10:-4])>=t0]; idx=np.linspace(0,len(fs)-1,min(16,len(fs))).astype(int)
fig,ax=plt.subplots(2,8,figsize=(16,4.4)); ax=ax.ravel()
for a,i in zip(ax,idx): a.imshow(np.load(fs[i]).astype(float),cmap="magma",vmin=0,vmax=1); a.set_title("t="+fs[i][-10:-4].lstrip("0"),fontsize=8); a.axis("off")
for a in ax[len(idx):]: a.axis("off")
fig.tight_layout(); fig.savefig(out,dpi=60)
