"""(c45) Coexistence rule of 20261026T1511-c42-arena-heldout applied to drive.py json files: coexist if predators are
present (n_pred > 0) at every count from t=6000 to 12000 and prey droplets present (n_prey > 0) at >= 50% of those counts.
usage: rule.py files.json..."""
import sys, json, numpy as np
res = {}
for f in sys.argv[1:]:
    d = json.load(open(f)); R = np.array(d["rows"]); t = R[:, 0]; late = t >= 6000
    pred_alive = R[R[:, 2] > 0, 0].max() if (R[:, 2] > 0).any() else -1
    pf = (R[late, 1] > 0).mean(); qf = (R[late, 2] > 0).mean()
    co = bool(qf == 1.0 and pf >= 0.5)
    res.setdefault(d["size"], []).append(co)
    print(d["size"], d["seed"], "pred_last_alive", pred_alive, "prey_frac_late %.2f" % pf, "pred_frac_late %.2f" % qf, "coexist", co,
          "final prey/pred", int(R[-1, 1]), int(R[-1, 2]))
for L, v in sorted(res.items()): print(L, "coexisting %d/%d" % (sum(v), len(v)))
