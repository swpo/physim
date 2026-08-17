
import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower/ecoevo")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from ecoevo_core import *   # brings lap, theory_to_raw, DT etc.
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower"
TC = json.load(open(WD + "/tcstar.json"))
raw = theory_to_raw(TC)

def frozen_gradient(raw, G, c, L=64, nticks=36000, seed=0, cut=0.4):
    """Run eco dynamics with uniform frozen genotype G; accumulate the
    biomass-weighted marginal invasion gradient s(G) = <P * dgrow/dG>/<P> .
    Frozen-G world == round-1 engine with a2->G a2, b2->G b2, d2->d2+c(G-1)."""
    rng = np.random.default_rng(seed)
    a1, b1, d1 = raw["a1"], raw["b1"], raw["d1"]
    a2, b2 = raw["a2"], raw["b2"]
    d2e = raw["d2"] + c * (G - 1.0)
    DRl, DH, DP, nu = raw["DR"], raw["DH"], raw["DP"], raw["nu"]
    r0, h0, p0 = 0.6, 0.2, 0.1
    accR = accH = accP = 0.0; nacc = 0
    for i in range(12000):
        f1o = a1 * r0 / (1 + b1 * r0); f2o = (G * a2) * h0 / (1 + (G * b2) * h0)
        r0 += DT * (r0 * (1 - r0) - f1o * h0)
        h0 += DT * ((f1o - d1) * h0 - f2o * p0)
        p0 += DT * ((f2o - d2e) * p0)
        r0 = min(max(r0, 1e-9), CAP); h0 = min(max(h0, 1e-9), CAP); p0 = min(max(p0, 1e-9), CAP)
        if i >= 8000: accR += r0; accH += h0; accP += p0; nacc += 1
    R0, H0, P0 = accR / nacc, accH / nacc, accP / nacc
    if P0 < 1e-7:
        return dict(status="P_dead_warm", s=None)
    R = R0 * (0.8 + 0.4 * rng.random((L, L)))
    H = H0 * (0.7 + 0.6 * rng.random((L, L)))
    P = P0 * (0.7 + 0.6 * rng.random((L, L)))
    num = 0.0; den = 0.0; nsamp = 0
    t_cut = int(nticks * cut)
    meanP_end = []
    for t in range(nticks):
        f1 = a1 * R / (1.0 + b1 * R)
        sat = 1.0 + (G * b2) * H
        f2 = (G * a2) * H / sat
        Rn = R + DT * (R * (1.0 - R) - f1 * H + DRl * lap(R))
        Hn = H + DT * ((f1 - d1) * H - f2 * P + DH * lap(H))
        Pn = P + DT * ((f2 - d2e) * P + DP * lap(P))
        if nu > 0 and t % 10 == 0:
            s10 = np.sqrt(10 * DT)
            Hn += nu * s10 * np.sqrt(np.maximum(Hn, 0)) * rng.standard_normal((L, L))
            Pn += nu * s10 * np.sqrt(np.maximum(Pn, 0)) * rng.standard_normal((L, L))
        R = np.clip(Rn, FLOOR, CAP); H = np.clip(Hn, FLOOR, CAP); P = np.clip(Pn, FLOOR, CAP)
        if t >= t_cut and t % 5 == 0:
            dgdG = a2 * H / sat ** 2 - c     # d(growth)/dG at resident G
            num += float((P * dgdG).sum()); den += float(P.sum()); nsamp += 1
            if t % 200 == 0: meanP_end.append(float(P.mean()))
    if den <= 0 or np.mean(meanP_end[-20:]) < 1e-6:
        return dict(status="P_extinct", s=None)
    return dict(status="ok", s=num / den, meanP=float(np.mean(meanP_end[-20:])))

out = {}
for c in (0.005, 0.01, 0.02, 0.03):
    for G in (0.6, 0.8, 1.0, 1.3, 1.7, 2.2, 3.0):
        t0 = time.time()
        r = frozen_gradient(raw, G, c)
        out[f"c={c},G={G}"] = r
        print(f"c={c} G={G}: {r['status']} s={r['s'] and round(r['s'],5)} "
              f"meanP={r.get('meanP') and round(r['meanP'],3)} ({round(time.time()-t0,1)}s)", flush=True)
json.dump(out, open("/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower/ecoevo/gradient_map.json", "w"), indent=1)
print("DONE gradient map")
