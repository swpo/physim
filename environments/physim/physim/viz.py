"""physim.viz — self-contained HTML gallery describing the worlds to humans.

Generates docs/worlds.html: for each difficulty preset, god-view and agent-view
panels rendered from the real engine. All images are embedded as base64 PNG —
one file, no assets, safe to serve on GitHub Pages.

Usage: .venv/bin/python -m physim.viz [--out docs/worlds.html]
"""
from __future__ import annotations

import base64
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from physim.engine import DIFFICULTY_PRESETS, World, make_world

plt.rcParams.update({
    "figure.facecolor": "white", "axes.titlesize": 9, "axes.labelsize": 8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.spines.top": False,
    "axes.spines.right": False, "font.family": "sans-serif",
})


def fig_to_b64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


def img(b64: str, alt: str) -> str:
    return f'<img src="data:image/png;base64,{b64}" alt="{alt}" loading="lazy"/>'


# ---------------------------------------------------------------- panels
def panel_micro_snapshots(w: World) -> str:
    """God view: micro lattice while a localized drive pushes one region."""
    n_in = w.p.n_in
    mo = (w.centers_in[:, 1] * w.p.n_modules // w.p.L).astype(int)
    target = mo[0]
    w.run(np.full((80, n_in), -0.8))
    frames = [("after global −0.8 drive", w.x.reshape(w.p.L, w.p.L).copy())]
    u = np.zeros(n_in); u[mo == target] = 1.0
    w.run(np.tile(u, (120, 1)))
    frames.append((f"pushing inputs near one region", w.x.reshape(w.p.L, w.p.L).copy()))
    w.run(np.zeros((150, n_in)))
    frames.append(("150 ticks after release", w.x.reshape(w.p.L, w.p.L).copy()))
    fig, axes = plt.subplots(1, 3, figsize=(7.5, 2.4))
    for ax, (title, X) in zip(axes, frames):
        ax.imshow(X, cmap="RdBu_r", vmin=-1, vmax=1, interpolation="nearest")
        ax.set_title(title); ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("GOD VIEW — hidden micro lattice x (blue −1 … red +1); "
                 f"{w.p.n_modules} module(s) as vertical stripes", y=1.06, fontsize=9)
    return img(fig_to_b64(fig), "micro lattice snapshots")


def panel_wiring(w: World) -> str:
    """God view: where inputs couple in and sensors read out."""
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.1))
    fig.subplots_adjust(wspace=0.15, top=0.78)
    field = (w.B @ np.ones(w.p.n_in)).reshape(w.p.L, w.p.L)
    axes[0].imshow(field, cmap="viridis", interpolation="nearest")
    axes[0].scatter(w.centers_in[:, 1], w.centers_in[:, 0], marker="*", s=90,
                    c="white", edgecolors="black", linewidths=0.6)
    axes[0].set_title("input field at u=+1 (★ port centers)", fontsize=8)
    axes[0].set_xticks([]); axes[0].set_yticks([])
    for m in range(1, w.p.n_modules):
        axes[0].axvline(m * w.p.L / w.p.n_modules - 0.5, color="white", lw=0.8, ls="--")
    dead = w.true_is_dead()
    n_live = w.p.n_out - w.p.n_dead
    sgn = np.sign(w.gain)
    axes[1].imshow(np.zeros((w.p.L, w.p.L)), cmap="gray", vmin=-1, vmax=1)
    axes[1].scatter(w.centers_out[sgn > 0][:, 1], w.centers_out[sgn > 0][:, 0],
                    s=40, c="#2ca02c", label=f"sensor + ({int((sgn>0).sum())})")
    axes[1].scatter(w.centers_out[sgn < 0][:, 1], w.centers_out[sgn < 0][:, 0],
                    s=40, c="#d62728", marker="v", label=f"sensor − ({int((sgn<0).sum())})")
    axes[1].set_title(f"sensor patches (+{w.p.n_dead} dead ch. not shown)", fontsize=8)
    axes[1].legend(loc="upper right", fontsize=6, framealpha=0.9)
    axes[1].set_xticks([]); axes[1].set_yticks([])
    fig.suptitle("GOD VIEW — port wiring the agent never sees", y=1.04, fontsize=9)
    return img(fig_to_b64(fig), "port wiring")


def panel_hysteresis(w: World) -> str:
    """God + agent view of the core law: bistability & hysteresis."""
    n_in = w.p.n_in
    us = np.linspace(-1, 1, 15)
    Mup, Yup, Mdn, Ydn = [], [], [], []
    for u in us:
        Y = w.run(np.full((100, n_in), u)); Mup.append(w.true_macro().mean())
        Yup.append(Y[-20:, :].mean(0))
    for u in us[::-1]:
        Y = w.run(np.full((100, n_in), u)); Mdn.append(w.true_macro().mean())
        Ydn.append(Y[-20:, :].mean(0))
    Mdn, Ydn = Mdn[::-1], Ydn[::-1]
    live = ~w.true_is_dead()
    chans = np.where(live)[0][:3]
    fig, axes = plt.subplots(1, 1 + len(chans), figsize=(2.6 * (1 + len(chans)), 2.5))
    axes[0].plot(us, Mup, "o-", ms=3, label="sweep up", color="#1f77b4")
    axes[0].plot(us, Mdn, "s-", ms=3, label="sweep down", color="#ff7f0e")
    axes[0].set_title("TRUE collective mode"); axes[0].set_xlabel("drive u")
    axes[0].legend(fontsize=6); axes[0].axhline(0, color="gray", lw=0.5)
    for ax, c in zip(axes[1:], chans):
        ax.plot(us, [y[c] for y in Yup], "o-", ms=3, color="#1f77b4")
        ax.plot(us, [y[c] for y in Ydn], "s-", ms=3, color="#ff7f0e")
        ax.set_title(f"sensor {c} (what the agent sees)")
        ax.set_xlabel("drive u"); ax.axhline(0, color="gray", lw=0.5)
    fig.suptitle("THE LAW TO DISCOVER — hysteresis: the up- and down-sweep disagree "
                 "in the bistable region", y=1.07, fontsize=9)
    return img(fig_to_b64(fig), "hysteresis loops")


