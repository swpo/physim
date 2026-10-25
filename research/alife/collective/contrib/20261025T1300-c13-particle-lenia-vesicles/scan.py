import sys, os, json, time, importlib.util as u, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
cfgs = [json.loads(a) for a in sys.argv[2:]]; out = sys.argv[1]; T = 6000; snaps = [0, 500, 2000, 6000]
fig, ax = plt.subplots(len(cfgs), len(snaps), figsize=(3 * len(snaps), 3 * len(cfgs)), squeeze=False)
for a, cfg in enumerate(cfgs):
    os.environ["WORLD_P"] = json.dumps(cfg)
    s = u.spec_from_file_location("w", "world.py"); w = u.module_from_spec(s); s.loader.exec_module(w)
    st = w.init(0, (128, 128))
    for n in range(T + 1):
        if n in snaps:
            b = ax[a, snaps.index(n)]; p = st["p"]
            Ui = w.energy_terms(p)[5]
            b.scatter(p[:, 1], p[:, 0], s=1, c=Ui, cmap="viridis", vmin=0, vmax=1); b.set_xlim(0, w.P["L"]); b.set_ylim(0, w.P["L"]); b.set_aspect(1)
            b.set_title(f"{cfg} t={n*w.P['dt']:.0f} U={Ui.mean():.2f}", fontsize=6); b.set_xticks([]); b.set_yticks([])
        if n < T: w.step(st)
plt.tight_layout(); plt.savefig(out, dpi=70)
