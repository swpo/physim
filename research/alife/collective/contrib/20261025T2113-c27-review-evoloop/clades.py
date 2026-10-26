"""Founder-clade shares and per-kind demography from evo_track.py event logs (c27).
Founders are the loops alive at t=0 (born with parent None at t=0); every later loop inherits its parent's root.
Loops born with no parent within rmax are 'orphans' (root None)."""
import json, sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out = {}
fig, axs = plt.subplots(2, 5, figsize=(20, 6.5))
for r, arm in enumerate(("mix", "neu")):
    for c, sd in enumerate((21, 22, 23, 25, 26)):
        d = json.load(open(f"runs/{arm}_s{sd}.json")); ev = d["events"]
        root, kind0, alive = {}, {}, {}
        series = []
        T = d["T"]; tt = 0; idx = 0
        ev.sort(key=lambda e: e["t"])
        roots = []
        for e in ev:
            if e["type"] == "birth":
                if e["t"] == 0: root[e["id"]] = e["id"]; roots.append(e["id"]); kind0[e["id"]] = e["area"]
                else: root[e["id"]] = root.get(e["parent"]) if e["parent"] is not None else None
                alive[e["id"]] = e["area"]
            elif e["type"] == "death": alive.pop(e["id"], None)
            elif e["type"] == "convert": alive[e["id"]] = e["to"]
        # replay for series
        alive = {}; series = []; nxt = 0
        for e in ev + [{"t": T + 1, "type": "end"}]:
            while nxt <= e["t"] and nxt <= T:
                cnt = {rt: sum(1 for k in alive if root.get(k) == rt) for rt in roots}
                kinds = {}
                for k, a in alive.items(): kinds[a] = kinds.get(a, 0) + 1
                series.append([nxt, len(alive)] + [cnt[rt] for rt in roots] + [kinds.get(4, 0) + kinds.get(3, 0) + kinds.get(2, 0)])
                nxt += 500
            if e["type"] == "birth": alive[e["id"]] = e["area"]
            elif e["type"] == "death": alive.pop(e["id"], None)
            elif e["type"] == "convert": alive[e["id"]] = e["to"]
        S = np.array(series, float)
        ax = axs[r, c]
        for j, rt in enumerate(roots): ax.plot(S[:, 0], S[:, 2 + j], label=f"clade of founder side {kind0[rt]}")
        ax.plot(S[:, 0], S[:, 1], "k:", lw=0.8, label="all loops")
        ax.plot(S[:, 0], S[:, -1], "g--", lw=0.8, label="loops of side <= 4")
        ax.set_title(f"{arm} seed {sd}", fontsize=9); ax.legend(fontsize=6); ax.set_xlabel("step")
        sh = S[:, 2] / np.maximum(S[:, 2] + S[:, 3], 1)
        nb = {}
        for e in ev:
            if e["type"] == "birth" and e["t"] > 0: nb.setdefault(e["parent_area"], [0, 0]); nb[e["parent_area"]][0] += 1; nb[e["parent_area"]][1] += e["area"] == e["parent_area"]
        out[f"{arm}_s{sd}"] = {"founder_sides": [kind0[rt] for rt in roots],
            "clade_counts_at": {int(S[i, 0]): [int(S[i, 2]), int(S[i, 3])] for i in range(0, len(S), 10)},
            "first_founder_clade_share_t10k_20k_40k": [round(float(sh[min(k, len(sh) - 1)]), 2) for k in (20, 40, 80)],
            "clade_extinct_step": [float(S[1:][np.nonzero(S[1:, 2 + j] == 0)[0][0], 0]) if (S[1:, 2 + j] == 0).any() else None for j in range(len(roots))],
            "orphan_births": sum(1 for e in ev if e["type"] == "birth" and e["t"] > 0 and e["parent"] is None),
            "births_by_parent_side_[n,breedtrue]": {str(k): v for k, v in sorted(nb.items(), key=lambda z: (z[0] is None, z[0]))}}
        print(arm, sd, out[f"{arm}_s{sd}"]["founder_sides"], "share of first founder's clade at 10k/20k/40k:", out[f"{arm}_s{sd}"]["first_founder_clade_share_t10k_20k_40k"], "extinct:", out[f"{arm}_s{sd}"]["clade_extinct_step"], "orphans", out[f"{arm}_s{sd}"]["orphan_births"])
fig.suptitle("evoloop head-to-head (c27): top, one side-11 and one side-4 founder; bottom, two side-11 founders (neutral pair). Live loops per founder clade", fontsize=9)
fig.tight_layout(); fig.savefig("clades.png", dpi=65)
json.dump(out, open("clades.json", "w"), indent=1)