def panel_agent_timeseries(w: World) -> str:
    """Agent view: raw sensor traces during a step protocol."""
    n_in = w.p.n_in
    U = np.concatenate([
        np.zeros((60, n_in)),
        np.full((80, n_in), 0.8),
        np.zeros((140, n_in)),
        np.full((80, n_in), -0.8),
        np.zeros((140, n_in)),
    ])
    Y = w.run(U)
    live = np.where(~w.true_is_dead())[0]
    dead = np.where(w.true_is_dead())[0]
    show = list(live[:5]) + list(dead[:1])
    fig, ax = plt.subplots(figsize=(7.2, 2.6))
    t = np.arange(len(U))
    for c in show:
        lbl = f"ch{c}" + (" (dead)" if c in dead else "")
        ax.plot(t, Y[:, c], lw=0.7, alpha=0.9, label=lbl)
    ax.fill_between(t, -2.2, 2.2, where=np.abs(U.mean(1)) > 0.01,
                    color="gold", alpha=0.15, label="drive on")
    ax.set_xlim(0, len(U)); ax.set_ylim(-2.2, 2.2)
    ax.set_xlabel("tick"); ax.set_ylabel("sensor reading")
    ax.legend(fontsize=6, ncol=6, loc="upper center", bbox_to_anchor=(0.5, 1.18))
    extras = "; one dead channel shown" if len(dead) else ""
    fig.suptitle("AGENT VIEW — raw sensor traces during +0.8 / −0.8 step probes "
                 f"(random gains, signs, offsets, noise{extras})",
                 y=1.28, fontsize=9)
    return img(fig_to_b64(fig), "agent-view time series")


def panel_adaptation(w: World) -> str:
    """D4 motif: duration-dependent memory + slow relaxation oscillation."""
    n_in = w.p.n_in
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.7))
    fig.subplots_adjust(wspace=0.18, top=0.74)
    for hold, color in ((60, "#1f77b4"), (400, "#d62728")):
        w2 = World(w.p, w.seed)
        w2.run(np.full((hold, n_in), 0.9))
        Y = w2.run(np.zeros((500, n_in)))
        m = [float(np.mean([w2.true_macro().mean()]))]  # placeholder start
        # god macro over the release, re-simulated for the plot:
        w3 = World(w.p, w.seed)
        w3.run(np.full((hold, n_in), 0.9))
        ms = []
        for _ in range(50):
            w3.run(np.zeros((10, n_in)))
            ms.append(w3.true_macro().mean())
        axes[0].plot(np.arange(50) * 10, ms, color=color, lw=1.2,
                     label=f"after {hold}-tick drive")
    axes[0].set_title("duration-dependent memory (TRUE mode)", fontsize=8)
    axes[0].set_xlabel("ticks after release"); axes[0].legend(fontsize=6)
    axes[0].axhline(0, color="gray", lw=0.5)
    w4 = World(w.p, w.seed + 7)
    ms = []
    for _ in range(160):
        w4.run(np.zeros((10, n_in)))
        ms.append(w4.true_macro().mean())
    axes[1].plot(np.arange(160) * 10, ms, lw=1.0, color="#2ca02c")
    axes[1].set_title("undriven: slow relaxation oscillation", fontsize=8)
    axes[1].set_xlabel("tick"); axes[1].axhline(0, color="gray", lw=0.5)
    fig.suptitle("D4 MOTIF — slow adaptation: what you did MINUTES ago still matters",
                 y=1.06, fontsize=9)
    return img(fig_to_b64(fig), "adaptation dynamics")


def panel_gs_objects(w: World) -> str:
    """God view for chemistry worlds: V field with objects, ports, sensors."""
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.1))
    fig.subplots_adjust(wspace=0.12, top=0.82)
    im = axes[0].imshow(w.V, cmap="magma", interpolation="nearest")
    axes[0].set_title("substance V — bright blobs are the objects", fontsize=8)
    axes[0].scatter(w.centers_in[:, 1], w.centers_in[:, 0], marker="*", s=80,
                    c="cyan", edgecolors="black", linewidths=0.5, label="input ports")
    axes[0].set_xticks([]); axes[0].set_yticks([])
    axes[1].imshow(w.V, cmap="gray", alpha=0.6, interpolation="nearest")
    n_live = w.p.n_out - w.p.n_dead
    pos = w.app_pos if w.app_pos is not None else w.centers_out
    axes[1].scatter(pos[:, 1], pos[:, 0], s=30, c="#2ca02c", label="sensors")
    movable = [s for (prop, s) in w.app_port_map.values() if prop == "move"]         if w.app_port_map else []
    if movable:
        axes[1].scatter(pos[movable, 1], pos[movable, 0], s=90, facecolors="none",
                        edgecolors="#d62728", linewidths=1.5, label="movable (stage)")
    axes[1].set_title("sensor placement (half near objects, half decoys)", fontsize=8)
    axes[1].legend(loc="upper right", fontsize=6)
    axes[1].set_xticks([]); axes[1].set_yticks([])
    fig.suptitle("GOD VIEW — living chemistry: localized objects, ports, sensors",
                 y=1.02, fontsize=9)
    return img(fig_to_b64(fig), "gray-scott objects")


def panel_gs_dynamics(w: World) -> str:
    """Kill / regrow under a targeted port drive + a sensor's view of it."""
    import numpy as np
    n_in = w.p.n_in
    frames = [("initial", w.V.copy())]
    U = np.zeros((300, n_in)); U[:, 0] = -1.0
    Y1 = w.run(U)
    frames.append(("port 0 driven −1 for 300t (feed starved)", w.V.copy()))
    Y2 = w.run(np.zeros((400, n_in)))
    frames.append(("400t after release", w.V.copy()))
    fig, axes = plt.subplots(1, 4, figsize=(9.2, 2.5))
    fig.subplots_adjust(wspace=0.15, top=0.80)
    for ax, (title, V) in zip(axes[:3], frames):
        ax.imshow(V, cmap="magma", vmin=0, vmax=0.4, interpolation="nearest")
        ax.set_title(title, fontsize=7.5)
        ax.set_xticks([]); ax.set_yticks([])
    Y = np.concatenate([Y1, Y2])
    delta = np.abs(Y[-20:].mean(0) - Y[:20].mean(0))
    hot = list(np.argsort(-delta)[:3])
    for c in hot:
        axes[3].plot(Y[:, c], lw=0.7, label=f"ch{c}")
    axes[3].axvline(300, color="black", ls="--", lw=0.8)
    axes[3].set_title("what nearby sensors read", fontsize=7.5)
    axes[3].legend(fontsize=6)
    fig.suptitle("GOD VIEW + AGENT VIEW — a reaction: starving a region kills its object",
                 y=1.04, fontsize=9)
    return img(fig_to_b64(fig), "gray-scott reaction")


