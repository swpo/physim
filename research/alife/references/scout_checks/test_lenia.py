import json, re, sys
import numpy as np
animals_path, patterns_path = sys.argv[1], sys.argv[2]

def ch2val(c):
    if c in '.b': return 0
    if c == 'o': return 255
    if len(c) == 1: return ord(c)-ord('A')+1
    return (ord(c[0])-ord('p'))*24 + (ord(c[1])-ord('A')+25)

def rle2arr(st):
    rows=[]; row=[]; cnt=''; last=''
    for ch in st:
        if ch.isdigit(): cnt+=ch
        elif ch in 'pqrstuvwxy@': last=ch
        else:
            if ch in '$!':
                n=int(cnt) if cnt else 1
                rows.append(row); [rows.append([]) for _ in range(n-1)]; row=[]; cnt=''
                if ch=='!': break
                continue
            v=ch2val(last+ch); last=''
            n=int(cnt) if cnt else 1; cnt=''
            row += [v/255]*n
    w=max(len(r) for r in rows)
    return np.array([r+[0]*(w-len(r)) for r in rows])

animals=json.load(open(animals_path))
orb=[a for a in animals if a.get('code')=='O2u'][0]
cells=rle2arr(orb['cells']); p=orb['params']
print('Orbium params', p, 'cells', cells.shape)

def bump4(r): 
    with np.errstate(divide='ignore', over='ignore'):
        return np.where((r>0)&(r<1), np.exp(4-1/(r*(1-r))), 0)
def quad4(r): return np.where((r>0)&(r<1),(4*r*(1-r))**4,0)
gaus=lambda u,m,s: 2*np.exp(-(u-m)**2/(2*s**2))-1
polyg=lambda u,m,s: 2*np.maximum(0,1-(u-m)**2/(9*s**2))**4-1

def run_orbium(core, growth, R=13, T=10, m=0.15, s=0.015, N=128, steps=1000, scale=1):
    y,x=np.mgrid[-N//2:N//2,-N//2:N//2]; D=np.sqrt(x**2+y**2)/R
    K=core(D)*(D<1); K/=K.sum(); fK=np.fft.fft2(np.fft.ifftshift(K))
    A=np.zeros((N,N)); c=cells
    A[N//2-c.shape[0]//2:N//2-c.shape[0]//2+c.shape[0], N//2-c.shape[1]//2:N//2-c.shape[1]//2+c.shape[1]]=c
    m0=A.sum(); cms=[]
    for t in range(steps):
        U=np.real(np.fft.ifft2(fK*np.fft.fft2(A)))
        A=np.clip(A+growth(U,m,s)/T,0,1)
    return m0, A.sum()

for name,core,g in [('bump4+gauss',bump4,gaus),('quad4+poly',quad4,polyg)]:
    for T in [10, 50, 2]:
        m0,m1=run_orbium(core,g,T=T,steps=100*T)
        print(f'Orbium {name} T={T}: mass t=0 {m0:.1f} -> t=100 {m1:.1f}')
