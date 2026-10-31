"""Correlated noise level check: 50 tu from the prepared state at dt 0.1, sd 0.01, ell 2 (two members) and noise 0;
body counts (labkit-style e > 0.5 periodic 8-connected, area >= 6), field ranges, picture of e and s at 50 tu."""
import json, sys, time
sys.argv = sys.argv[:1]
import numpy as np
import cconv as K
C, LW = K.C, K.LW
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
st, info = C.prepared()
res, finals = {}, {}
for name, w, seed in (("noise0", K.world(sd=0.0, ell=0.0), 11), ("corr_s11", K.world(), 11), ("corr_s12", K.world(), 12)):
    t0 = time.process_time()
    sim, rec = C.run_stepper(w, st, 2500, 50, seed=seed)
    res[name] = dict(cpu_s=round(time.process_time() - t0, 1), bodies_by_tu=[(r["tu"], r.get("bodies")) for r in rec][::5],
                     max_over_run={f: round(max(r["ranges"][f][1] for r in rec), 4) for f in K.FIELDS},
                     min_over_run={f: round(min(r["ranges"][f][0] for r in rec), 5) for f in K.FIELDS},
                     finite=all(r["finite"] for r in rec))
    finals[name] = sim["F"]
    print(name, json.dumps(res[name]), flush=True)
for name in ("corr_s11", "corr_s12"):
    res[name]["rms_diff_vs_noise0_50tu"] = {f: round(float(np.sqrt(((finals[name][i] - finals["noise0"][i]) ** 2).mean())), 5) for i, f in enumerate(K.FIELDS)}
res["member_rms_diff_50tu"] = {f: round(float(np.sqrt(((finals["corr_s11"][i] - finals["corr_s12"][i]) ** 2).mean())), 5) for i, f in enumerate(K.FIELDS)}
old = json.loads((C.OUT / "noise.json").read_text())
res["white_0.01_previous_runner"] = dict(member_rms_diff=old["0.01/member_rms_diff"], max_e=[old["0.01/seed11"]["max_e"], old["0.01/seed12"]["max_e"]])
json.dump(res, open(K.OUT / "noiselevel.json", "w"), indent=1)
fig, ax = plt.subplots(2, 3, figsize=(9, 6))
for j, name in enumerate(finals):
    ax[0, j].imshow(finals[name][0], cmap="magma", vmin=0, vmax=1); ax[0, j].set_title(f"{name} e at 50 tu", fontsize=8)
    ax[1, j].imshow(finals[name][3], cmap="viridis", vmin=0, vmax=45); ax[1, j].set_title(f"{name} s at 50 tu", fontsize=8)
    for a in ax[:, j]:
        a.axis("off")
fig.tight_layout(); fig.savefig(K.OUT / "noiselevel.png", dpi=70)
print(json.dumps({k: v for k, v in res.items() if not k.startswith(("noise0", "corr"))}, indent=1))