def panel_gs2_species(w: World) -> str:
    """Two-species god view: composite color map + dependency structure."""
    import numpy as np
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1))
    fig.subplots_adjust(wspace=0.12, top=0.80)
    L = w.p.L
    rgb = np.zeros((L, L, 3))
    rgb[..., 0] = np.clip(w.V / 0.35, 0, 1)          # species 1 -> red
    rgb[..., 2] = np.clip(w.V2 / 0.35, 0, 1)         # species 2 -> blue
    rgb[..., 1] = np.clip((w.V * w.V2) / 0.05, 0, 1) # overlap -> green tint
    axes[0].imshow(rgb, interpolation="nearest")
    axes[0].set_title("species A (red), species B (blue); bound pairs appear magenta/white",
                      fontsize=7.5)
    axes[0].set_xticks([]); axes[0].set_yticks([])
    # dependency panel: distances of each B object to nearest A object
    o1, o2 = w.true_objects(), w.true_objects2()
    ds = []
    for (a2, b2) in o2:
        if o1:
            ds.append(min(np.hypot(min(abs(a2-a1), L-abs(a2-a1)),
                                   min(abs(b2-b1), L-abs(b2-b1))) for (a1, b1) in o1))
    axes[1].hist(ds, bins=np.arange(0, 20, 1.5), color="#8250df", edgecolor="white")
    axes[1].set_title("distance from each B object to nearest A object\n"
                      "(clustering at ~0 = B lives ON A)", fontsize=7.5)
    axes[1].set_xlabel("cells")
    fig.suptitle("GOD VIEW — two species, one dependency law: B survives only near A",
                 y=1.02, fontsize=9)
    return img(fig_to_b64(fig), "two species dependency")


def panel_gs2_cascade(w: World) -> str:
    """The cascade law: kill an A host via its port -> bound B dies too."""
    import numpy as np
    L = w.p.L
    o1, o2 = w.true_objects(), w.true_objects2()
    bound = [(a1, b1) for (a1, b1) in o1 for (a2, b2) in o2
             if np.hypot(min(abs(a1-a2), L-abs(a1-a2)),
                         min(abs(b1-b2), L-abs(b1-b2))) < 4]
    s1_ports = [i for i in range(w.p.n_in) if w.port_species[i] == 0]
    cent = [tuple(w.coords[int(np.argmax(w.B[:, i]))]) for i in range(w.p.n_in)]
    def tdist(p1, p2):
        return np.hypot(min(abs(p1[0]-p2[0]), L-abs(p1[0]-p2[0])),
                        min(abs(p1[1]-p2[1]), L-abs(p1[1]-p2[1])))
    port = min(s1_ports,
               key=lambda i: min((tdist(cent[i], bp) for bp in bound), default=999))
    def rgb_of():
        rgb = np.zeros((L, L, 3))
        rgb[..., 0] = np.clip(w.V / 0.35, 0, 1)
        rgb[..., 2] = np.clip(w.V2 / 0.35, 0, 1)
        return rgb
    frames = [("initial (bound A+B pairs)", rgb_of())]
    U = np.zeros((500, w.p.n_in)); U[:, port] = -1.0
    w.run(U)
    frames.append((f"port {port} driven −1, 500t", rgb_of()))
    w.run(np.zeros((500, w.p.n_in)))
    frames.append(("+500t after release: pair gone", rgb_of()))
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 2.7))
    fig.subplots_adjust(wspace=0.08, top=0.78)
    for ax, (title, im_) in zip(axes, frames):
        ax.imshow(im_, interpolation="nearest")
        ax.set_title(title, fontsize=7.2)
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("GOD VIEW — the cascade law: killing a host kills its dependent",
                 y=1.04, fontsize=9)
    return img(fig_to_b64(fig), "cascade law")


def panel_ex_waves(w: World) -> str:
    """Excitable world: traveling wave frames + a sensor's pulse train."""
    import numpy as np
    L = w.p.L
    frames = []
    Y = None
    for k in range(3):
        w.run(np.zeros((18, w.p.n_in)))
        frames.append((f"t+{18*(k+1)} ticks", (w.eu + 1.2) / 2.4))
    Yl = w.run(np.zeros((250, w.p.n_in)))
    live = np.where(~w.true_is_dead())[0]
    sw = Yl[:, live].max(0) - Yl[:, live].min(0)
    ch = int(live[np.argmax(sw)])
    fig, axes = plt.subplots(1, 4, figsize=(9.0, 2.5))
    fig.subplots_adjust(wspace=0.1, top=0.78)
    for ax, (title, im_) in zip(axes[:3], frames):
        ax.imshow(im_, cmap="inferno", vmin=0, vmax=1, interpolation="nearest")
        ax.set_title(title, fontsize=7.5)
        ax.set_xticks([]); ax.set_yticks([])
    axes[3].plot(Yl[:, ch], lw=0.7, color="#0550ae")
    axes[3].set_title(f"sensor ch{ch}: periodic pulses", fontsize=7.5)
    fig.suptitle("GOD VIEW — a pacemaker emits rings of excitation; sensors see pulse trains",
                 y=1.04, fontsize=9)
    return img(fig_to_b64(fig), "excitable waves")


def panel_ex_laws(w: World) -> str:
    """The two headline laws: entrainment (faster source wins) + refractory block."""
    import numpy as np
    n_in = w.p.n_in
    live = np.where(~w.true_is_dead())[0]
    # entrainment: drive port 0 sustained -> global rhythm speeds up
    w1 = w.clone_fresh(noise_seed=41)
    Y0 = w1.run(np.zeros((300, n_in)))
    U = np.zeros((300, n_in)); U[:, 0] = 1.0
    Y1 = w1.run(U)
    sw = Y0[:, live].max(0) - Y0[:, live].min(0)
    ch = int(live[np.argmax(sw)])
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.5))
    fig.subplots_adjust(wspace=0.15, top=0.76)
    axes[0].plot(np.arange(300), Y0[:, ch], lw=0.7, label="intrinsic rhythm")
    axes[0].plot(np.arange(300, 600), Y1[:, ch], lw=0.7, label="port-0 held at +1")
    axes[0].axvline(300, color="black", ls="--", lw=0.8)
    axes[0].set_title("entrainment: a sustained drive creates a FASTER pacemaker\n"
                      "that takes over the whole medium", fontsize=7.5)
    axes[0].legend(fontsize=6)
    # refractory block: pulse-train at short period -> skipped beats
    w2 = w.clone_fresh(noise_seed=42)
    segsY = []
    for period in (100, 40):
        U = np.zeros((400, n_in))
        for t in range(400):
            if (t % period) < 8:
                U[t, 0] = 1.0
        segsY.append(w2.run(U)[:, ch])
    axes[1].plot(segsY[0], lw=0.7, label="drive every 100t → 1:1")
    axes[1].plot(segsY[1], lw=0.7, alpha=0.8, label="drive every 40t → skipped beats")
    axes[1].set_title("refractory block: drive too fast and the medium\n"
                      "answers only every 2nd pulse", fontsize=7.5)
    axes[1].legend(fontsize=6)
    fig.suptitle("GOD VIEW — the compact laws an agent must find", y=1.05, fontsize=9)
    return img(fig_to_b64(fig), "excitable laws")


