import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import patch_lib as P
G = P.G
gA = G.ref_M0(); gB = G.ref_M4(5.8)
N = 192; dx = 0.5
rho = P.rho_band(N, dx, 24.0, 72.0, 2.0)
g, pm = P.blend_genomes(gA, gB, rho)
print("pmaps:", {k: list(v) for k, v in pm.items()})
F = P.state_vacuum_map(g, pm, N)
F = G.poke(F, g, 0, 12.0, 24.0, 2.0, 3.0, dx)
t0 = time.time()
r = P.run_patched(g, pm, F=F, L=96.0, dx=dx, T=50.0, rec_tu=5.0)
print("50tu wall:", round(time.time()-t0,2), "s -> 3000tu ~", round((time.time()-t0)*60/60,1), "min")
print("status", r["status"], "ncomp", r["ncomp0"][-1], "area", r["area0"][-1])
