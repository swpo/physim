import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import minimize
import time
N=24
I=np.eye(N); Lap=2*I-np.roll(I,1,0)-np.roll(I,-1,0); Adv=(np.roll(I,1,0)-np.roll(I,-1,0))/2
C=np.kron(np.eye(6),np.ones((1,4)))
k=2*np.pi*np.arange(N)/N
coskd=np.cos(np.arange(N)[:,None]*k)
inds=(np.arange(N)[:,None]-np.arange(N)[None,:])%N
lo=np.array([.05,.02,-.3]); hi=np.array([.25,.12,.3])

def matrices(th):
    D,g,c=th
    A=(1-g)*(I-D*Lap+c*Adv)
    ls=(1-g)**2*((1-2*D*(1-np.cos(k)))**2+(c*np.sin(k))**2)
    col=coskd@(.09/(1-ls))/N
    return A,col[inds]

def loglik(th, datasets, save=False):
    A,S=matrices(th)
    ll=0.
    for obs in datasets:
        B,T,G=obs.shape
        m=np.zeros((B,N)); P=S.copy()
        for t in range(T):
            res=obs[:,t,:]-m@C.T
            cross=P@C.T
            V=C@cross+.09*np.eye(G)
            cf=cho_factor(V,lower=True)
            K=cho_solve(cf,cross.T).T
            ll-=.5*(2*B*np.log(np.diag(cf[0])).sum()+(res*cho_solve(cf,res.T).T).sum())
            m+=res@K.T
            P-=K@cross.T
            m=m@A.T
            P=A@P@A.T+.09*I
    return ll

def hess(fun,x,eps=1e-4):
    eye=eps*np.eye(3); H=np.zeros((3,3))
    for i in range(3):
        for j in range(3):
            H[i,j]=(fun(x+eye[i]+eye[j])-fun(x+eye[i]-eye[j])-fun(x-eye[i]+eye[j])+fun(x-eye[i]-eye[j]))/(4*eps*eps)
    return H

def joint_cov(th,T):
    A,S=matrices(th)
    cs=[]
    for t in range(T):
        cs.append(C@S@C.T + (.09*np.eye(6) if t==0 else 0))
        S=A@S
    return np.block([[cs[i-j] if i>=j else cs[j-i].T for j in range(T)] for i in range(T)])

def fisher(th,T):
    cf=cho_factor(joint_cov(th,T))
    eps=np.eye(3)*1e-4
    der=[cho_solve(cf,(joint_cov(th+eps[j],T)-joint_cov(th-eps[j],T))/(2e-4)) for j in range(3)]
    return np.array([[np.trace(der[i]@der[j])*.5 for j in range(3)] for i in range(3)])

if __name__=='__main__':
    import os
    data=[np.load('data_initial.npz')['obs']]
    if os.path.exists('data_extra.npz'): data.append(np.load('data_extra.npz')['obs'])
    start=time.time()
    obj=lambda th:-loglik(th,data)
    fit=minimize(obj,[.15,.07,0.],bounds=list(zip(lo,hi)),method='L-BFGS-B',options={'ftol':1e-12,'gtol':1e-6})
    th=fit.x
    Hess=hess(obj,th)
    print('fit',fit, '\nsecs',time.time()-start)
    print('sd',np.sqrt(np.diag(np.linalg.inv(Hess))))
    print('corr',np.linalg.inv(Hess)/np.outer(np.sqrt(np.diag(np.linalg.inv(Hess))),np.sqrt(np.diag(np.linalg.inv(Hess)))))
    np.savez('fit.npz',theta=th,Hess=Hess)
    for t in [1,2,3,4,5,8,10,16,20,25,40]:
        f=fisher(th,t)
        print(t,'final sd',np.sqrt(np.diag(np.linalg.inv(Hess+200/t*f))), 'logdet',np.linalg.slogdet(Hess+200/t*f)[1],flush=True)