def panel_eco_populations(w: World) -> str:
    """Ecology god view: species map + population/resource curves under a
    fertilize->free->poison protocol."""
    import numpy as np
    from scipy import ndimage
    L = w.p.L
    fig, axes = plt.subplots(1, 3, figsize=(9.2, 2.8))
    fig.subplots_adjust(wspace=0.22, top=0.78)
    rgb = np.zeros((L, L, 3))
    rgb[..., 0] = np.clip(w.V1e / 0.3, 0, 1)
    rgb[..., 2] = np.clip(w.V2e / 0.3, 0, 1)
    rgb[..., 1] = np.clip(w.Re / w.eco_R_max, 0, 1) * 0.25
    axes[0].imshow(rgb, interpolation="nearest")
    axes[0].set_title("fast variant (red), efficient variant (blue),\n"
                      "resource (faint green)", fontsize=7.5)
    axes[0].set_xticks([]); axes[0].set_yticks([])
    # population curves under a protocol
    hist = {"n1": [], "n2": [], "R": []}
    protocol = ([1.0] * 12 + [0.0] * 12 + [-1.0] * 20 + [0.0] * 16)
    for amp in protocol:
        w.run(np.full((100, w.p.n_in), amp))
        m = w.true_macro()
        hist["n1"].append(m[0]); hist["n2"].append(m[1]); hist["R"].append(m[2])
    tt = np.arange(len(protocol)) * 100
    axes[1].plot(tt, hist["n1"], color="#d62728", lw=1.2, label="fast variant")
    axes[1].plot(tt, hist["n2"], color="#1f77b4", lw=1.2, label="efficient variant")
    axes[1].axvspan(0, 1200, color="green", alpha=0.08)
    axes[1].axvspan(2400, 4400, color="red", alpha=0.08)
    axes[1].set_title("populations: fertilize (green) → free → poison (red) → recover",
                      fontsize=7.5)
    axes[1].set_xlabel("ticks"); axes[1].legend(fontsize=6)
    axes[2].plot(tt, hist["R"], color="#2ca02c", lw=1.2)
    axes[2].set_ylim(0, 1.05)
    axes[2].set_title("resource level (fraction of ceiling)", fontsize=7.5)
    axes[2].set_xlabel("ticks")
    fig.suptitle("GOD VIEW — an ecosystem: two organism variants competing for one "
                 "regenerating resource", y=1.03, fontsize=9)
    return img(fig_to_b64(fig), "ecology populations")


def panel_eco_selection(w: World) -> str:
    """The selection law: sustained scarcity drives the fast variant extinct."""
    import numpy as np
    hist = {"n1": [], "n2": []}
    T_blocks = 46
    for b in range(T_blocks):
        amp = -1.0 if b >= 6 else 0.0
        w.run(np.full((100, w.p.n_in), amp))
        m = w.true_macro()
        hist["n1"].append(m[0]); hist["n2"].append(m[1])
    tt = np.arange(T_blocks) * 100
    fig, ax = plt.subplots(figsize=(6.8, 2.4))
    ax.plot(tt, hist["n1"], color="#d62728", lw=1.3, label="fast variant (greedy)")
    ax.plot(tt, hist["n2"], color="#1f77b4", lw=1.3, label="efficient variant (frugal)")
    ax.axvspan(600, tt[-1], color="red", alpha=0.07)
    ax.set_xlabel("ticks"); ax.set_ylabel("population")
    ax.legend(fontsize=7)
    fig.suptitle("GOD VIEW — natural selection: under sustained scarcity (red span) the "
                 "greedy variant collapses; the frugal one inherits the world",
                 y=1.04, fontsize=9)
    return img(fig_to_b64(fig), "selection law")


