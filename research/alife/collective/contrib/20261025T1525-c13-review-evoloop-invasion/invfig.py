import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(10, 3.4), sharey=True); out = []
for k, (m, lab) in enumerate(((8, "invader: planted side-4 loop"), (15, "neutral: planted side-11 loop"))):
    for s in range(30, 36):
        d = json.load(open(f"census/inv_s{s}_m{m}.json")); C = d["census"]
        t = [c["t"] for c in C]; f4 = [c["hist"][4] / max(c["n"], 1) for c in C]
        ax[k].plot(t, f4, label=f"seed {s}")
        first = next((c["t"] for c in C if c["hist"][4] / max(c["n"], 1) > 0.5), None)
        out.append({"seed": s, "arm": "invader" if m == 8 else "neutral", "side4_majority_at": first, "final_n": C[-1]["n"], "final_side4_share": round(C[-1]["hist"][4] / max(C[-1]["n"], 1), 2), "final_side11": C[-1]["hist"][11]})
    ax[k].set_title(lab, fontsize=9); ax[k].set_xlabel("step"); ax[k].axhline(0.5, color="0.7", lw=0.5)
ax[0].set_ylabel("side-4 share of loops"); ax[1].legend(fontsize=7)
plt.tight_layout(); plt.savefig("invasion_c13.png", dpi=90)
json.dump(out, open("invasion_c13.json", "w"), indent=0)
for o in out: print(o)
