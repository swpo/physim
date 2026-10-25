import numpy as np, sys, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
out=sys.argv[1]; runs=sys.argv[2:]
fig,ax=plt.subplots(1,2,figsize=(10,3.6)); res={}
for r in runs:
    lab,path=r.split('=')
    d=np.load(path+'/frames.npz'); m=d['matter']; R=d['render']; f=d['render_f']
    dtf=300*0.01
    ls='-' if 'full' in lab else ('--' if 'noK' in lab else ':')
    ax[0].plot(np.arange(len(m))*dtf, m.reshape(len(m),-1).sum(1), ls, label=lab)
    ax[1].plot(f*dtf, R[:,2].reshape(len(f),-1).sum(1), ls, label=lab)
    res[lab]={'u_total_t0':float(m[0].sum()),'u_total_t300':float(m[100].sum()),'u_total_end':float(m[-1].sum()),'K_total_end':float(R[-1,2].sum())}
ax[0].set_xlabel('time'); ax[0].set_ylabel('total amphiphile (u+1)'); ax[0].set_yscale('log'); ax[0].legend(fontsize=7)
ax[1].set_xlabel('time'); ax[1].set_ylabel('total catalyst K'); ax[1].set_yscale('symlog'); ax[1].legend(fontsize=7)
plt.tight_layout(); plt.savefig(out,dpi=100); print(json.dumps(res,indent=1))