def preset_notes(name: str) -> str:
    return {
        "D0": "Clean senses, one collective mode. 6 inputs, 24 well-behaved sensors, "
              "low noise. The tutorial world: find polarities, find the switch, map the loop.",
        "D1": "Same law, murky senses: 4 dead channels, 35% inverted sensors, gain "
              "spread 0.6–1.6×, more noise. Tests sensor calibration before science.",
        "D2": "Three semi-independent regions (modules) with their own switches + "
              "murky senses. Local inputs matter: which port drives which region?",
        "D3": "Six modules, weak global coupling, tighter budget. Requires targeted "
              "per-region experiments and bookkeeping.",
        "D4": "Frontier: 8 modules, per-module response speeds (25× spread), and a "
              "slow fatigue variable (~200-tick memory) that turns the world into a "
              "slow relaxation oscillator. Duration of drive matters; states drift "
              "for hundreds of ticks after release. Best current agents: ~0.2–0.4.",
        "C0": "Chemistry track opens: a two-substance reaction world where the "
              "stable structures are LOCALIZED OBJECTS (self-sustaining spots), "
              "not system-wide switches. Ports perturb the local feed rate: the "
              "right drive can starve an object to death or fatten it. Sensors "
              "are fixed; half sit near objects, half watch empty background.",
        "C1": "Chemistry + microscopy: bigger world, and SOME input ports secretly "
              "move a sensor (a translation stage) or toggle one, instead of "
              "touching the world. Stage ports integrate (effects persist after "
              "release and reverse under opposite drive) — discovering which "
              "ports are apparatus is part of the science. Scanning a movable "
              "sensor across the world is how you find distant objects. One "
              "preparation contract is answerable ONLY by operating the stage.",
        "C2": "Moving chemistry: the objects DRIFT (~1 cell / 20 ticks along a "
              "hidden direction), so every sensor sees transit traffic rather "
              "than a fixed scene. Tail averages converge to traffic statistics; "
              "half the prediction contracts ask for a channel's fluctuation "
              "level (sd) — understanding requires modeling motion, not just "
              "levels. Includes apparatus ports and occasional object "
              "births/deaths. No preparation contracts in v1: positions are "
              "transient by design (tracking preps are future work).",
        "E1": "STORM WORLD: the environment itself cycles — recurring famines "
              "(hidden period, ~half the time) alternate with plenty. Because "
              "traits are heritable (particulate inheritance: new tissue copies "
              "its parent's genotype) and the famine depth sits at the selective "
              "sweet spot, the population EVOLVES: it arrives already adapted "
              "to its climate, and de-adapts/re-adapts when agents fertilize or "
              "poison eras. Two clocks to discover: the storm cycle, and the "
              "slower clock of the gene pool tracking it.",
        "E0": "EVOLUTION: organisms carry a heritable trait g (their "
              "'genome'), copied to new tissue as they grow, mutating slightly "
              "at growth sites. The trait sets each cell's consumption and "
              "hardiness through a fixed biochemistry map — greedy and frugal "
              "are now REGIONS OF TRAIT SPACE, not built-in kinds. Sustained "
              "scarcity (port poison) shifts the whole population toward "
              "frugal genotypes, and it RE-EXPANDS once adapted: natural "
              "selection with genetic memory. Contracts probe adaptation "
              "history: the same drive gives different answers depending on "
              "what the population has lived through. Some sensors read a "
              "phenotype stain (trait-weighted density) — hidden, as ever.",
        "B2": "HYBRID: the excitable wave layer feeds the ecology. Each "
              "traveling wave locally boosts resource regeneration (rain); "
              "base regeneration alone cannot sustain life, so the population "
              "tracks the wave rate — and pacing the medium too fast triggers "
              "refractory conduction block, DELIVERING FEWER MEALS (a "
              "non-monotonic trap). Ports inject current: agents can create "
              "pacemakers, i.e., feed the world. Composed from C4 + B0a, each "
              "separately certified.",
        "B0a": "Curriculum world: ONE organism variant + the regenerating "
               "resource. The only law is logistic growth to a carrying "
               "capacity that ports can raise (fertilize) or lower (poison). "
               "The first rung of the biology ladder.",
        "B0b": "Curriculum world: two variants in a RICH world — competition "
               "and coexistence without extinction risk. Second rung.",
        "B1": "Selection-boundary worlds: the resource ceiling is drawn NEAR "
              "the exclusion threshold, so each instance secretly lands on one "
              "side — fast variant present, or already excluded. Long sustained "
              "drives can push the ecosystem across. Contracts probe the "
              "boundary; agents that never ask which side they are on "
              "misprice every long-horizon prediction.",
        "B0": "BIOLOGY track opens: an ecosystem. Two organism variants compete "
              "for one regenerating resource. The discoverable laws are "
              "population-scale: colonies grow to a carrying capacity; the two "
              "variants divide the world (one grows fast but consumes greedily, "
              "the other is frugal but fragile); and under sustained scarcity — "
              "which the agent can CREATE by driving ports negative (poisoning "
              "resource regeneration) — the greedy variant goes extinct while "
              "the frugal one inherits the world. Sensors read species-blind "
              "organism density; ports fertilize or poison regions. Contracts "
              "probe equilibrium populations, capacity shifts, post-poison "
              "recovery, and the extinction boundary.",
        "C4": "EXCITABLE chemistry: the medium carries traveling WAVES. A hidden "
              "pacemaker emits rings of excitation; every sensor reads a periodic "
              "pulse train (phase = distance / wave speed). The compact laws: a "
              "wave speed, a refractory period (drive too fast → skipped beats, "
              "2:1 block), and ENTRAINMENT (any faster rhythm source — including "
              "one the agent creates with a sustained port drive — takes over "
              "the whole medium; on collision the faster wave annihilates the "
              "slower). Contracts ask for pulse RATES and mean levels under "
              "held-out drive schedules: level-thinking fails completely here "
              "(persistence theory scores 0.25). Rich, not big: a ~40-line "
              "wave theory solves it; nothing less structural does.",
        "C3": "MULTI-SPECIES chemistry (two coupled reaction systems). Two kinds "
              "of object exist: species A is self-sufficient; species B can only "
              "survive in A's presence — B objects live stacked ON their A hosts, "
              "and killing a host kills its tenant (a cascade law). Each input "
              "port feeds ONE species (hidden tag); each sensor reads a hidden "
              "species mixture. That there are two kinds of stuff at all is "
              "itself a discovery: agents must separate the species from port "
              "responses and sensor correlations before the dependency and "
              "cascade laws even become visible.",
    }[name]


HTML_HEAD = """<!doctype html>
<html><head><meta charset="utf-8"/>
<title>physim worlds — visual guide</title>
<style>
 body {{ font-family: -apple-system, Segoe UI, Helvetica, Arial, sans-serif;
        max-width: 980px; margin: 24px auto; padding: 0 16px; color: #1a1a1a; }}
 h1 {{ font-size: 26px; }} h2 {{ font-size: 20px; margin-top: 40px;
      border-bottom: 2px solid #eee; padding-bottom: 6px;}}
 .note {{ background: #f6f8fa; border-left: 4px solid #0969da; padding: 10px 14px;
         border-radius: 4px; margin: 12px 0; font-size: 14px; }}
 .panel {{ margin: 18px 0; }} img {{ max-width: 100%; height: auto;
          border: 1px solid #e1e4e8; border-radius: 6px; }}
 .meta {{ color: #57606a; font-size: 13px; }}
 table {{ border-collapse: collapse; font-size: 13px; }}
 td, th {{ border: 1px solid #d0d7de; padding: 4px 10px; text-align: center; }}
 code {{ background:#f6f8fa; padding: 1px 5px; border-radius: 4px; font-size: 13px;}}
</style></head><body>
<nav style="font-size:14px;margin-bottom:18px;">
<a href="index.html">home</a> · <a href="results.html">results</a> ·
<a href="worlds.html"><b>the worlds</b></a> ·
<a href="scoring.html">scoring</a> ·
<a href="rollouts-bulk.html">rollouts: bulk</a> ·
<a href="rollouts-chemistry.html">rollouts: chemistry</a> ·
<a href="https://github.com/swpo/physim">github</a></nav>
<h1>physim worlds — a visual guide</h1>
<p>Each physim task drops an agent into a procedurally generated world with
<b>hidden laws</b> behind an <b>anonymous port interface</b>: it can set input
ports in [−1,1] and read noisy, unnamed sensors — nothing else. This page shows
what those worlds actually are, from two perspectives: the <b>god view</b>
(evaluator-only: the hidden lattice, the wiring, the true collective modes) and
the <b>agent view</b> (exactly what crosses the interface). The agent never sees
any god-view panel.</p>
<div class="note"><b>The physics in one line:</b> every world is a lattice of
coupled nonlinear units whose neighbor coupling exceeds the collective
threshold — so each region behaves like a magnet: two stable branches,
switching, hysteresis. Higher difficulties add unreliable sensors, multiple
semi-independent regions, response-speed differences, and (D4) a slow fatigue
variable. The agent's job: discover all of this by experiment, then predict
held-out protocols.</div>
"""



