"""Smoke test of the agent and designer APIs on the Flow-Lenia VW-0 worlds (writes smoke.json)."""
import json
import sys
import time

import numpy as np

import lenia_world as LW
vw = LW.vw

name = sys.argv[1] if len(sys.argv) > 1 else "A_gliders"
out = {}
specs, parts = LW.make_specs(name)
for phi in ("objects", "coarse"):
    w = vw.VectorWorld(specs[phi], world_seed=7)
    card = w.card()
    t0 = time.time()
    o0 = w.reset(seed=3)
    t_reset = time.time() - t0
    d = w.designer
    st = d.state()
    mass0 = st["h0"].reshape(parts["l0"].shape).sum((1, 2))
    # a legal zero-sum input on the first k coordinates, then free ticks
    inv = LW.inverse_in_map(w)
    S = st["h0"].reshape(parts["l0"].C, -1).sum(0)  # matter per cell (actuator index = cell)
    src = np.argsort(-S)[:4]                         # four densest cells
    snk = np.argsort(S)[:4]                          # four empty cells
    a = {int(inv[i]): -0.5 for i in src}
    a.update({int(inv[i]): 0.5 for i in snk})
    t0 = time.time()
    o1 = w.step(a)
    t_step = time.time() - t0
    mass1 = d.state()["h0"].reshape(parts["l0"].shape).sum((1, 2))
    errs = []
    for bad in ({0: 0.5}, {i: 0.1 for i in range(9)}, {0: 2.0, 1: -2.0}, {0: 0.9, 1: 0.9, 2: -0.9, 3: -0.9, 4: 0.5, 5: -0.5}):
        try:
            w.step(bad)
            errs.append("accepted")
        except vw.InputViolation as e:
            errs.append(str(e)[:120])
    Y = w.run([(0, a), (2, a)], query_times=[1, 3, 5])
    mass2 = d.state()["h0"].reshape(parts["l0"].shape).sum((1, 2))
    rec = {"card": card, "reset_seconds": t_reset, "step_seconds": t_step, "n_obs": int(o0.size),
           "mass_before": mass0.tolist(), "mass_after_input": mass1.tolist(), "mass_after_run": mass2.tolist(),
           "violations": errs, "run_shape": list(Y.shape),
           "obs_changed_by_input_tick": float(np.abs(o1 - o0).sum())}
    if phi == "objects":
        T = parts["tracker"].table(d.state()["m"][None])[0]
        rec["slots"] = [{f: round(float(T[s, i]), 3) for i, f in enumerate(LW.OBJ_FEATURES + LW.SLOT_EXTRA)}
                        for s in range(T.shape[0]) if T[s, 0] > 0.5]
        # component masses below the tracking threshold, for the m_min choice
        tr = parts["tracker"]
        lab, comps = LW.Tracker(parts["l0"], tr.K, 0.5).components(d.state()["h0"])
        rec["all_component_masses"] = sorted(round(c["mass"], 1) for c in comps)
    out[phi] = rec
    print(phi, json.dumps({k: v for k, v in rec.items() if k != "card"}, default=str)[:1500])
json.dump(vw.jsonable(out), open(f"smoke_{name}.json", "w"), indent=1, default=str)
