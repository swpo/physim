import numpy as np
mu_k,sigma_k,w_k,mu_g,sigma_g,c_rep=4.0,1.0,0.022,0.6,0.15,1.0
rng=np.random.default_rng(20)
P=(rng.random((200,2))-0.5)*12.0
dt=0.1
def step(P):
    d=P[:,None,:]-P[None,:,:]            # x_i - p_j
    r=np.sqrt((d**2).sum(-1)); np.fill_diagonal(r,1e6)
    u=(d/ r[...,None])
    k=np.exp(-((r-mu_k)/sigma_k)**2)
    U=w_k*k.sum(1)
    dU=(w_k*k*(-2*(r-mu_k)/sigma_k**2))[...,None]*u
    dU=dU.sum(1)
    G=np.exp(-((U-mu_g)/sigma_g)**2)
    dG=(G*(-2*(U-mu_g)/sigma_g**2))[:,None]*dU
    rep=np.clip(1-r,0,None)
    dR=(-c_rep*rep)[...,None]*u; dR=dR.sum(1)
    E=(c_rep/2*(rep**2).sum(1)-G)
    return P+dt*(dG-dR), E.mean()
for t in range(10001):
    P,E=step(P)
    if t%2000==0:
        c=P.mean(0); v=None
        print(t, round(E,4), np.round(c,3), np.round(np.abs(P-c).max(),2))
# angular velocity estimate
P2,_=step(P); c=P.mean(0); rel=P-c; vel=(P2-P)/dt
L=np.mean(rel[:,0]*vel[:,1]-rel[:,1]*vel[:,0]); print('angmom', L, 'mean speed', np.linalg.norm(vel,axis=1).mean())
vc=vel-vel.mean(0)
om=(rel[:,0]*vc[:,1]-rel[:,1]*vc[:,0])/(rel**2).sum(1)
print('omega mean',om.mean(),'omega std',om.std(),'drift speed',np.linalg.norm(vel.mean(0)))
