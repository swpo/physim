import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np
from scipy.special import ndtri,logsumexp
from scipy.stats import qmc,chi2
from infer import loglik,lo,hi
from time import time
z=np.load('fit.npz'); mode=z['theta']; cov=np.linalg.inv(z['Hess'])
data=[np.load('data_initial.npz')['obs'],np.load('data_extra.npz')['obs']]
# A slightly heavy-tailed importance distribution avoids a Gaussian tail approximation.
n=16384; df=8; scale=1.2
u=qmc.Sobol(4,scramble=True,seed=7262).random_base2(14)
y=ndtri(u[:,:3])/np.sqrt(chi2.ppf(u[:,3],df)[:,None]/df)
particles=mode+y@np.linalg.cholesky(cov*scale**2).T
valid=((particles>lo)&(particles<hi)).all(1)
particles=particles[valid]; y=y[valid]
ll=np.empty(len(particles)); start=time()
for j,th in enumerate(particles):
    ll[j]=loglik(th,data)
    if j%2000==0: print(j,len(particles),'sec',time()-start,flush=True)
logq=-(df+3)/2*np.log1p((y*y).sum(1)/df)
logw=ll-logq; w=np.exp(logw-logsumexp(logw))
mu=w@particles
covpost=np.einsum('b,bi,bj->ij',w,particles-mu,particles-mu)
print('posterior mean',mu,'sd',np.sqrt(np.diag(covpost)),'ESS',1/(w@w),flush=True)
np.savez('posterior_raw.npz',theta=particles,weight=w,ll=ll)
# Systematic resampling (Sobol's existing space filling order is kept).
k=1024
ix=np.searchsorted(np.cumsum(w),(np.arange(k)+.37)/k)
np.savez('submission/posterior.npz',theta=particles[ix])
