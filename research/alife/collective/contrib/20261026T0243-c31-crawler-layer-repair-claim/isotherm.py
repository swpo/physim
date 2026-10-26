"""Positive control: frozen disk, conserved s (no source, no decay), uniform start.
Equilibrium of flux = -Ds grad s + Ds beta s(1-s) grad w is the Fermi/Langmuir isotherm
s = 1/(1 + exp(-(beta w + mu))), mu set by conservation (van der Sman & van der Graaf 2006)."""
import os, json, sys, importlib.util
import numpy as np
from scipy.optimize import brentq
beta = float(sys.argv[1]); s0 = float(sys.argv[2])
os.environ["WORLD_P"] = json.dumps({"freeze": 1, "kp": 0.0, "kd": 0.0, "beta": beta, "eta": 0.0, "K": 0.0})
spec = importlib.util.spec_from_file_location("w", "world.py"); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
s = W.init(0, W.META["size"]); s["s"][:] = s0
for k in range(int(sys.argv[3])):
    s = W.step(s)
phi = s["phi"]; w = 4 * phi * (1 - phi); M = s["s"].mean()
mu = brentq(lambda m: (1 / (1 + np.exp(-(beta * w + m)))).mean() - M, -30, 30)
pred = 1 / (1 + np.exp(-(beta * w + mu)))
err = np.abs(s["s"] - pred).max() / pred.max()
print(f"beta={beta} s0={s0} max sim={s['s'].max():.4f} pred={pred.max():.4f} rel maxerr={err:.3f} rim/bulk sim={s['s'].max()/np.median(s['s']):.2f} pred={pred.max()/np.median(pred):.2f}")
j = phi.shape[0] // 2
np.savetxt(f"runs/isotherm_b{beta}_s{s0}.txt", np.c_[np.arange(phi.shape[1]), phi[j], s["s"][j], pred[j]], fmt="%.5f", header="x phi s_sim s_langmuir")
