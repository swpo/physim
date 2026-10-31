"""Try candidate programs around one vortex: capture fields (1 member), follow the vortex, save crops for strips.

python try_programs.py BODY_ID OUTNAME SEED  (programs defined in PROGRAMS below, device0 at the body, mix diag(3,3,1))
"""
import json, sys
import numpy as np
sys.path.insert(0, "/home/user/evalwork/vortex_eval/scripts")
import common as C
import design as D

import os
ST = os.environ.get("STATE_T")
s = D.load_state(f"{C.OUT}/prep/state_s31_t{ST}.pkl" if ST else f"{C.OUT}/prep/state_s31.pkl")
bs = {b["id"]: b for b in json.load(open(f"{C.OUT}/prep/bodies_s31.json"))}
bid, name, seed = int(sys.argv[1]), sys.argv[2], int(sys.argv[3])
progs = json.loads(sys.argv[4])
d1 = int(sys.argv[5]) if len(sys.argv) > 5 else 1
yx = [float(v) for v in os.environ["SITE"].split(",")] if os.environ.get("SITE") else [bs[bid]["cy"], bs[bid]["cx"]]
d1yx = [float(v) for v in os.environ["D1"].split(",")] if os.environ.get("D1") else [bs[d1]["cy"], bs[d1]["cx"]]
devs = [D.device(0, yx), D.device(1, d1yx)]
MIX = np.diag([3.0, 3.0, 1.0])
crops, summary = {}, {}
for pname, actions in progs.items():
    o = D.oracle(s, devs)
    o._mix = MIX.copy()
    fr, res = D.capture(o, actions, seed=seed)
    hist, ev = D.follow(fr, yx)
    iy = (np.arange(-24, 24) + int(round(yx[0]))) % 128
    ix = (np.arange(-24, 24) + int(round(yx[1]))) % 128
    crops[pname] = np.stack([fr[t][0][np.ix_(iy, ix)] for t in sorted(fr) if t % 5 == 0])
    crops[pname + "_Y"] = np.stack([fr[t][1][np.ix_(iy, ix)] for t in sorted(fr) if t % 5 == 0])
    summary[pname] = dict(split_t=D.persistent_split(hist), n=[h.get("n") for h in hist[::5]],
                          circ=[round(h.get("circ", 0), 1) for h in hist[::5]], d0=res[0][:, ::10, 0, 0].round(3).tolist())
    print(name, pname, "split", summary[pname]["split_t"], "n", summary[pname]["n"], "circ", summary[pname]["circ"], flush=True)
np.savez_compressed(f"{C.OUT}/mech/try_{name}.npz", **crops)
json.dump(dict(body=bid, seed=seed, programs=progs, summary=summary), open(f"{C.OUT}/mech/try_{name}.json", "w"), indent=0)
