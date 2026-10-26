import numpy as np, json, sys
def ss(q):
    e=q["e0"]; F=1.0
    for _ in range(500):
        c=q["kc"]*F*e**q["n"]; p=c/(c+q["ks"]); F=q["kF"]/(q["kF"]+q["y"]*q["kc"]*e**q["n"]*(1-p))
    return e,p,F
def growth(q,ks=np.linspace(0.005,1.5,300)):
    e,p,F=ss(q); L2=q["Lsc"]**2
    re=q["n"]*q["kc"]*F*e**(q["n"]-1)*(1-p); rF=q["kc"]*e**q["n"]*(1-p); rp=q["kc"]*F*e**q["n"]
    out=[]
    for k in ks:
        k2=k*k*L2
        J=np.array([[-q["De"]*k2-q["d"], q["chi"]*e*(1-e)*k2, 0],
                    [re, -q["Dp"]*k2-rp-q["ks"], rF],
                    [-q["y"]*re, q["y"]*rp, -q["DF"]*k2-q["y"]*rF-q["kF"]]])
        out.append(np.linalg.eigvals(J).real.max())
    out=np.array(out); i=out.argmax(); return out[i], ks[i], (e,p,F)
base=dict(De=0.1,chi=3,kc=2,ks=1,DF=2,y=1,kF=0.2,Dp=1,n=2,d=0.0001,Lsc=3,e0=0.12)
if __name__=="__main__":
    for e0 in [0.12,0.15,0.2,0.25,0.3]:
      for d in [0.0001,0.001,0.003,0.01]:
        for chi in [3,5]:
          q=dict(base,e0=e0,d=d,chi=chi); s,k,st=growth(q)
          print(f"e0={e0} d={d} chi={chi}: sigma_max={s:.2e} at k={k:.3f} (lambda={2*np.pi/k:.0f}px) ss p={st[1]:.2f} F={st[2]:.2f}")
