import numpy as np, sys
def disp(chi, DF, kF, De=0.01, e0=0.15, kc=1, ks=1, y=1, hold=False):
    F=1.0
    if not hold:
        for _ in range(500):
            p=kc*F*e0/(kc*F*e0+ks); F=kF/(kF+y*kc*e0*(1-p))
    p=kc*F*e0/(kc*F*e0+ks)
    best=(-9,0)
    for q in np.linspace(0.01,2,400):
        q2=q*q; m=e0*(1-e0)
        # vars e,p,F ; cat = kc F e (1-p)
        ce=kc*F*(1-p); cp=-kc*F*e0; cF=kc*e0*(1-p)
        J=np.array([[-De*q2, chi*m*q2, 0],
                    [ce, -q2+cp-ks, cF],
                    [-y*ce, -y*cp, -DF*q2-y*cF-kF]])
        if hold: J=J[:2,:2]
        lam=np.linalg.eigvals(J).real.max()
        if lam>best[0]: best=(lam,q)
    return F,best
print('hold chi.3', disp(0.3,1,0,hold=True))
for chi in [0.3,0.6,1.0]:
  for DF in [0.25,1]:
    for kF in [0.01,0.05,0.2]:
        F,(l,q)=disp(chi,DF,kF); print(f"chi={chi} DF={DF} kF={kF} F0={F:.2f} lam={l:.4f} q*={q:.2f} L={2*np.pi/q:.0f}")
