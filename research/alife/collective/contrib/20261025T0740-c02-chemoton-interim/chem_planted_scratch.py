"""FCH field chemoton scratch. u: amphiphile (FCH), P: precursor (fed, crosses membranes),
K: catalyst, Gray-Scott-like autocatalysis K^2 P, transport gated by the bilayer: D_K exp(-beta (u+1)).
K converts P into amphiphile: u += r K P. Amphiphile degrades: -kap (u+1)."""
import numpy as np, sys, time
from bfch import Wp, Wpp, AL2, show
def roll_lap_gated(K, g, D, dx):
    # div(D g grad K) with min face mobility
    out=np.zeros_like(K)
    for ax in (0,1):
        for s in (1,-1):
            Kn=np.roll(K,-s,axis=ax); gn=np.roll(g,-s,axis=ax)
            out+=np.minimum(g,gn)*(Kn-K)
    return D*out/dx**2
def run(u,P,K, L=4*np.pi, eps=0.1, eta1=1.45, eta2=3.0, dt=1e-2, T=10, S=1.0, nsnap=6,
        Dp=0.05, Dk=0.05, beta=4.0, F=0.04, a=1.0, dK=0.1, r=0.0, kap=0.0, b=0.0, ub=None):
    N=u.shape[0]; dx=L/N
    k=2*np.pi*np.fft.fftfreq(N,d=dx); KX,KY=np.meshgrid(k,k,indexing='ij'); k2=KX**2+KY**2
    e2=eps**2; et1=eta1*eps; et2=eta2*eps; q=e2*k2; Lmu=(q+AL2)**2+S; den=1+dt*k2*Lmu
    snaps=[]; nsteps=int(round(T/dt)); every=max(1,nsteps//(nsnap-1)); ts=[]
    for n in range(nsteps+1):
        if n%every==0: snaps.append((u.copy(),P.copy(),K.copy())); ts.append(n*dt)
        if n==nsteps: break
        uh=np.fft.fft2(u); lu=np.real(np.fft.ifft2(-k2*uh)); w=e2*lu-Wp(u)
        lw=np.real(np.fft.ifft2(-k2*np.fft.fft2(w))); mu=e2*lw-Wpp(u)*w+et1*e2*lu-et2*Wp(u)
        unew=np.real(np.fft.ifft2((uh - dt*k2*(np.fft.fft2(mu)-Lmu*uh))/den))
        g=np.exp(-beta*np.clip(u+1,0,None))
        auto=a*K*K*P; prod=r*K*P
        Pn=P+dt*(roll_lap_gated(P,np.ones_like(P),Dp,dx)+F*(1-P)-auto-prod)
        Kn=K+dt*(roll_lap_gated(K,g,Dk,dx)+auto-dK*K)
        u=unew+dt*(prod-kap*((u+1)-b))
        P,K=Pn,Kn
        if not np.isfinite(u).all(): print('blowup',n); break
    return snaps,ts
def show3(s,ts,fn,title=''):
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig,ax=plt.subplots(3,len(s),figsize=(2.6*len(s),8))
    for i,(u,P,K) in enumerate(s):
        ax[0,i].imshow(u,cmap='magma',vmin=-1.1,vmax=1.1); ax[0,i].set_title(f't={ts[i]:.0f} u m={u.mean():.3f}',fontsize=7)
        ax[1,i].imshow(P,cmap='viridis',vmin=0,vmax=1); ax[1,i].set_title(f'P {P.min():.2f}..{P.max():.2f}',fontsize=7)
        ax[2,i].imshow(K,cmap='inferno',vmin=0,vmax=max(1e-3,K.max())); ax[2,i].set_title(f'K max {K.max():.2f} sum {K.sum():.0f}',fontsize=7)
    for a in ax.flat: a.axis('off')
    fig.suptitle(title,fontsize=8); plt.savefig(fn,dpi=60,bbox_inches='tight'); plt.close()
if __name__=='__main__':
    args=dict(a.split('=') for a in sys.argv[2:]); args={k:float(v) if k not in('N','nsnap','ic') else int(v) for k,v in args.items()}
    N=int(args.pop('N',192)); L=N*4*np.pi/256; args['L']=L; x=(np.arange(N)+0.5)*L/N-L/2; X,Y=np.meshgrid(x,x,indexing='ij')
    ic=args.pop('ic',0); R=args.pop('R',2.0); K0=args.pop('K0',0.5)
    r1=np.hypot(X,Y); r2=np.hypot(X-99,Y)
    u=-1+0.02+1.5/np.cosh((r1-R)/0.1)**2   # vesicle on the left
    K=K0*((r1<R-0.3)|(r2<R-0.3)).astype(float)   # K inside the vesicle and a bare K disk on the right
    P=np.ones_like(u)*0.5
    if ic==1:
        rng=np.random.default_rng(int(args.pop('seed',0)))
        u=-1+args.pop('off',0.1)+0.3*(2*rng.random(u.shape)-1); K=K0*rng.random(u.shape)
    t=time.time(); s,ts=run(u,P,K,**args); print('time',time.time()-t)
    show3(s,ts,sys.argv[1],' '.join(sys.argv[2:]))
