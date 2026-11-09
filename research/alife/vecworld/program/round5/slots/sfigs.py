"""sfigs -- figures of the round-5 study `slots` (local, matplotlib; reads only the job's small outputs).

usage: python -B sfigs.py JOB_DIR OUT_DIR       (JOB_DIR = a copy of origin/gpu-jobs:jobs/<job>/out)
fig_segmentations.png  the matter field of certification trajectory 0 (half A) at three ticks, the tracker's label
                       map, and the hard masks of the slot encoders certified on that half (token resolution)
fig_agreement.png      agreement with the tracker per Phi (seed means): ARI, matched recall, slots per object,
                       mass / velocity R^2 of the matched slot (direct mask moments and RFF probe of the readout)
fig_ceilings.png       closure ceilings (slot-set family S on 6 numbers per slot) against the horizon
fig_objval.png         objective values on frozen readouts (set, self, rec) per Phi
"""
import json
import os
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import hsv_to_rgb  # noqa: E402

JD, OD = sys.argv[1], sys.argv[2]
os.makedirs(OD, exist_ok=True)
C = json.load(open(os.path.join(JD, "combined.json")))
HZ = C["horizons"]
PAL = np.array([hsv_to_rgb(((i * 0.618034) % 1.0, 0.85, 1.0)) for i in range(13)])
ORDER = ["trk", "km_s6", "km_s3", "km_s6w", "km_s6_p1", "grid", "sam_sup", "sam_set", "sam_set_dg", "sam_set_ws", "sam_set_ws_dg",
         "sam_self", "sam_self_dg", "sam_self_ws", "sam_rec", "sam_rec_ws", "sam_set_sg", "sam_rec_nomem", "sgm_set", "sgm_set_dg",
         "sgm_rec", "sac_set", "sac_set_dg", "sac_self", "sac_rec", "sgc_set", "sgc_rec"]


def groups():
    """name -> list of phi keys (seeds) present in combined.json, in ORDER."""
    g = {}
    for phi in C["phis"]:
        if "@" in phi or phi.startswith("hand_"):
            continue
        m = next(iter(C["phis"][phi]["meta"].values()))
        base = m["config"] if m.get("kind") == "learned" else phi          # seeds of one learned config together
        g.setdefault(base, []).append(phi)
    return {k: sorted(g[k]) for k in ORDER if k in g} | {k: sorted(v) for k, v in g.items() if k not in ORDER}


G = groups()


def smean(phis, f):
    v = []
    for p in phis:
        try:
            x = f(C["phis"][p])
        except (KeyError, TypeError):
            x = None
        if x is not None:
            v.append(x)
    return np.mean(np.asarray(v, float), 0) if v else None


