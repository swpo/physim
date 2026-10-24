"""Parity of xgenome.step with blobkit.genome.run_genome on m4 (noise-free, f64)."""
import json, sys, time
import numpy as np
sys.path.insert(0, "/home/user/physim/packages/blobkit")
from blobkit import genome as G
import xgenome as X
g = json.load(open("/home/user/physim/packages/blobkit/blobkit/data/worlds/m4.json"))
N, dx = 96, 0.5
F0 = G.state_vacuum(g, N); F0 = G.poke(F0, g, 0, 20, 24, 2.0, 3.0, dx)
T = 20.0
out = G.run_genome(g, F=F0, L=N*dx, T=T, save_fields=True, stop_all_dead=False)
S = X.make_state(g, N, F=F0.copy())
t0 = time.time()
for _ in range(int(round(T/0.02))): X.step(S)
print("max abs diff", np.abs(S["F"]-out["fields"]).max(), "field range", np.ptp(out["fields"][0]), "xg wall", time.time()-t0, "bk wall", out["wall_s"])
