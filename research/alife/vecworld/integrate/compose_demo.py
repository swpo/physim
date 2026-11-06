"""Composition operators on the Flow-Lenia worlds (writes results/compose_demo.json).
  stack:  level 2 = Phi2(Phi_objects): object count, mean speed, kinetic proxy sum m|v|^2, close pairs
  concat: A_gliders/objects (+) B_swarm/objects, jointly anonymised, k summed (16)
  stride: two ticks of A_gliders/objects as one (40 sub-steps)"""
import json
import time

import numpy as np

import lenia_world as LW
vw = LW.vw

out = {}
sA, pA = LW.make_specs("A_gliders")
sB, pB = LW.make_specs("B_swarm")
K = pA["tracker"].K


def phi2(h1, m2):
    S = h1.reshape(len(h1), K, LW.NF)
    pres = S[:, :, 0] > 0.5
    sp = np.hypot(S[:, :, 10], S[:, :, 11])
    n = pres.sum(1)
    ke = (S[:, :, 1] * sp ** 2 * pres).sum(1)
    E = 128 / (2 * np.pi)
    cx = np.arctan2(S[:, :, 4], S[:, :, 3]) * E
    cy = np.arctan2(S[:, :, 6], S[:, :, 5]) * E
    close = np.zeros(len(h1))
    for b in range(len(h1)):
        idx = np.flatnonzero(pres[b])
        for i in range(len(idx)):
            for j in range(i + 1, len(idx)):
                d = np.hypot((cx[b, idx[i]] - cx[b, idx[j]] + 64) % 128 - 64, (cy[b, idx[i]] - cy[b, idx[j]] + 64) % 128 - 64)
                close[b] += d < 1.6 * (S[b, idx[i], 7] + S[b, idx[j], 7]) + 2
    return np.stack([n, (sp * pres).sum(1) / np.maximum(n, 1), ke, close], 1)


t0 = time.time()
w2 = vw.VectorWorld(vw.stack(sA["objects"], phi2, 4, name="A_gliders/level2"), 1)
o = [w2.reset(5)] + [w2.step(None) for _ in range(4)]
out["stack"] = {"card_n_obs": w2.card()["n_obs"], "obs": np.array(o).tolist(), "seconds": time.time() - t0}
t0 = time.time()
wc = vw.VectorWorld(vw.concat(sA["objects"], sB["objects"], name="A+B objects"), 2)
oc = wc.reset(5)
a = wc.designer.random_program(np.random.default_rng(0), 1, rate=1.0)
o1 = wc.step(a[0][1] if a else None)
m = wc.designer.state()["h0"]
out["concat"] = {"card": {k: wc.card()[k] for k in ("n_in", "n_obs")}, "inputs_k": wc.spec.inputs.k,
                 "mass_A": float(m[:32768].sum()), "mass_B": float(m[32768:].sum()), "seconds": time.time() - t0}
t0 = time.time()
ws = vw.VectorWorld(vw.stride(sA["objects"], 2), 3)
ws.reset(5)
ws.step(None)
out["stride"] = {"name": ws.spec.name, "noise_dim": ws.spec.noise_dim, "seconds": time.time() - t0}
json.dump(vw.jsonable(out), open("results/compose_demo.json", "w"), indent=1)
print(json.dumps(vw.jsonable(out))[:1500])
