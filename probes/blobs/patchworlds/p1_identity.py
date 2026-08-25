"""p1_identity.py — P1 IDENTITY null test + smoke row.

Three runs of the SAME physical world (M0, one poked blob, T=300):
  ref : G.run_genome            (unpatched reference engine)
  scal: run_patched, pmaps={}   (fork, scalar path)
  fmap: run_patched, forcemap   (fork, EVERY param a constant map via rho blend A|A)
Gate: bit-identity of final fields + all recorded series. Honest fallback:
report max|diff| if not bit-equal.
"""
import numpy as np, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch_lib as P
G = P.G

L, dx, T = 96.0, 0.5, 300.0
N = int(round(L / dx))
g = G.ref_M0()

rho = P.rho_band(N, dx, 24.0, 72.0, 3.0)
gf, pm_null = P.blend_genomes(g, g, rho)
gf2, pm_force = P.blend_genomes(g, g, rho, forcemap=True)
print("null pmaps:", {k: list(v) for k, v in pm_null.items()})
print("force pmaps keys:", {k: len(v) for k, v in pm_force.items()})

F0 = G.state_vacuum(g, N)
F0 = G.poke(F0, g, 0, 40.0, 40.0, 2.0, 3.0, dx)

kw = dict(L=L, dx=dx, T=T, rec_tu=5.0, save_fields=True)
ref = G.run_genome(g, F=F0.copy(), **kw)
scal = P.run_patched(g, pmaps={}, F=F0.copy(), **kw)
fmap = P.run_patched(gf2, pmaps=pm_force, F=F0.copy(), **kw)

def cmp(a, b, name):
    d = float(np.max(np.abs(a["fields"] - b["fields"])))
    bit = bool(np.array_equal(a["fields"], b["fields"]))
    pa, pb = np.array(a["pos0"][-1]), np.array(b["pos0"][-1])
    dp = float(np.max(np.abs(pa - pb))) if pa.size and pb.size else -1.0
    na_, nb_ = a["ncomp0"].tolist(), b["ncomp0"].tolist()
    print(f"{name}: bit={bit} max|dF|={d:.3e} max|dpos|={dp:.3e} ncomp_eq={na_==nb_}")
    return dict(bit=bit, max_dF=d, max_dpos=dp, ncomp_eq=na_ == nb_)

c1 = cmp(ref, scal, "ref-vs-scalar")
c2 = cmp(ref, fmap, "ref-vs-forcemap")
c3 = cmp(scal, fmap, "scalar-vs-forcemap")
area = ref["area0"][-1]
print("M0 blob area(final):", area, "ncomp:", int(ref["ncomp0"][-1]))

P.log(dict(test="P1_identity", world="M0", L_px=N, T=T,
           gate="bit-identity of fields+series across ref/scalar/forcemap paths",
           ref_area_final=area, ref_ncomp_final=int(ref["ncomp0"][-1]),
           ref_vs_scalar=c1, ref_vs_forcemap=c2, scalar_vs_forcemap=c3,
           verdict=("PASS-bit" if c1["bit"] and c2["bit"] else
                    ("PASS-eps" if max(c1["max_dF"], c2["max_dF"]) < 1e-10 else "FAIL"))))
print("logged P1")
