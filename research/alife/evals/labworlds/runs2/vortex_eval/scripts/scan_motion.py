import json, sys, numpy as np
sys.path.insert(0, "/home/user/evalwork/vortex_eval/scripts")
import common as C, design as D
s = D.load_state(f"{C.OUT}/prep/state_s31_t580.pkl")
o = D.oracle(s, [D.device(0, [91.4, 122.1]), D.device(1, [72, 40])])
fr, _ = D.capture(o, [], seed=4300)
np.savez_compressed(f"{C.OUT}/mech/sham580_om.npz", **{f"t{int(t)}": fr[t][0] for t in sorted(fr) if t % 5 == 0})
lab, bs = D.bodies(fr[0.0][0])
rows = []
for b in bs:
    hist, ev = D.follow(fr, [b["cy"], b["cx"]])
    ok = all(h.get("n") == 1 for h in hist)
    end = hist[-1]
    if end.get("n", 0) == 0:
        rows.append(dict(cy=b["cy"], cx=b["cx"], sign=b["sign"], area=b["area"], fate="died")); continue
    path = [(h["cy"], h["cx"]) for h in hist]
    disp = np.hypot(D.wrap(end["cy"] - b["cy"]), D.wrap(end["cx"] - b["cx"]))
    steps = [float(np.hypot(D.wrap(path[i + 1][0] - path[i][0]), D.wrap(path[i + 1][1] - path[i][1]))) for i in range(len(path) - 1)]
    rows.append(dict(cy=round(b["cy"], 1), cx=round(b["cx"], 1), sign=b["sign"], area=b["area"], single=ok, disp=round(float(disp), 1),
                     pathlen=round(sum(steps), 1), d_dev0=round(float(np.hypot(D.wrap(b["cy"] - 91.4), D.wrap(b["cx"] - 122.1))), 1),
                     traj=[(round(h["cy"], 1), round(h["cx"], 1)) for h in hist[::5]], circ=[round(h["circ"], 1) for h in hist[::10]]))
rows.sort(key=lambda r: -r.get("disp", 0))
json.dump(rows, open(f"{C.OUT}/mech/motion580.json", "w"), indent=0)
for r in rows[:14]:
    print({k: v for k, v in r.items() if k != "traj"})
