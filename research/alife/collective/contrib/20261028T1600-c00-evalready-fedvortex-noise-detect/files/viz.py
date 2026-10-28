"""figures: (1) pulse snapshots (om, pulsed vs twin, at t=20 and 50) for chosen cases + blow-up timing of strong om pulses;
(2) detect: probe readouts (dev0 centre node om and Y, global mean Y) for each arm's members."""
import sys, copy, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex")
import apparatus as A

OUT = A.OUT


def pulses():
    m = A.load()
    s0, info = A.load_prep(m, 0)
    sites = info["sites"]
    cases = [("om", "centre_n", 0.03), ("om", "empty", 0.03), ("om", "centre_p", 0.3), ("Y", "centre_p", 3.0), ("Y", "empty", 3.0)]
    twin = copy.deepcopy(s0)
    tw = {}
    t = 0
    for mk in (20, 50):
        twin = A.advance_time(m, twin, mk - t, t_rel0=t); t = mk; tw[mk] = copy.deepcopy(twin)
    fig, ax = plt.subplots(len(cases), 5, figsize=(13, 2.7 * len(cases)))
    for i, (f, site, amp) in enumerate(cases):
        y, x = sites[site]
        inj = dict(field=f, bump=A.bump_at(y, x), amp=amp, start=0.0, dur=20.0)
        s = copy.deepcopy(s0); t = 0; snaps = {}
        for mk in (20, 50):
            s = A.advance_time(m, s, mk - t, inj=inj, t_rel0=t); t = mk; snaps[mk] = copy.deepcopy(s)
        panels = [(s0["om"], "prepared t=0"), (tw[20]["om"], "twin t=20"), (snaps[20]["om"], f"pulsed t=20"),
                  (snaps[20]["om"] - tw[20]["om"], "diff t=20"), (snaps[50]["om"] - tw[50]["om"], "diff t=50")]
        for j, (img, ttl) in enumerate(panels):
            v = 0.25 if j < 3 else 0.1
            ax[i, j].imshow(np.clip(img, -v, v), cmap="RdBu_r", vmin=-v, vmax=v, origin="lower")
            ax[i, j].plot([x], [y], "k+", ms=10)
            ax[i, j].set_xticks([]); ax[i, j].set_yticks([])
            ax[i, j].set_title(ttl, fontsize=8)
        ax[i, 0].set_ylabel(f"{f} @ {site}\namp {amp}", fontsize=8)
    fig.suptitle("signed vorticity (red +, blue -), colour clipped at +-0.25 (fields) / +-0.1 (diffs); + marks the injection site", fontsize=9)
    plt.tight_layout(); plt.savefig(OUT / "pulse_snapshots.png", dpi=70)
    # blow-up timing / threshold for strong om pulses at the empty site
    res = {}
    for amp in (1.0, 1.5, 2.0, 3.0):
        y, x = sites["empty"]
        inj = dict(field="om", bump=A.bump_at(y, x), amp=amp, start=0.0, dur=20.0)
        s = copy.deepcopy(s0); t = 0; first = None; umax = 0
        with np.errstate(all="ignore"):
            while t < 50 - 1e-9:
                s = A.advance_time(m, s, 0.5, inj=inj, t_rel0=t); t += 0.5
                if not np.isfinite(s["om"]).all():
                    first = t; break
                uy, ux = m._vel(s); umax = max(umax, float(np.sqrt(uy ** 2 + ux ** 2).max()))
        res[amp] = dict(nonfinite_at=first, u_max_before=round(umax, 2), cfl_before=round(umax * m.P["dt"], 3))
    print(json.dumps(res))
    (OUT / "blowup_om_empty.json").write_text(json.dumps(res, indent=1))


def detect(tag, arms):
    E = {a: np.load(OUT / f"ens_s0_{tag}_{a}.npy") for a in ["native", "truth"] + arms}
    every = 2.0
    feats = [(6, "dev0 centre node om"), (13 + 6, "dev0 centre node Y"), (26 + 9, "dev1 centre node om"), (65, "global mean Y"), (66, "global var om")]
    # node order in lattice(): square nodes sorted by (iy, ix); centre (0,0) is index 6; hex centre index 9
    fig, ax = plt.subplots(len(feats), 1, figsize=(10, 2.2 * len(feats)), sharex=True)
    col = {"native": "k", "truth": "0.6", "adv0": "tab:blue", "fork": "tab:red", "dthalf": "tab:green", "kF0": "tab:orange"}
    for i, (fi, name) in enumerate(feats):
        for a, X in E.items():
            tt = (np.arange(X.shape[1]) + 1) * every
            for k in range(X.shape[0]):
                ax[i].plot(tt, X[k, :, fi], color=col[a], lw=0.6, alpha=0.7, label=a if k == 0 else None)
        ax[i].set_ylabel(name, fontsize=8)
    ax[0].legend(fontsize=7, ncol=6)
    ax[-1].set_xlabel("time since prepared state")
    fig.suptitle(f"probe readouts, 8 members per arm, noise {tag}", fontsize=9)
    plt.tight_layout(); plt.savefig(OUT / f"detect_traces_{tag}.png", dpi=70)


if __name__ == "__main__":
    if sys.argv[1] == "pulses":
        pulses()
    else:
        detect(sys.argv[2], sys.argv[3].split(","))
