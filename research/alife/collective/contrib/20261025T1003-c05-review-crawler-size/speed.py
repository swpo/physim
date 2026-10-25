"""Speed of a fixed-size crawler (c04 positive-control world) every 20 t, new seed. usage: speed.py 'json' seed"""
import sys, os, json
os.environ["WORLD_P"] = sys.argv[1]
import importlib.util, numpy as np
spec = importlib.util.spec_from_file_location("cr", "../../contrib/20261025T0641-c04-crawler-positive-control/world.py"); c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
seed = int(sys.argv[2]); N = c.P["N"]; dx = c.P["dx"]
s = c.init(seed, (N, N)); L = N * dx
def com(u):
    y, x = np.mgrid[0:N, 0:N] * dx
    return [np.angle((u * np.exp(2j * np.pi * z / L)).sum()) * L / 2 / np.pi for z in (x, y)]
pos = []
for i in range(int(200 / c.P["dt"]) + 1):
    if i % 400 == 0: pos.append(com(s["u"]))
    s = c.step(s) or s
pos = np.array(pos); d = np.diff(pos, axis=0); d = (d + L / 2) % L - L / 2
print(json.dumps({"P": sys.argv[1], "seed": seed, "speeds": np.round(np.hypot(d[:, 0], d[:, 1]) / 20, 2).tolist(), "area": round(float((s["u"] > 0.5).sum() * dx * dx))}))
