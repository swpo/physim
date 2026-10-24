import json, sys
import numpy as np
src=open(sys.argv[1]).read()
pid=sys.argv[2]; N=int(sys.argv[3]); steps=int(sys.argv[4]); norm=sys.argv[5]=='norm'
i=src.index(f'patterns["{pid}"]'); j=src.index('"cells":',i); k=src.index('[',j)
depth=0
for e in range(k,len(src)):
    if src[e]=='[': depth+=1
    elif src[e]==']':
        depth-=1
        if depth==0: break
cells=np.array(json.loads(src[k:e+1].replace('\n','').replace('\t','').replace(',]',']')))
print('cells', cells.shape)
F=lambda s: eval(s) if '/' in s else float(s)
KS={'VT049W':[
([1],0.272,0.0595,0.138,0.91,0,0),([1],0.349,0.1585,0.48,0.62,0,0),([1,1/4],0.2,0.0332,0.284,0.5,0,0),
([0,1],0.114,0.0528,0.256,0.97,1,1),([1],0.447,0.0777,0.5,0.72,1,1),([5/6,1],0.247,0.0342,0.622,0.8,1,1),
([1],0.21,0.0617,0.35,0.96,2,2),([1],0.462,0.1192,0.218,0.56,2,2),([1],0.446,0.1793,0.556,0.78,2,2),
([11/12,1],0.327,0.1408,0.344,0.79,0,1),([3/4,1],0.476,0.0995,0.456,0.5,0,2),([11/12,1],0.379,0.0697,0.67,0.72,1,0),
([1],0.262,0.0877,0.42,0.68,1,2),([1/6,1,0],0.412,0.1101,0.43,0.82,2,0),([1],0.201,0.0786,0.278,0.82,2,1)]}
kers=KS[pid]; R=12; T=float(sys.argv[6]) if len(sys.argv)>6 else 2
bell=lambda x,m,s: np.exp(-((x-m)/s)**2/2)
y,x=np.mgrid[-N//2:N//2,-N//2:N//2]; D=np.sqrt(x**2+y**2)/R
fKs=[]
for b,m,s,h,r,c0,c1 in kers:
    Ds=D*len(b)/r; bb=np.array(b)
    K=(Ds<len(b))*bb[np.minimum(Ds.astype(int),len(b)-1)]*bell(Ds%1,0.5,0.15)
    K/=K.sum(); fKs.append(np.fft.fft2(np.fft.ifftshift(K)))
C=cells.shape[0]
A=np.zeros((C,N,N)); h0,w0=cells.shape[1],cells.shape[2]
A[:,N//2-h0//2:N//2-h0//2+h0,N//2-w0//2:N//2-w0//2+w0]=cells
def ncomp(M,thr=0.1):
    lab=np.zeros(M.shape,int); n=0; sizes=[]
    on=M>thr
    for (a,b) in zip(*np.nonzero(on)):
        if lab[a,b]: continue
        n+=1; st=[(a,b)]; lab[a,b]=n; sz=0
        while st:
            p,q=st.pop(); sz+=1
            for dp,dq in ((1,0),(-1,0),(0,1),(0,-1)):
                u,v=(p+dp)%M.shape[0],(q+dq)%M.shape[1]
                if on[u,v] and not lab[u,v]: lab[u,v]=n; st.append((u,v))
        sizes.append(sz)
    return sum(1 for s in sizes if s>=30)
hsum=[0]*C
for b,m,s,h,r,c0,c1 in kers: hsum[c1]+=h
for t in range(steps+1):
    if t%(steps//10)==0:
        print(f't={t/T:.0f} mass={A.sum():.1f} blobs(>=30px)={ncomp(A.sum(0))}', flush=True)
    fA=[np.fft.fft2(A[c]) for c in range(C)]
    G=np.zeros_like(A)
    for (b,m,s,h,r,c0,c1),fK in zip(kers,fKs):
        U=np.real(np.fft.ifft2(fK*fA[c0]))
        G[c1]+=h*(2*bell(U,m,s)-1)
    if norm:
        for c in range(C): G[c]/=hsum[c]
    A=np.clip(A+G/T,0,1)
