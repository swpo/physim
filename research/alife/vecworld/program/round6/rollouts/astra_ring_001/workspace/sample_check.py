import numpy as np
from scipy.special import ndtri
from scipy.stats import qmc
from scipy.spatial.distance import cdist,pdist
from submission.predict import filter_history,forecast_joint,L2
th=np.load('fit.npz')['theta']; h=np.load('data_initial.npz')['obs'][0,-17:]
a,m,p,ll=filter_history(th[None],h,np.zeros((16,24)))
queries={1:[1,2,4,8,16],2:[16,32]}
mu,cov,block,scale=forecast_joint(a,m,p,np.zeros((32,24)),queries)
s=cov[0]/scale[:,None]/scale[None,:]; d=len(s);L=np.linalg.cholesky(s)
e,V=np.linalg.eigh(s); B=V[:,::-1]*np.sqrt(e[::-1]);R=np.linalg.solve(L,B)
# Actual marginal score, including both level-1 and level-2 at time 16.
trans=[]
for level,ts in queries.items():
 for t in ts:
  proj=np.eye(d)[block[t]]
  if level==2 and t in queries[1]: proj=np.diag(1/np.array([4.3,2.7,2.7]))@L2@np.diag(scale[block[t]])@proj
  trans.append(proj)
rng=np.random.default_rng(196)
y=rng.normal(size=(4096,d))@L.T
ys=[y@T.T for T in trans]
results={method:[] for method in ['iid','antithetic','qmc-chol','qmc-pca']}
for seed in range(100):
 rng=np.random.default_rng(seed)
 z=rng.normal(size=(32,d));anti=rng.normal(size=(16,d));anti=np.concatenate([anti,-anti]);u=ndtri(qmc.Sobol(d,scramble=True,seed=seed).random_base2(5))
 xs={'iid':z@L.T,'antithetic':anti@L.T,'qmc-chol':u@L.T,'qmc-pca':u@B.T}
 for method,x in xs.items():
  scores=[]
  for T,truth in zip(trans,ys):
   xx=x@T.T
   scores.append((cdist(xx,truth).mean()-pdist(xx).sum()/32**2)/np.sqrt(len(T)))
  results[method].append(np.mean(scores))
for method,x in results.items():print(method,np.mean(x),np.std(x))
