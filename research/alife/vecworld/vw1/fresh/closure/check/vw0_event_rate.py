"""Checker (old-page claim only, VW-0 data read only): share of live slot-ticks with a tracker event at
t+1 in the VW-0 A_gliders base runs, at the 72 saved test states vs at every tick (checker's rule)."""
import glob, json
import numpy as np
fs = sorted(glob.glob("/home/user/evalwork/vecworld/integrate/data/A_gliders/base_*.npz"))
NF, K = 12, 12
tot = {"test": [0, 0], "every": [0, 0]}
per = []
for f in fs:
    d = np.load(f)
    Y, tab = d["Yo"], d["tab"]
    p = Y.reshape(len(Y), K, NF)[..., 0] > 0.5
    ev = tab[..., 3]
    Lv = p[:-1] | p[1:]; E = ((ev[1:] != 0) | (p[:-1] != p[1:])) & Lv
    tot["every"][0] += int(E.sum()); tot["every"][1] += int(Lv.sum())
    ts = d["st_tick"] - int(d["burn_in"])
    e1 = int(E[ts].sum()); l1 = int(Lv[ts].sum())
    tot["test"][0] += e1; tot["test"][1] += l1
    per.append((e1, l1))
per = np.array(per); rng = np.random.default_rng(0)
bs = [per[rng.choice(len(per), len(per))].sum(0) for _ in range(2000)]
out = {"n_traj": len(fs), "test_states_share": tot["test"][0] / tot["test"][1], "test_states_counts": tot["test"],
       "test_states_share_se": float(np.std([b[0] / b[1] for b in bs])),
       "every_tick_share": tot["every"][0] / tot["every"][1], "every_tick_counts": tot["every"]}
print(out)
json.dump(out, open("/home/user/evalwork/vecworld/vw1/fresh/closure/check/vw0_event_rate.json", "w"), indent=1)
