
"""g3_sigma_staircase.py -- staircase step position vs sigma (micro price).
Up-sweep only (one ramp): record C at the 5->6 up-jump for sigma in 5 values.
Theory: k_c(C)=k_c(1)*C^sigma -> jump when C = (k_jump/k_c1)^(1/sigma):
log C_jump ~ (1/sigma), smooth and monotone (for k_jump > k_c(1)).
"""
import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from morpho_sim import simulate

out = []
for sigma in [0.7, 0.85, 1.0, 1.2, 1.4]:
    p = dict(ny=8, nx=64, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=11.0, Dc=10.0,
             sigma=sigma, mode="ramp", ramp=(0.7, 1.6, 12000.0, 20.0), C0=0.7,
             steps=60000, meas_every=25, seed=1, k_ref=0.62, noise_amp=2e-3,
             Cmin=0.4, Cmax=1.9)
    r = simulate(p)
    t, n, C = r["t"], r["nz"].astype(int), r["Cm"]
    jump56 = None; jumps = []
    for i in range(1, len(n)):
        if t[i] > 150 and n[i] != n[i - 1]:
            jumps.append((int(n[i-1]), int(n[i]), round(float(C[i]), 4)))
            if n[i - 1] == 5 and n[i] == 6 and jump56 is None:
                jump56 = float(C[i])
    row = dict(sigma=sigma, C_jump_5to6=round(jump56, 4) if jump56 else None,
               pred_exponent=round((jump56 ** sigma), 4) if jump56 else None,
               all_jumps=jumps[:8])
    out.append(row)
    print(row, flush=True)
with open("results_sigma_staircase.json", "w") as f:
    json.dump(out, f, indent=1)
print("done")
