"""Bayesian linear-Gaussian filtering and posterior predictive trajectories."""
import os
import numpy as np
from scipy.special import ndtri, logsumexp
from scipy.stats import qmc

N = 24
I = np.eye(N)
LAP = 2*I - np.roll(I, 1, 0) - np.roll(I, -1, 0)
ADV = (np.roll(I, 1, 0) - np.roll(I, -1, 0))/2
C = np.kron(np.eye(6), np.ones((1, 4)))
ANG = 2*np.pi*np.arange(6)/6
L2 = np.stack([np.ones(6), np.cos(ANG), np.sin(ANG)])
K = 2*np.pi*np.arange(N)/N
COSKD = np.cos(np.arange(N)[:, None]*K)
IDX = (np.arange(N)[:, None] - np.arange(N)[None, :]) % N


def initial(theta):
    d,g,c = theta.T
    a = (1-g[:,None,None])*(I-d[:,None,None]*LAP+c[:,None,None]*ADV)
    spec = (1-g[:,None])**2*((1-2*d[:,None]*(1-np.cos(K)))**2+(c[:,None]*np.sin(K))**2)
    col = (.09/(1-spec)) @ COSKD.T/N
    return a, col[:,IDX]


def filter_history(theta, history, prefix):
    a,p = initial(theta)
    b = len(theta)
    m = np.zeros((b,N))
    ll = np.zeros(b)
    for t,y in enumerate(history):
        cross = p@C.T
        v = C@cross + .09*np.eye(6)
        r = y-m@C.T
        rhs = np.concatenate([cross.transpose(0,2,1), r[:,:,None]],axis=2)
        sol = np.linalg.solve(v,rhs)
        gain = sol[:,:,:N].transpose(0,2,1)
        ll -= .5*(np.linalg.slogdet(v)[1]+np.sum(r*sol[:,:,-1],axis=1))
        m += np.einsum('bij,bj->bi',gain,r)
        p -= gain@cross.transpose(0,2,1)
        if t < len(history)-1:
            m = np.einsum('bij,bj->bi',a,m)+prefix[t]
            p = a@p@a.transpose(0,2,1)+.09*I
    return a,m,(p+p.transpose(0,2,1))*.5,ll


def forecast_joint(a,m,p,test,queries):
    times = sorted({int(t) for ts in queries.values() for t in ts})
    block = {}; projection = {}; scale = []; dim=0
    for t in times:
        has_l1 = t in queries.get(1,[])
        projection[t] = np.eye(6) if has_l1 else L2
        d = len(projection[t])
        block[t] = slice(dim,dim+d)
        scale.extend([1.5]*6 if has_l1 else [4.3,2.7,2.7])
        dim+=d
    b = len(m)
    mean=np.zeros((b,dim)); cov=np.zeros((b,dim,dim))
    ps={}; powers=[np.broadcast_to(I,a.shape)]
    at=a.transpose(0,2,1)
    for t in range(1,max(times)+1):
        powers.append(a@powers[-1])
        m=np.einsum('bij,bj->bi',a,m)+test[t-1]
        p=a@p@at+.09*I
        if t in block:
            ps[t]=p.copy()
            mean[:,block[t]]=m@C.T@projection[t].T
    for j,t in enumerate(times):
        ct=projection[t]@C
        for s in times[:j+1]:
            cs=projection[s]@C
            v=ct@(powers[t-s]@ps[s])@cs.T
            if t==s:
                v=v+.09*projection[t]@projection[t].T
            cov[:,block[t],block[s]]=v
            cov[:,block[s],block[t]]=v.transpose(0,2,1)
    cov=(cov+cov.transpose(0,2,1))*.5
    return mean,cov,block,np.array(scale)


def predict(history, program, queries, n_samples, seed):
    posterior=np.load(os.path.join(os.path.dirname(__file__),'posterior.npz'))
    theta=posterior['theta']
    history=np.asarray(history,dtype=float)
    prefix=np.asarray(program['prefix'],dtype=float)
    test=np.asarray(program['test'],dtype=float)
    queries={int(l):list(map(int,ts)) for l,ts in queries.items()}
    a,m,p,ll=filter_history(theta,history,prefix)
    ll=ll+np.log(posterior['weight'])
    w=np.exp(ll-logsumexp(ll))
    dim=sum(6 if t in queries.get(1,[]) else 3 for t in {t for ts in queries.values() for t in ts})
    # Randomized low-discrepancy sampling keeps Gaussian marginals while reducing
    # finite-cloud Monte Carlo error.  Every row is one coherent future.
    q=qmc.Sobol(dim+1,scramble=True,seed=int(seed)%(2**32))
    u=q.random_base2(int(np.ceil(np.log2(max(n_samples,1)))))[:n_samples]
    ix=np.searchsorted(np.cumsum(w),u[:,0],side='right').clip(max=len(w)-1)
    mean,cov,block,scale=forecast_joint(a[ix],m[ix],p[ix],test,queries)
    cov=cov/scale[None,:,None]/scale[None,None,:]
    avg=cov.mean(0)
    vals,vecs=np.linalg.eigh(avg)
    # Use principal directions for the reference covariance, and a smooth
    # orthogonal rotation of each component's Cholesky factor.
    ref=np.linalg.cholesky(avg)
    rotation=np.linalg.solve(ref,vecs[:,::-1]*np.sqrt(np.maximum(vals[::-1],1e-14)))
    noise=ndtri(np.clip(u[:,1:],1e-12,1-1e-12))@rotation.T
    draws=mean+np.einsum('bij,bj->bi',np.linalg.cholesky(cov),noise)*scale
    result={}
    for level,ts in queries.items():
        result[level]=np.stack([draws[:,block[t]] if level==1 or t not in queries.get(1,[]) else draws[:,block[t]]@L2.T for t in ts],axis=1)
    return result
