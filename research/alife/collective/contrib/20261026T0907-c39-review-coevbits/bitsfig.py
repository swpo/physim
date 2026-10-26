"""Genotype-level view of a coevbits run: consensus bits of births per window for prey and predators,
Hamming distance between the two consensuses, and turnover of the dominant genotype.
usage: bitsfig.py tag seed [twin_tag]  -> data/<tag>_s<seed>_bits.png and _bits.json"""
import sys, json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

W = 2000


def windows(tag, seed):
    d = np.load(f"data/{tag}_s{seed}.npz"); m = json.load(open(f"data/{tag}_s{seed}.json")); log = d["log"].astype(np.float64)
    nb = int(m["prm"]["nb"]); T = int(m["t_end"]) // W * W; out = {}
    for sp in (0, 1):
        b = log[(log[:, 1] == sp) & (log[:, 2] == 1)]; t = b[:, 0].astype(int); g = b[:, 5].astype(np.int64)
        bits = ((g[:, None] >> np.arange(nb)) & 1).astype(float); w = t // W; nw = T // W
        cons = np.full((nw, nb), np.nan); dom = np.full(nw, -1, np.int64); domsh = np.zeros(nw); ngen = np.zeros(nw, int)
        for i in range(nw):
            s = w == i
            if not s.any(): continue
            cons[i] = bits[s].mean(0); u, c = np.unique(g[s], return_counts=True)
            dom[i] = u[c.argmax()]; domsh[i] = c.max() / c.sum(); ngen[i] = len(u)
        out[sp] = dict(cons=cons, dom=dom, domsh=domsh, ngen=ngen)
    return out, nb, T


def main():
    tag, seed = sys.argv[1], int(sys.argv[2]); twin = sys.argv[3] if len(sys.argv) > 3 else None
    o, nb, T = windows(tag, seed); x = np.arange(T // W) * W
    fig, ax = plt.subplots(2, 3, figsize=(17, 7))
    for j, (sp, nm) in enumerate(((0, "prey"), (1, "predator"))):
        ax[0, j].imshow(o[sp]["cons"].T, aspect="auto", cmap="coolwarm", vmin=0, vmax=1, extent=[0, T, nb - 0.5, -0.5], interpolation="nearest")
        ax[0, j].set_title(f"{nm}: share of births with bit k = 1 per {W} steps", fontsize=9); ax[0, j].set_ylabel("bit")
    pc, qc = o[0]["cons"], o[1]["cons"]
    dist = np.nansum(np.abs(np.round(pc) - np.round(qc)), 1); dist[np.isnan(qc).all(1)] = np.nan
    ax[0, 2].plot(x, dist, label="real"); ax[0, 2].set_title("Hamming distance prey vs predator consensus", fontsize=9)
    res = {}
    for sp, nm in ((0, "prey"), (1, "pred")):
        dm = o[sp]["dom"]; changes = int(np.sum(dm[1:] != dm[:-1])); seen = set(); ret = 0
        for i in range(1, len(dm)):
            if dm[i] != dm[i - 1] and dm[i] in seen: ret += 1
            seen.add(int(dm[i - 1]))
        res[nm] = dict(dominant_changes=changes, dominant_returns=ret, distinct_dominants=len(set(dm.tolist()) - {-1}),
                       mean_dom_share=float(o[sp]["domsh"].mean()))
        ax[1, 0].plot(x, o[sp]["domsh"], label=f"{nm} real"); ax[1, 1].plot(x, o[sp]["ngen"], label=f"{nm} real")
    if twin:
        t2, _, _ = windows(twin, seed)
        for sp, nm in ((0, "prey"), (1, "pred")):
            ax[1, 0].plot(x[:len(t2[sp]["domsh"])], t2[sp]["domsh"], ":", label=f"{nm} twin"); ax[1, 1].plot(x[:len(t2[sp]["ngen"])], t2[sp]["ngen"], ":", label=f"{nm} twin")
            dm = t2[sp]["dom"]; res[nm + "_twin"] = dict(dominant_changes=int(np.sum(dm[1:] != dm[:-1])), distinct_dominants=len(set(dm.tolist()) - {-1}),
                                                         mean_dom_share=float(t2[sp]["domsh"].mean()))
        d2 = np.nansum(np.abs(np.round(t2[0]["cons"]) - np.round(t2[1]["cons"])), 1); ax[0, 2].plot(x[:len(d2)], d2, ":", label="twin")
    ax[0, 2].legend(fontsize=7); ax[1, 0].set_title("share of births in the dominant genotype", fontsize=9); ax[1, 0].legend(fontsize=7)
    ax[1, 1].set_title("distinct genotypes born per window", fontsize=9); ax[1, 1].legend(fontsize=7); ax[1, 1].set_yscale("log")
    ax[1, 2].axis("off"); ax[1, 2].text(0, 1, json.dumps(res, indent=1), va="top", family="monospace", fontsize=7)
    fig.suptitle(f"coevbits {tag} seed {seed} (windows of {W} steps)", fontsize=10); fig.tight_layout()
    fig.savefig(f"data/{tag}_s{seed}_bits.png", dpi=80); json.dump(res, open(f"data/{tag}_s{seed}_bits.json", "w"), indent=1); print(json.dumps(res))


if __name__ == "__main__":
    main()