EXPLAINER = """
<h2 id="how-it-works">How these worlds work — the full picture</h2>

<h3>1. The layout and the rules</h3>
<p>Under the hood, every world is a <b>grid of simple units</b> (from 24×24 up
to 96×96 cells). Each cell holds a few numbers — its <i>field values</i> —
and time advances in discrete <b>ticks</b>: at every tick each cell updates by
the same local rule. There are three world tracks, each built from a different
rule family (and, in the hardest worlds, from <i>combinations</i> of them);
all are instances of one template (a multi-channel lattice field theory:
diffusion/mixing + a pointwise nonlinear reaction + the input fields +
noise).</p>

<p><b>Track 1 — bulk matter (worlds D0–D4).</b> One field per cell, updated
as:</p>
<pre>new x  =  tanh( J · (mix of my own x and my neighbours' x)
              + my region's bias
              + the input field at my location
              − fatigue · a )   + small noise</pre>
<p>Every ingredient matters for what an agent experiences:</p>
<ul>
<li><b>tanh</b> squashes activations toward −1 or +1 — each cell "wants" to
saturate rather than sit in between.</li>
<li><b>J (coupling)</b> pulls a cell toward the average of its neighbours. When
J&nbsp;&gt;&nbsp;~1.15, agreement is self-reinforcing: whole regions lock into
the same sign. This single knob is what creates all the interesting collective
behaviour — the grid stops acting like independent cells and starts acting like
a <i>material</i>.</li>
<li><b>Regions (modules)</b>: the grid is cut into vertical stripes. Neighbour
links do not cross stripe boundaries; stripes are coupled only weakly (through
a shared mean, if at all). So each stripe is its own quasi-independent magnet
that can point up or down on its own.</li>
<li><b>Response speed (D4)</b>: each region has its own update rate λ — some
regions react to change in ~20 ticks, others take 25× longer.</li>
<li><b>Fatigue (D4)</b>: a second, slow variable <code>a</code> in every cell
integrates recent activation (timescale ~200 ticks) and pushes back against it.
A region held "up" for a long time builds up fatigue and, when released,
rebounds — even oscillates on its own. This makes <i>how long</i> you drive the
system matter, not just how hard.</li>
<li><b>Noise</b>: every update includes a small random kick, and every re-run
of the same experiment draws fresh noise — like a real lab, repetition gives
statistically similar but never identical results.</li>
</ul>
<p>Because of the coupling, each region behaves like a switch with memory
(physicists: a ferromagnet below its critical temperature). Push it hard enough
positive and it snaps to its +1 branch <i>and stays there when you let go</i>;
same for negative. Between the two switching thresholds there is a bistable
zone where the region's current state depends on its history — that is the
<b>hysteresis loop</b> in the plots below. The pattern of branch states across
regions is the world's effective long-term memory.</p>

<p><b>Track 2 — chemistry (worlds C0, C1, …).</b> Two fields per cell: a
<i>food</i> concentration U and a <i>substance</i> concentration V. Food drips
in everywhere at a feed rate, the substance consumes food autocatalytically
(V grows where V already is and food remains) and decays at a kill rate.
Out of these three processes come <b>self-sustaining localized objects</b>: a
spot of V is a little metabolism that eats the food arriving by diffusion, and
its own halo of depleted food stops it from growing and pushes other spots
away. The objects are the "atoms" of these worlds: they persist indefinitely,
repel each other to a preferred spacing, can be dragged by feed gradients,
starve to death if the local feed is suppressed, and split if it is raised.
None of this is programmed — it all emerges from the two-field rule, and the
agent's job is to discover the objects and their laws through the sensors.</p>

<p><b>The apparatus twist (C1 and up).</b> In higher chemistry worlds, some
input ports do not touch the world at all — they secretly operate the
<i>measurement apparatus</i>: one moves a sensor across the grid like a
microscope stage, another can enable or disable a sensor. Nothing labels these
ports. They are discoverable by their signature: a field port acts like a
<i>force</i> (its effect fades after release), an apparatus port acts like a
<i>stage</i> (its effect persists and reverses under opposite drive). Learning
to operate — and then exploit — one's own instruments becomes part of the
science: scanning a movable sensor across the world is how an agent can find
objects its fixed sensors never see.</p>

<p><b>Track 3 — biology (worlds B0a, B0b, B0, B1, B2).</b> Start from the
chemistry track's organisms — self-sustaining spots — and make their food
supply <b>finite</b>. A third field, the <i>resource</i>, regenerates slowly
toward a ceiling, diffuses, and is consumed wherever organisms live. That one
change turns chemistry into ecology, and every classical population law
emerges on its own:</p>
<ul>
<li><b>Carrying capacity</b> (B0a): a founder colony multiplies until
consumption balances regeneration, then the population saturates. Push
consumption higher and you get boom–bust cycles, then extinction — logistic
population dynamics that nobody programmed in.</li>
<li><b>Competition</b> (B0b): two organism <i>variants</i> share the same
resource pool under a trade-off — one is <b>greedy</b> (grows fast, consumes
heavily), the other <b>frugal</b> (efficient, but dies faster on its own).
In a rich world they coexist, dividing the map between them.</li>
<li><b>Natural selection</b> (B0): the environment picks the winner. Ports
now <i>fertilize</i> or <i>poison</i> regional resource regeneration, so the
agent can tilt the world. Under sustained scarcity the greedy variant
collapses to extinction while the frugal one inherits the world — an
extinction that persists after the poison is lifted, because the dead do not
recolonize.</li>
<li><b>The selection boundary</b> (B1): each instance secretly draws its
resource ceiling near the exclusion threshold, so the world starts either
with both variants alive or with the greedy one already gone. Long, sustained
drives can push an instance across the boundary. Agents that never ask
"which side am I on?" misprice every long-horizon prediction.</li>
<li><b>Heredity and adaptation</b> (E0): organisms carry a mutable,
heritable trait that sets their metabolism through a fixed biochemistry map.
Greedy and frugal stop being built-in kinds and become <i>regions of trait
space</i>; under sustained scarcity the population evolves toward frugality
and recovers — natural selection, emergent, with the population's history
written in its gene pool.</li>
<li><b>Waves as weather</b> (B2, a hybrid of the chemistry and biology
rules): the excitable-wave layer from C4 is coupled in as the <i>food
delivery system</i> — each passing wave locally boosts resource regeneration
("rain"), and base regeneration alone cannot sustain life. The population
therefore tracks the wave rate, and the coupling inherits the wave layer's
refractory trap: pace the medium too fast and conduction block makes waves
<i>fail</i>, delivering fewer meals, not more. Ports inject current here, so
an agent can create pacemakers — literally feeding the world by making it
rain — but only if it first discovers what the waves are and what they do.</li>
</ul>
<p>Biology-track sensors read <b>organism density</b>, blind to which variant
they are watching (some read one variant, some the other, some a mixture —
the weights are hidden, so "there are two kinds of life here" is itself a
discovery). Contracts ask population-scale questions over long horizons:
equilibrium levels, how the ecosystem shifts under sustained
fertilizing/poisoning, how it recovers after a famine pulse, and what
survives at the extinction boundary. A caution learned from measurement:
population aggregates respond <i>smoothly</i> to most drives (spatial
averaging washes out discontinuities — even near-extinct colonies recolonize
from refugia), which is why the pure-ecology worlds sit mid-tier while the
wave-fed hybrid B2, whose food supply is gated by non-smooth wave physics,
breaks frontier models today.</p>

<h3>2. The idea: why the worlds are built this way</h3>
<p>The benchmark asks one question: <b>can an agent do science?</b> Not recall
science — do it. That requires a world where:</p>
<ul>
<li><b>There are real laws to find, at the right level.</b> The cell-update rule
above is the "microphysics", and it is deliberately impossible to read off from
the outside (sensors are too coarse, too noisy, too few). But the coupling
guarantees that a small number of <b>collective</b> quantities — one branch
state per region — obey simple, discoverable laws: switching thresholds,
hysteresis, relaxation schedules, fatigue rebound. Exactly like real physics,
the useful theory lives at a coarser level than the mechanism; the agent must
find the level itself. Nothing in the interface hints that "regions" exist,
how many there are, or which sensor watches which.</li>
<li><b>Observation is an achievement, not a given.</b> Sensors are anonymous,
scrambled, biased, sometimes dead. Before any physics can start, the agent has
to calibrate its own senses — find the noise floor, identify dead channels,
work out polarities and groupings. We think of it as "learning to use your
hands before building instruments".</li>
<li><b>Experiments cost.</b> A tick budget forces choices: sweep slowly or probe
many ports? Long releases (to see fatigue) or many repetitions (to beat noise)?
Strategy, not stamina, is what separates agents.</li>
<li><b>The test is out-of-sample by construction.</b> After exploration, the
world poses <i>contracts</i> on fresh copies of itself (same laws, new random
start). Memorised trajectories are useless; only laws transfer.</li>
</ul>
<p>The difficulty ladders then turn independent screws. Bulk track D0→D4:
sensor opacity (dead channels, inverted signs, gain spread, noise), number of
regions (1 → 8 collective degrees of freedom), law depth (fast/slow regions,
fatigue), and budget pressure — D0 is a tutorial magnet; D4 is a slow, moody,
multi-region material where the best current AI agents score ~0.3 of the
achievable 1.0. Chemistry track C0→C4: from fixed sensors watching a few
static objects, through movable apparatus and drifting objects, to the
excitable-wave world C4 whose timing physics currently defeats every frontier
model. Biology track B0a→B2: a curriculum by construction — carrying capacity
alone, then competition, then selection, then the selection boundary, then
the wave-fed hybrid — each rung a certified standalone world, so the hardest
biology world literally decomposes into its own training ladder.</p>

<h3>3. What the agent can see and do</h3>
<p>The agent never sees the grid, the regions, the wiring, or any panel marked
"god view" on this page. Its entire universe is:</p>
<ul>
<li><b>{n_in_range} input ports</b> ("dials"). Each port either projects a
smooth, invisible field onto one patch of the grid (a force on the world:
magnetic-field-like in the bulk track, feed-rate-like in the chemistry track)
— or, in apparatus worlds, secretly operates a sensor instead. The agent does
not know which is which, or where anything points. It sets the dials tick by
tick, each in [−1, +1].</li>
<li><b>{n_out_range} output sensors</b> ("gauges"). Each live sensor reads the
average activation of one small random patch, then multiplies it by a random
gain (possibly negative — the sensor may be installed "upside down"), adds a
random offset and fresh noise per tick. Several gauges are dead: pure noise
around a constant. Channel order is shuffled; nothing is labelled.</li>
<li><b>Actions</b> (through a fixed tool interface, no other access):
  <ul>
  <li><code>run(program)</code> — hold or ramp the dials over chosen durations;
  world evolves; get back per-sensor summaries (means/sds over the final ticks,
  optionally downsampled traces). State persists between runs.</li>
  <li><code>run_policy(code)</code> — submit a small program that reads the
  gauges each tick and sets the dials in response, executed inside the world
  loop: closed-loop control, for holding states that no fixed input can reach.</li>
  <li><code>reset()</code> — fresh random initial state, same laws (costs
  budget).</li>
  <li><code>ready()</code> → receive contracts; <code>answer(...)</code>,
  <code>answer_prep(policy)</code>, <code>submit_theory(simulator)</code>.</li>
  </ul></li>
<li><b>Scoring</b>, all on fresh world-copies the agent never touched:
  <b>prediction</b> contracts ("under this input schedule, what will sensor 23
  average at the end?" — answered with a point estimate or, since v0.10.0,
  full <b>quantiles</b>, scored by a proper distributional rule (CRPS) against
  the world's own god-mode repetition ensemble, with the world's irreducible
  noise floor subtracted: honest uncertainty and multimodal structure pay,
  bluffed certainty loses), <b>preparation</b> contracts ("get sensor 12 into
  this band and make it stay after you let go" — a policy, scored on 5 fresh
  copies), and optionally an <b>executable theory</b> (a simulator of the
  sensors, scored by replaying every contract protocol through it).
  Full mechanics: <a href="scoring.html">the scoring page</a>.</li>
</ul>
<p class="meta">Everything an agent can access runs in a separate process from
the world engine; hidden state, wiring, and ground-truth ensembles never cross
that boundary. Worlds are procedurally generated from a seed (plus an optional
evaluator-side salt, so public code cannot reproduce a live evaluation world).</p>

<h2>The difficulty ladder, world by world</h2>
"""


