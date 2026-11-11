import numpy as np
from infer import loglik,joint_cov,matrices,C
from scipy.linalg import cho_factor,cho_solve
from submission.predict import filter_history,forecast_joint,predict,L2
from time import time
th=np.load('fit.npz')['theta']
h=np.load('data_initial.npz')['obs'][0]
y=h.ravel();V=joint_cov(th,len(h));cf=cho_factor(V)
ll=-np.log(np.diag(cf[0])).sum()-.5*y@cho_solve(cf,y)
a,m,p,lik=filter_history(th[None],h,np.zeros((len(h)-1,24)))
print('GP vs inference KF vs prediction KF:',ll,loglik(th,[h[None]]),lik)
queries={1:[1,2,4,8,16],2:[16,32]}
mu,cov,block,scale=forecast_joint(a,m,p,np.zeros((32,24)),queries)
# Direct Gaussian conditioning of full observed past and future.
full=joint_cov(th,len(h)+32)
obs_ix=np.arange(len(h)*6)
future_ix=np.concatenate([np.arange((len(h)-1+t)*6,(len(h)+t)*6) for t in sorted(block)])
cross=full[np.ix_(future_ix,obs_ix)]
conditional_mu=cross@cho_solve(cf,y)
conditional_cov=full[np.ix_(future_ix,future_ix)]-cross@cho_solve(cf,cross.T)
proj=np.zeros((33,36));proj[:30,:30]=np.eye(30);proj[30:,30:]=L2
print('Forecast mean/cov errors:',np.max(np.abs(mu[0]-proj@conditional_mu)),np.max(np.abs(cov[0]-proj@conditional_cov@proj.T)))
praw=np.load('posterior_raw.npz'); w=praw['weight']; theta=praw['theta']
p1024=np.load('submission/posterior.npz')['theta']
print('Full posterior and compressed posterior means:',w@theta,p1024.mean(0))
print('Full posterior and compressed posterior sd:',np.sqrt(np.einsum('b,bi,bi->i',w,theta-w@theta,theta-w@theta)),p1024.std(0))
t=time(); pred=predict(h[-17:],{'prefix':np.zeros((16,24)),'test':np.zeros((32,24))},queries,32,113)
print('prediction time',time()-t,'coherence discrepancy',np.max(np.abs(pred[1][:,-1]@L2.T-pred[2][:,0])))
