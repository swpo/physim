import sys, os, json, importlib.util, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sets = [json.loads(x) for x in sys.argv[2:]]; T = 3000; times = [0, 200, 1000, 2000, 3000]
fig, ax = plt.subplots(len(sets), len(times), figsize=(2 * len(times), 2.1 * len(sets)))
for r, p in enumerate(sets):
    os.environ["WORLD_P"] = json.dumps(p)
    spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
    s = w.init(0, (96, 96))
    for t in range(T + 1):
        if t in times:
            c = times.index(t); a = ax[r, c]; a.imshow(w.fields(s)[1], cmap="magma"); a.set_xticks([]); a.set_yticks([])
            a.set_title((json.dumps(p) + "\n" if c == 0 else "") + f"t={t}", fontsize=6)
        w.step(s)
plt.tight_layout(); plt.savefig(sys.argv[1], dpi=60)