def build(out_path: str = "docs/worlds.html") -> str:
    from physim.engine import WorldParams
    presets = list(DIFFICULTY_PRESETS.values())
    exp = EXPLAINER.format(
        L=presets[0].L,
        n_in_range=f"{min(p.n_in for p in presets)}–{max(p.n_in for p in presets)}",
        n_out_range=f"{min(p.n_out for p in presets)}–{max(p.n_out for p in presets)}",
    )
    parts = [HTML_HEAD, exp]
    for name in DIFFICULTY_PRESETS:
        p = DIFFICULTY_PRESETS[name]
        w = make_world(name, seed=0)
        if p.reaction in ("ecology", "ecowave", "evo"):
            parts.append(f"<h2>{name} — biology track, "
                         f"{p.n_in} inputs / {p.n_out} sensors ({p.n_dead} dead)</h2>")
        elif p.reaction in ("grayscott", "grayscott2", "excitable"):
            parts.append(f"<h2>{name} — chemistry track, "
                         f"{p.n_in} inputs / {p.n_out} sensors ({p.n_dead} dead"
                         + (f", {p.n_apparatus} apparatus ports" if p.n_apparatus else "")
                         + ")</h2>")
        else:
            parts.append(f"<h2>{name} — {p.n_modules} module(s), "
                         f"{p.n_in} inputs / {p.n_out} sensors ({p.n_dead} dead)</h2>")
        parts.append(f'<p class="note">{preset_notes(name)}</p>')
        if p.reaction == "evo":
            parts.append(f'<p class="meta">lattice {p.L}×{p.L} · heritable trait field '
                         f'(mutation {p.evo_mut}, linear GP map) · resource ceiling '
                         f'{p.eco_R_max} · sensor noise {p.meas_noise} · '
                         f'tick budget {p.max_ticks:,}</p>')
        elif p.reaction == "ecowave":
            parts.append(f'<p class="meta">lattice {p.L}×{p.L} · excitable wave layer feeding '
                         f'a single-variant ecology (rain {p.bw_rain}, base regen '
                         f'{p.bw_regen0}) · pacemaker period ≈{p.ex_pace_period} ticks · '
                         f'tick budget {p.max_ticks:,}</p>')
        elif p.reaction == "ecology":
            parts.append(f'<p class="meta">lattice {p.L}×{p.L} · two organism variants '
                         f'(kill {p.eco_k1}/{p.eco_k2}, consumption {p.eco_c1}/{p.eco_c2}) · '
                         f'resource ceiling {p.eco_R_max} (alien-warped) · '
                         f'sensor noise {p.meas_noise} · tick budget {p.max_ticks:,}</p>')
        elif p.reaction == "excitable":
            parts.append(f'<p class="meta">lattice {p.L}×{p.L} · excitable medium '
                         f'(FHN-class) · intrinsic pacemaker period ≈{p.ex_pace_period} ticks · '
                         f'sensor noise {p.meas_noise} · tick budget {p.max_ticks:,}</p>')
        elif p.reaction in ("grayscott", "grayscott2"):
            parts.append(f'<p class="meta">lattice {p.L}×{p.L} · feed F≈{p.gs_F} · '
                         f'kill k≈{p.gs_k} (alien-warped per instance) · '
                         f'sensor noise {p.meas_noise} · sign-flip prob {p.p_flip} · '
                         f'tick budget {p.max_ticks:,}</p>')
        else:
            parts.append(f'<p class="meta">lattice {p.L}×{p.L} · coupling J={p.J} · '
                         f'micro noise σ={p.sigma} · sensor noise {p.meas_noise} · '
                         f'sign-flip prob {p.p_flip} · tick budget {p.max_ticks:,}</p>')
        if p.reaction == "ecology" and not p.eco_single:
            parts.append('<div class="panel">' + panel_eco_populations(make_world(name, 0)) + "</div>")
            parts.append('<div class="panel">' + panel_eco_selection(make_world(name, 0)) + "</div>")
        elif p.reaction in ("ecology", "ecowave", "evo"):
            pass   # curriculum/hybrid/evo worlds: note-only for now
        elif p.reaction == "excitable":
            parts.append('<div class="panel">' + panel_ex_waves(make_world(name, 0)) + "</div>")
            parts.append('<div class="panel">' + panel_ex_laws(make_world(name, 0)) + "</div>")
        elif p.reaction == "grayscott2":
            parts.append('<div class="panel">' + panel_gs2_species(make_world(name, 0)) + "</div>")
            parts.append('<div class="panel">' + panel_gs2_cascade(make_world(name, 0)) + "</div>")
        elif p.reaction == "grayscott":
            parts.append('<div class="panel">' + panel_gs_objects(make_world(name, 0)) + "</div>")
            parts.append('<div class="panel">' + panel_gs_dynamics(make_world(name, 0)) + "</div>")
        else:
            parts.append('<div class="panel">' + panel_wiring(make_world(name, 0)) + "</div>")
            parts.append('<div class="panel">' + panel_micro_snapshots(make_world(name, 0)) + "</div>")
            parts.append('<div class="panel">' + panel_hysteresis(make_world(name, 0)) + "</div>")
            parts.append('<div class="panel">' + panel_agent_timeseries(make_world(name, 0)) + "</div>")
            if p.eps_adapt > 0:
                parts.append('<div class="panel">' + panel_adaptation(make_world(name, 0)) + "</div>")
    parts.append("""<p class="meta">Generated by <code>python -m physim.viz</code> from the real
engine (seed 0 of each preset). God-view panels use evaluator-only accessors;
agent-view panels use only the public interface. Scoring is described in
<a href="#how-it-works">section 3 above</a>.</p>
</body></html>""")
    html = "\n".join(parts)
    import pathlib
    out = pathlib.Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    return str(out)


if __name__ == "__main__":
    import sys
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "docs/worlds.html"
    print("wrote", build(out))
