"""Run the claim's world.py (unchanged, defaults) to time T and save the state. usage: python mkstate.py SEED T OUT.npz"""
import sys, importlib.util, numpy as np
spec = importlib.util.spec_from_file_location("w", "/home/user/physim/research/alife/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py")
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, T, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
s = w.init(seed, w.META["size"])
while s["t"] < T - 1e-9:
    w.step(s)
np.savez(out, e=s["e"], p=s["p"], F=s["F"], s=s["s"], t=s["t"])
print("saved", out, s["t"])
