"""FCH as in the NSF benchmark (Promislow group): u_t = Lap[(e^2 Lap - W'')(e^2 Lap u - W') + e^2 eta1 Lap u - eta2 W'],
W = [(u+1)^2/2][(u-1)^2/2 + g/3 (u-2)], eta1=1.45e, eta2=3e (sub/super) or 1.5e (critical), bath u=-1+e d/alpha^2."""
import numpy as np, sys, time
G=0.3
def W(u):  A=(u+1)**2/2; B=(u-1)**2/2+G/3*(u-2); return A*B
def Wp(u): A=(u+1)**2/2; B=(u-1)**2/2+G/3*(u-2); return (u+1)*B+A*((u-1)+G/3)
def Wpp(u):A=(u+1)**2/2; B=(u-1)**2/2+G/3*(u-2); return B+2*(u+1)*((u-1)+G/3)+A
AL2=Wpp(-1.0)
def grid(N,L):
    x=(np.arange(N))*L/N; X,Y=np.meshgrid(x,x,indexing='ij'); return X,Y
def bilayer_curve_ic(N,L,eps,d,rho_fn):
    X,Y=grid(N,L); th=np.arctan2(Y-L/2,X-L/2); r=np.hypot(X-L/2,Y-L/2)
    z=(r-rho_fn(th))/eps
    # bilayer profile: homoclinic approx; use sech^2 with peak near u*~ +1
    return -1+2.0/np.cosh(z/1.0)**2 + eps*d/AL2
def run(u0, L=4*np.pi, eps=0.1, eta1=1.45, eta2=3.0, dt=1e-3, T=1.0, S=1.0, nsnap=6, feed=0.0, src=None, cb=None):
    N=u0.shape[0]; u=u0.copy()
    k=2*np.pi*np.fft.fftfreq(N,d=L/N); KX,KY=np.meshgrid(k,k,indexing='ij'); k2=KX**2+KY**2
    e2=eps**2; et1=eta1*eps; et2=eta2*eps
    q=e2*k2; Lmu=(q+AL2)**2 - et1*q*0 + S  # (q+a)(q+a) + stab
    den=1+dt*k2*Lmu
    snaps=[]; nsteps=int(round(T/dt)); every=max(1,nsteps//(nsnap-1)); times=[]
    for n in range(nsteps+1):
        if n%every==0: snaps.append(u.copy()); times.append(n*dt)
        if n==nsteps: break
        uh=np.fft.fft2(u)
        lu=np.real(np.fft.ifft2(-k2*uh))
        w=e2*lu-Wp(u)
        lw=np.real(np.fft.ifft2(-k2*np.fft.fft2(w)))
        mu=e2*lw-Wpp(u)*w+et1*e2*lu-et2*Wp(u)
        u=np.real(np.fft.ifft2((uh - dt*k2*(np.fft.fft2(mu)-Lmu*uh))/den))
        if feed: u=u+dt*feed*(1 if src is None else src(u))
        if not np.isfinite(u).all(): print('blowup',n); break
    return snaps,times
def show(s,fn,title='',times=None):
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig,ax=plt.subplots(1,len(s),figsize=(3*len(s),3.2))
    for i,(a,f) in enumerate(zip(ax,s)): a.imshow(f,cmap='magma',vmin=-1.1,vmax=1.1); a.axis('off'); a.set_title(f't={times[i] if times else i:.2f} {f.min():.2f}..{f.max():.2f} m={f.mean():.3f}',fontsize=7)
    fig.suptitle(title,fontsize=8); plt.savefig(fn,dpi=70,bbox_inches='tight'); plt.close()
if __name__=='__main__':
    args=dict(a.split('=') for a in sys.argv[2:]); args={k:float(v) if k not in('N','seed','nsnap') else int(v) for k,v in args.items()}
    N=args.pop('N',256); d=args.pop('d',0.2); eps=args.get('eps',0.1); seed=args.pop('seed',0); mode=args.pop('ic',0)
    if mode==0:
        u0=bilayer_curve_ic(N,4*np.pi,eps,d,lambda th: 3-eps/2*np.cos(6*(th-np.pi/11))-eps**2*np.cos(th-3*np.pi/11))
    else:
        rng=np.random.default_rng(seed); u0=-1+eps*d/AL2+args.pop('amp',0.3)*(rng.random((N,N))*2-1)
    t=time.time(); s,ts=run(u0,**args); print('time',time.time()-t)
    np.save(sys.argv[1].replace('.png','.npy'),s[-1]); show(s,sys.argv[1],' '.join(sys.argv[2:])+f' d={d}',ts)
