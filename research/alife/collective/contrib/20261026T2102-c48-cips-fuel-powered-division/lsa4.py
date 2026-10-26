"""Linear stability of the uniform bath of the c48 fuel-powered-turnover world (e, p, F, i)."""
import numpy as np, sys, json
def ss(q):
    e = q["e0"]; F = 1.0
    for _ in range(500):
        c = q["kc"] * F * e ** q["n"]; p = c / (c + q["ks"]); F = (q["kF"] - q["y_r"] * q["d"] * e) / (q["kF"] + q["y"] * q["kc"] * e ** q["n"] * (1 - p))
    return e, p, F
def growth(q, ks=np.linspace(0.005, 1.5, 300), const=False):
    e, p, F = ss(q); i = q["i0"]; r = q["d"] * e / (F * i); L2 = q["Lsc"] ** 2
    re = q["n"] * q["kc"] * F * e ** (q["n"] - 1) * (1 - p); rF = q["kc"] * e ** q["n"] * (1 - p); rp = q["kc"] * F * e ** q["n"]
    yr = 0 if const else q["y_r"]; ri = 0 if const else r * i
    out = []
    for k in ks:
        k2 = k * k * L2
        J = np.array([[-q["De"] * k2 - q["d"], q["chi"] * e * (1 - e) * k2, ri, r * F],
                      [re, -q["Dp"] * k2 - rp - q["ks"], rF, 0],
                      [-q["y"] * re, q["y"] * rp, -q["DF"] * k2 - q["y"] * rF - q["kF"] - yr * ri, -yr * r * F],
                      [q["d"], 0, -ri, -q["Di"] * k2 - r * F]])
        out.append(np.linalg.eigvals(J).real.max())
    out = np.array(out); j = out.argmax(); return out[j], ks[j]
q = dict(De=0.1, chi=3, kc=2, ks=1, DF=2, y=1, kF=0.2, Dp=1, n=2, d=0.003, Lsc=3, e0=0.12, i0=0.03, Di=1.0, y_r=1.0)
q.update(json.loads(sys.argv[1]) if len(sys.argv) > 1 else {})
print("fuel-powered:", growth(q)); print("const control:", growth(q, const=True))
q0 = dict(q, i0=1e9 ** -1); 
