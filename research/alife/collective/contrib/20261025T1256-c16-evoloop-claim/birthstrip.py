"""Replay an evoloop run and show randomly chosen births: crops centred between parent and daughter holes,
at t_birth - 300, t_birth (hole closes), t_birth + 300. Rows: on-kind births, then off-kind (mutant) daughters."""
import sys, os, json, importlib.util, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
COL = np.array([[0,0,0],[0,0,255],[255,0,0],[0,255,0],[255,255,0],[255,0,255],[255,255,255],[0,255,255],[255,128,0]])/255
trk, t0, t1, n_on, n_off, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
r = json.load(open(trk)); rng = np.random.default_rng(0)
B = [e for e in r["events"] if e["type"] == "birth" and e["parent"] is not None and t0 <= e["t"] <= t1]
on = [e for e in B if e["area"] == e["parent_area"]]; off = [e for e in B if e["area"] != e["parent_area"]]
pick = [on[i] for i in rng.choice(len(on), n_on, replace=False)] + [off[i] for i in rng.choice(len(off), n_off, replace=False)]
offs = (-300, 0, 300); want = {}
for k, e in enumerate(pick):
    for o in offs: want.setdefault(e["t"] + o, []).append((k, o))
os.environ["WORLD_P"] = json.dumps(r["params"])
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(trk)), "world.py")); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
L = r["L"]; s = w.init(r["seed"], (L, L)); crops = {}; R = 24
for t in range(0, max(want) + 1):
    if t in want:
        for k, o in want[t]:
            e = pick[k]; a = np.array(e["c"]); b = np.array(e["pc"]); d = (a - b + L / 2) % L - L / 2; m = (b + d / 2) % L
            ii = (int(m[0]) + np.arange(-R, R)) % L; jj = (int(m[1]) + np.arange(-R, R)) % L
            crops[(k, o)] = s["g"][np.ix_(ii, jj)].copy()
    w.step(s)
fig, ax = plt.subplots(len(pick), 3, figsize=(6, 2.1 * len(pick)))
for k, e in enumerate(pick):
    for j, o in enumerate(offs):
        ax[k, j].imshow(COL[crops[(k, o)]], interpolation='nearest'); ax[k, j].set_xticks([]); ax[k, j].set_yticks([])
        a = np.array(e["c"]); b = np.array(e["pc"]); d = (a - b + L / 2) % L - L / 2
        ax[k, j].plot(R + d[1] / 2, R + d[0] / 2, '+', color='lime', ms=10, mew=2)    # daughter hole centre
        ax[k, j].plot(R - d[1] / 2, R - d[0] / 2, 'x', color='white', ms=8, mew=2)    # parent hole centre
        ax[k, j].set_title(f"t={e['t'] + o}" + (f"  side {e['parent_area']}->{e['area']}" if o == 0 else ""), fontsize=7)
fig.suptitle(f"seed {r['seed']}: {n_on} random on-kind births, then {n_off} random off-kind daughters, t in [{t0},{t1}]\nwhite x = parent hole, green + = daughter hole (closes at the middle frame)", fontsize=8, y=0.995)
plt.tight_layout(rect=(0, 0, 1, 0.985)); plt.savefig(out, dpi=80)