def fig_segmentations(ch="A"):
    fp = os.path.join(JD, "masks", f"_frames__cert{ch}.npz")
    if not os.path.exists(fp):
        return
    fr = np.load(fp)
    S, tmap, ticks = fr["S"], fr["map"].astype(int), fr["ticks"]
    cols = [("matter", None), ("tracker", None)]
    for name in G:
        p = os.path.join(JD, "masks", f"{name}__cert{ch}.npz")
        if not os.path.exists(p):
            p = os.path.join(JD, "masks", f"{name}_s0__cert{ch}.npz")
        if os.path.exists(p):
            cols.append((name, p))
    cols = cols[:12]
    nr, nc = len(ticks), len(cols)
    fig, ax = plt.subplots(nr, nc, figsize=(1.9 * nc, 2.0 * nr), squeeze=False)
    for ci, (name, p) in enumerate(cols):
        for ri in range(nr):
            a = ax[ri, ci]
            bright = np.clip(S[ri] / 1.2, 0, 1) ** 0.6
            if name == "matter":
                img = np.repeat(bright[..., None], 3, -1)
            elif name == "tracker":
                img = PAL[tmap[ri] % 13] * bright[..., None]
                img[tmap[ri] == 0] = 0.55 * bright[tmap[ri] == 0][..., None]
            else:
                d = np.load(p)
                P = int(d["P"])
                lab = d["lab"][ri].astype(int).reshape(128 // P, 128 // P)
                lab = np.kron(lab, np.ones((P, P), int))
                img = PAL[(lab + 1) % 13] * bright[..., None]
            a.imshow(img, interpolation="nearest")
            a.set_xticks([])
            a.set_yticks([])
            if ri == 0:
                a.set_title(name, fontsize=8)
            if ci == 0:
                a.set_ylabel(f"tick {int(ticks[ri])}", fontsize=8)
    fig.suptitle(f"hard masks on certification trajectory 0, half {ch} (colour = slot, brightness = matter; "
                 "tracker: grey = untracked)", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(OD, "fig_segmentations.png"), dpi=130)
    plt.close(fig)


def fig_agreement():
    names = [n for n in G if n != "trk" and smean(G[n], lambda r: r["agreement"]["ari_hard_matter_weighted"]) is not None]
    if not names:
        return
    mets = [("ARI (hard masks)", lambda r: r["agreement"]["ari_hard_matter_weighted"]),
            ("matched recall", lambda r: r["agreement"]["recall"]),
            ("1 / slots per object", lambda r: 1.0 / r["agreement"]["slots_per_object"]),
            ("mass R2 (mask moments)", lambda r: max(r["agreement"]["direct"]["mass_R2"], -0.5)),
            ("mass R2 (RFF probe of readout)", lambda r: r["agreement"]["probe_rff"]["mass_R2"]),
            ("velocity R2 (RFF probe of readout)", lambda r: r["agreement"]["probe_rff"]["vel_R2"])]
    fig, ax = plt.subplots(2, 3, figsize=(15, 7))
    for a, (title, f) in zip(ax.ravel(), mets):
        v = [smean(G[n], f) for n in names]
        a.bar(range(len(names)), [0 if x is None else x for x in v], color=["#888" if n.startswith(("km", "grid")) else
                                                                           ("#c33" if "sup" in n else "#37a") for n in names])
        for n_i, n in enumerate(names):
            for p in G[n]:
                try:
                    a.plot(n_i, f(C["phis"][p]), "k.", ms=4)
                except (KeyError, TypeError):
                    pass
        a.set_xticks(range(len(names)))
        a.set_xticklabels(names, rotation=70, fontsize=7)
        a.set_title(title, fontsize=9)
        a.axhline(1.0, color="k", lw=0.5, ls=":")
        a.set_ylim(min(-0.5, a.get_ylim()[0]), 1.05)
    fig.suptitle("agreement with the tracker's object view (bars: mean over seeds; dots: seeds; grey = no learning, red = "
                 "supervised capacity control)", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(OD, "fig_agreement.png"), dpi=120)
    plt.close(fig)


def fig_ceilings():
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.6))
    for name in G:
        sub = [p + "@mp6" if (p + "@mp6") in C["phis"] else p for p in G[name]]
        c = smean(sub, lambda r: r["families"]["S"]["ceiling"])
        if c is None:
            continue
        ls = "--" if name.startswith(("km", "grid")) else ("-" if name != "trk" else "-")
        ax[0].plot(range(len(HZ)), c, ls, marker="o", ms=3, lw=2.2 if name == "trk" else 1.2, color="k" if name == "trk" else None,
                   label=name)
        co = smean(G[name], lambda r: r["families"]["O"]["ceiling"])
        if co is not None:
            ax[1].plot(range(len(HZ)), co, ls, marker="o", ms=3, lw=2.2 if name == "trk" else 1.2, color="k" if name == "trk" else None,
                       label=name)
    for h in ("hand_mass", "hand_chan"):
        if h in C["phis"]:
            for a in ax:
                a.plot(range(len(HZ)), C["phis"][h]["families"]["GL"]["ceiling"], ":", color="#777", lw=1.5, label=h + " (GL)")
    for a, t in zip(ax, ("family S, 6 numbers per slot (mp6 sub-view / code)", "family O, 12 numbers per slot (moment layout only)")):
        a.set_xticks(range(len(HZ)))
        a.set_xticklabels(HZ)
        a.set_xlabel("horizon (ticks)")
        a.set_ylabel("closure ceiling")
        a.set_title(t, fontsize=9)
        a.set_ylim(0, 1.02)
        a.grid(alpha=0.3)
    ax[1].legend(fontsize=6, ncol=2)
    fig.tight_layout()
    fig.savefig(os.path.join(OD, "fig_ceilings.png"), dpi=120)
    plt.close(fig)


def fig_objval():
    ov = C.get("objval", {})
    names = [n for n in ORDER if n in ov] + [n for n in ov if n not in ORDER]
    if not names:
        return
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
    for a, k in zip(ax, ("set", "self", "rec")):
        v = [np.mean(ov[n][k]["val"]) if ov[n].get(k) else np.nan for n in names]
        a.bar(range(len(names)), v, color=["k" if n == "trk" else ("#888" if n.startswith(("km", "grid")) else
                                                                    ("#c33" if "sup" in n else "#37a")) for n in names])
        for i, n in enumerate(names):
            if ov[n].get(k):
                a.plot([i] * len(ov[n][k]["val"]), ov[n][k]["val"], "w.", ms=3)
        a.set_xticks(range(len(names)))
        a.set_xticklabels(names, rotation=70, fontsize=7)
        a.set_title({"set": "closure, set head (whitened error; 1 = mean predictor)", "self": "local law, self head",
                     "rec": "reconstruction (unexplained fraction of the patch energy)"}[k], fontsize=9)
    fig.suptitle("objective values on frozen readouts (heads trained from scratch, held-out trajectories; lower = the "
                 "objective prefers this view)", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(OD, "fig_objval.png"), dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    fig_segmentations()
    fig_agreement()
    fig_ceilings()
    fig_objval()
    print("figures in", OD, sorted(f for f in os.listdir(OD) if f.startswith("fig_")))
