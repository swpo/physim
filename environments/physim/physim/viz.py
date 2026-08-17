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




# ---------------------------------------------------------------- animations
GIF_DIR = "docs/assets"


def _save_gif(pil_frames, name: str, duration: int = 100) -> str:
    """Quantized, size-capped gif; returns the docs-relative src path."""
    import pathlib
    pathlib.Path(GIF_DIR).mkdir(parents=True, exist_ok=True)
    path = f"{GIF_DIR}/{name}"
    q = [f.quantize(colors=128, dither=0) for f in pil_frames]
    q[0].save(path, save_all=True, append_images=q[1:], duration=duration,
              loop=0, optimize=True)
    return f"assets/{name}"


def _up(a, f=2):
    import numpy as np
    return np.repeat(np.repeat(a, f, 0), f, 1)


def _film_row(panels, badge: str, badge_color, caption: str, scale=2):
    """Compose horizontally-joined field panels + a text bar into a PIL frame."""
    import numpy as np
    from PIL import Image, ImageDraw
    sep = np.full((panels[0].shape[0] * scale, 3, 3), 1.0)
    cells = []
    for i, p_ in enumerate(panels):
        if i:
            cells.append(sep)
        cells.append(_up(p_, scale))
    row = np.concatenate(cells, axis=1)
    canvas = np.full((row.shape[0] + 18, row.shape[1], 3), 0.12)
    canvas[18:, :, :] = row
    pil = Image.fromarray((np.clip(canvas, 0, 1) * 255).astype("uint8"))
    d = ImageDraw.Draw(pil)
    d.text((5, 3), badge, fill=badge_color)
    d.text((max(120, pil.width // 3), 3), caption, fill=(200, 200, 200))
    return pil


def gif_evo_storm(name="E1", seed=0) -> str:
    """E1 film: fertilize era de-adapts the gene pool (mean g rises), then the
    world's own storm cycle re-selects frugality — evolution on camera."""
    import numpy as np
    from matplotlib import cm
    w = make_world(name, seed)
    n_in = w.p.n_in
    sub = w.p.gs_steps_per_tick
    frames = []
    # phase 1: fertilize era (rich regime favors greedy: g drifts UP)
    for k in range(26):
        w.run(np.full((260, n_in), 0.85))
        frames.append(("FERTILIZED (port era)", (120, 220, 120), w))
        frames[-1] = ("FERTILIZED (port era)", (120, 220, 120),
                      w.V1e.copy(), w.Ge.copy(), w.Re.copy(), w.true_macro())
    # phase 2: free run through ~1.5 storm cycles (world weather re-selects)
    for k in range(64):
        w.run(np.zeros((260, n_in)))
        cyc = (w.evo_storm_dwell + w.evo_storm_calm) * sub
        storm = (getattr(w, "_evo_tick", 0) % cyc) < w.evo_storm_dwell * sub
        lab = ("STORM (famine)", (255, 110, 70)) if storm else ("calm", (150, 220, 150))
        frames.append((lab[0], lab[1], w.V1e.copy(), w.Ge.copy(), w.Re.copy(),
                       w.true_macro()))
    pils = []
    for (badge, colr, V, G, R, m) in frames:
        alive = V > 0.05
        Gc = cm.coolwarm(np.clip(G, 0, 1))[..., :3]
        Gc = np.where(alive[..., None], Gc, 0.10)
        Rc = np.zeros((*R.shape, 3))
        Rc[..., 1] = np.clip(R / w.eco_R_max, 0, 1)
        Vc = cm.magma(np.clip(V / 0.35, 0, 1))[..., :3]
        mg = float(m[1]) if m[0] > 0 else float("nan")
        pils.append(_film_row([Vc, Gc, Rc], badge, colr,
                              f"mean genotype {mg:.2f}   [biomass | genotype: blue=frugal red=greedy | resource]"))
    return _save_gif(pils, f"{name.lower()}_evolution.gif", duration=110)


def gif_evo_free(name="E0", seed=0) -> str:
    """E0 film: mutation keeps genetic variance alive (colored colony mosaic);
    a poison era then selects frugality live."""
    import numpy as np
    from matplotlib import cm
    w = make_world(name, seed)
    n_in = w.p.n_in
    frames = []
    for k in range(30):
        w.run(np.zeros((200, n_in)))
        frames.append(("free run", (150, 220, 150),
                       w.V1e.copy(), w.Ge.copy(), w.true_macro()))
    for k in range(40):
        w.run(np.full((200, n_in), -0.75))
        frames.append(("POISON ERA (scarcity)", (255, 110, 70),
                       w.V1e.copy(), w.Ge.copy(), w.true_macro()))
    for k in range(20):
        w.run(np.zeros((200, n_in)))
        frames.append(("released", (150, 220, 150),
                       w.V1e.copy(), w.Ge.copy(), w.true_macro()))
    pils = []
    for (badge, colr, V, G, m) in frames:
        alive = V > 0.05
        Gc = cm.coolwarm(np.clip(G, 0, 1))[..., :3]
        Gc = np.where(alive[..., None], Gc, 0.10)
        Vc = cm.magma(np.clip(V / 0.35, 0, 1))[..., :3]
        mg = float(m[1]) if m[0] > 0 else float("nan")
        sg = float(m[2]) if m[0] > 0 else float("nan")
        pils.append(_film_row([Vc, Gc], badge, colr,
                              f"mean g {mg:.2f}  sd g {sg:.2f}   [biomass | genotype]"))
    return _save_gif(pils, f"{name.lower()}_selection.gif", duration=110)


def panel_evo_ghist(name="E1", seed=0) -> str:
    """Genotype-distribution timeline: the population histogram wanders under
    port eras and world weather — quantitative genetics as a picture."""
    import numpy as np
    w = make_world(name, seed)
    n_in = w.p.n_in
    bins = np.linspace(0, 1, 41)
    rows, marks = [], []
    def snap(era):
        V, G = w.V1e, w.Ge
        alive = V > 0.05
        h, _ = np.histogram(G[alive], bins=bins, weights=V[alive])
        rows.append(h / max(h.sum(), 1e-9)); marks.append(era)
    phases = [(0.85, 22, "fertilize"), (0.0, 26, "free (storms)"),
              (-0.6, 18, "poison"), (0.0, 22, "free (storms)")]         if name == "E1" else              [(0.0, 22, "free"), (0.85, 20, "fertilize"), (0.0, 14, "free"),
              (-0.75, 22, "poison"), (0.0, 12, "free")]
    for amp, blocks, lab in phases:
        for b in range(blocks):
            w.run(np.full((300, n_in), amp))
            snap(lab)
    Z = np.array(rows).T
    fig, ax = plt.subplots(figsize=(8.6, 2.9))
    ax.imshow(Z, aspect="auto", origin="lower", cmap="magma",
              extent=[0, len(rows) * 300, 0, 1])
    ax.set_ylabel("genotype g"); ax.set_xlabel("ticks")
    x0 = 0
    for amp, blocks, lab in phases:
        ax.axvline(x0, color="w", lw=0.6, alpha=0.5)
        ax.text(x0 + 150, 1.04, lab, fontsize=7,
                color={"fertilize": "#1a7f37", "poison": "#cf222e"}.get(lab, "#555"),
                transform=ax.get_xaxis_transform())
        x0 += blocks * 300
    fig.suptitle("GOD VIEW — the gene pool as a distribution: variance persists "
                 "(mutation-selection balance), eras move the whole distribution",
                 y=1.14, fontsize=9)
    return img(fig_to_b64(fig), "genotype histogram timeline")


def gif_excitable_waves(name="C4", seed=0) -> str:
    """C4 film: pacemaker rings, collisions, and a port-driven competing
    pacemaker entraining the medium."""
    import numpy as np
    from matplotlib import cm
    w = make_world(name, seed)
    n_in = w.p.n_in
    frames = []
    for k in range(40):
        w.run(np.zeros((14, n_in)))
        frames.append(("natural pacemaker", (150, 220, 150), w.eu.copy()))
    U = np.zeros(n_in); U[0] = 1.0
    for k in range(44):
        prog = np.tile(U * (1.0 if (k % 2 == 0) else 0.0), (14, 1))
        w.run(prog)
        frames.append(("DRIVING port 0 (competing source)", (255, 160, 60), w.eu.copy()))
    for k in range(24):
        w.run(np.zeros((14, n_in)))
        frames.append(("released", (150, 220, 150), w.eu.copy()))
    pils = []
    for (badge, colr, eu) in frames:
        Ec = cm.viridis(np.clip((eu + 2.0) / 4.0, 0, 1))[..., :3]
        pils.append(_film_row([Ec], badge, colr, "excitation field (waves)", scale=3))
    return _save_gif(pils, f"{name.lower()}_waves.gif", duration=70)


def gif_ecowave_rain(name="B2", seed=0) -> str:
    """B2 film: waves water the ecology — wave passage regenerates resource,
    organisms persist where rain arrives."""
    import numpy as np
    from matplotlib import cm
    w = make_world(name, seed)
    n_in = w.p.n_in
    frames = []
    for k in range(72):
        w.run(np.zeros((30, n_in)))
        frames.append((w.eu.copy(), w.V1e.copy(), w.Re.copy()))
    pils = []
    for (eu, V, R) in frames:
        Ec = cm.viridis(np.clip((eu + 2.0) / 4.0, 0, 1))[..., :3]
        Vc = cm.magma(np.clip(V / 0.35, 0, 1))[..., :3]
        Rc = np.zeros((*R.shape, 3))
        Rc[..., 1] = np.clip(R / w.eco_R_max, 0, 1)
        pils.append(_film_row([Ec, Vc, Rc], "waves feed the ecology", (150, 220, 150),
                              "[waves | organisms | resource ('rain' trails)]"))
    return _save_gif(pils, f"{name.lower()}_rain.gif", duration=90)


def gif_gs_drift(name="C2", seed=0) -> str:
    """C2 film: living chemistry on the move — objects drift, sensors see
    transit traffic."""
    import numpy as np
    from matplotlib import cm
    w = make_world(name, seed)
    n_in = w.p.n_in
    frames = []
    for k in range(64):
        w.run(np.zeros((25, n_in)))
        frames.append(w.V.copy())
    pils = []
    for V in frames:
        Vc = cm.magma(np.clip(V / 0.5, 0, 1))[..., :3]
        pils.append(_film_row([Vc], "objects drift", (150, 220, 150),
                              "concentration field (sensors are fixed patches)", scale=3))
    return _save_gif(pils, f"{name.lower()}_drift.gif", duration=90)


def gif_bulk_switch(name="D4", seed=0) -> str:
    """D-track film: drive one region across its switching threshold, release,
    watch hysteresis hold it — then fatigue rebound."""
    import numpy as np
    from matplotlib import cm
    w = make_world(name, seed)
    n_in = w.p.n_in
    mo = (w.centers_in[:, 1] * w.p.n_modules // w.p.L).astype(int)
    u_hit = np.zeros(n_in); u_hit[mo == mo[0]] = 1.0
    frames = []
    def shoot(U, blocks, badge, colr, per=14):
        for k in range(blocks):
            w.run(np.tile(U, (per, 1)))
            frames.append((badge, colr, w.x.reshape(w.p.L, w.p.L).copy()))
    shoot(np.full(n_in, -0.7), 12, "global -0.7 drive: reset", (120, 160, 255))
    shoot(np.zeros(n_in), 8, "released", (150, 220, 150))
    shoot(u_hit, 16, "pushing ONE region's ports", (255, 160, 60))
    shoot(np.zeros(n_in), 28, "released: hysteresis holds", (150, 220, 150))
    pils = []
    for (badge, colr, X) in frames:
        Xc = cm.RdBu_r(np.clip((X + 1) / 2, 0, 1))[..., :3]
        pils.append(_film_row([Xc], badge, colr, "", scale=8))
    return _save_gif(pils, f"{name.lower()}_switch.gif", duration=80)


def gif_eco_selection(name="B0", seed=0) -> str:
    """B0 film: two variants coexist; sustained poison starves the greedy one
    to extinction; the frugal inherits the map."""
    import numpy as np
    w = make_world(name, seed)
    n_in = w.p.n_in
    frames = []
    def shoot(amp, blocks, badge, colr, per=160):
        for k in range(blocks):
            w.run(np.full((per, n_in), amp))
            m = w.true_macro()
            frames.append((badge, colr, w.V1e.copy(), w.V2e.copy(), w.Re.copy(),
                           int(m[0]), int(m[1])))
    shoot(0.0, 16, "coexistence (free run)", (150, 220, 150))
    shoot(-1.0, 34, "POISON ERA (sustained scarcity)", (255, 110, 70))
    shoot(0.0, 18, "released — extinction persists", (150, 220, 150))
    pils = []
    for (badge, colr, V1, V2, R, n1, n2) in frames:
        rgb = np.zeros((*V1.shape, 3))
        rgb[..., 0] = np.clip(V1 / 0.3, 0, 1)
        rgb[..., 2] = np.clip(V2 / 0.3, 0, 1)
        Rc = np.zeros((*R.shape, 3)); Rc[..., 1] = np.clip(R / w.eco_R_max, 0, 1)
        pils.append(_film_row([rgb, Rc], badge, colr,
                              f"greedy(red) n={n1}  frugal(blue) n={n2}   [organisms | resource]"))
    return _save_gif(pils, f"{name.lower()}_selection.gif", duration=100)


def html_head(title: str, active: str = "worlds") -> str:
    links = [("index.html", "home", "home"), ("results.html", "results", "results"),
             ("worlds.html", "the worlds", "worlds"), ("scoring.html", "scoring", "scoring"),
             ("rollouts-bulk.html", "rollouts", "rollouts"),
             ("https://github.com/swpo/physim", "github", "github")]
    nav = " · ".join(f'<a href="{h}">{("<b>%s</b>" % t) if k == active else t}</a>'
                     for h, t, k in links)
    return f"""<!doctype html>
<html><head><meta charset="utf-8"/>
<title>{title}</title>
<style>
 body {{ font-family: -apple-system, Segoe UI, Helvetica, Arial, sans-serif;
        max-width: 980px; margin: 24px auto; padding: 0 16px; color: #1a1a1a; }}
 h1 {{ font-size: 26px; }} h2 {{ font-size: 20px; margin-top: 40px;
      border-bottom: 2px solid #eee; padding-bottom: 6px;}}
 h3 {{ font-size: 16px; margin-top: 26px; }}
 .note {{ background: #f6f8fa; border-left: 4px solid #0969da; padding: 10px 14px;
         border-radius: 4px; margin: 12px 0; font-size: 14px; }}
 .panel {{ margin: 18px 0; }} img {{ max-width: 100%; height: auto;
          border: 1px solid #e1e4e8; border-radius: 6px; }}
 .film {{ margin: 14px 0; }}
 .film img {{ image-rendering: pixelated; }}
 .film .cap {{ color: #57606a; font-size: 13px; margin-top: 4px; }}
 .meta {{ color: #57606a; font-size: 13px; }}
 .cardrow {{ display: flex; flex-wrap: wrap; gap: 12px; margin: 16px 0; }}
 .tcard {{ border: 1px solid #d0d7de; border-radius: 8px; padding: 12px 16px;
          flex: 1 1 260px; }}
 .tcard h3 {{ margin: 0 0 6px; font-size: 16px; }}
 .tcard p {{ margin: 4px 0; font-size: 13.5px; color: #333; }}
 table {{ border-collapse: collapse; font-size: 13px; }}
 td, th {{ border: 1px solid #d0d7de; padding: 4px 10px; text-align: center; }}
 code {{ background:#f6f8fa; padding: 1px 5px; border-radius: 4px; font-size: 13px;}}
</style></head><body>
<nav style="font-size:14px;margin-bottom:18px;">{nav}</nav>
"""


def film(src: str, caption: str) -> str:
    return (f'<div class="film"><img src="{src}" loading="lazy"/>'
            f'<div class="cap">{caption}</div></div>')


INTRO = """
<h1>physim worlds — a visual guide</h1>
<p>Each physim task drops an agent into a procedurally generated world with
<b>hidden laws</b> behind an <b>anonymous port interface</b>: it can set input
ports in [−1,1] and read noisy, unnamed sensors — nothing else. These pages
show what those worlds actually are, from two perspectives: the <b>god view</b>
(evaluator-only: the hidden lattice, the wiring, the true collective modes,
films of the dynamics) and the <b>agent view</b> (exactly what the agent
gets). Under the hood every world is a <b>grid of simple units</b> (24×24 up
to 96×96 cells) updated by one local rule per track family; everything an
agent encounters — materials, chemistry, organisms, evolution — <i>emerges</i>
from that rule. Time advances in discrete <b>ticks</b>; experiments spend a
tick budget.</p>

<div class="cardrow">
<div class="tcard"><h3><a href="worlds-bulk.html">D — bulk matter</a></h3>
<p>Coupled tanh lattices: collective bistability, hysteresis, per-region
timescales, slow fatigue. The tutorial track that ends in a moody, 8-region
material (D4) frontier agents still fail.</p></div>
<div class="tcard"><h3><a href="worlds-chemistry.html">C — chemistry</a></h3>
<p>Reaction–diffusion: self-sustaining "atoms", movable measurement apparatus,
drifting objects, two coupled species, and an excitable wave medium (C4) whose
timing physics breaks every frontier model.</p></div>
<div class="tcard"><h3><a href="worlds-life.html">B — ecology</a></h3>
<p>Make the food finite and chemistry becomes ecology: carrying capacity,
competition, natural selection, the exclusion boundary — and B2, where
excitable waves are the weather that feeds the world.</p></div>
<div class="tcard"><h3><a href="worlds-evolution.html">E — evolution</a></h3>
<p>Add heredity: a mutable trait field new tissue copies from its parents.
Gene pools shift under selection the world itself applies — storms, famines,
port-driven eras — and the population's history is written in its genotypes.</p></div>
</div>

<h2 id="how-it-works">How the worlds work — the shared machinery</h2>
<p>All four tracks are instances of one template: a multi-channel lattice
field theory (diffusion/mixing + a pointwise nonlinear reaction + input
fields + noise). The track pages describe each reaction family; everything
below is common.</p>

<h3>The idea: why the worlds are built this way</h3>
<p>The benchmark asks one question: <b>can an agent do science?</b> Not recall
science — do it. That requires a world where:</p>
<ul>
<li><b>There are real laws to find, at the right level.</b> The cell-update
rule is the "microphysics", deliberately impossible to read off from outside
(sensors are too coarse, too noisy, too few). But the dynamics guarantee that
a small number of <b>collective</b> quantities — branch states, object counts,
wave rates, populations, gene-pool means — obey simple, discoverable laws.
Exactly like real physics, the useful theory lives at a coarser level than
the mechanism; the agent must find the level itself. Nothing in the interface
hints that regions, objects, species, or genotypes exist.</li>
<li><b>Observation is an achievement, not a given.</b> Sensors are anonymous,
scrambled, biased, sometimes dead. Before any physics can start, the agent has
to calibrate its own senses — find the noise floor, identify dead channels,
work out polarities and groupings. "Learning to use your hands before
building instruments."</li>
<li><b>Experiments cost.</b> A tick budget forces choices: sweep slowly or
probe many ports? Long releases or many repetitions? Strategy, not stamina,
separates agents.</li>
<li><b>The test is out-of-sample by construction.</b> After exploration, the
world poses <i>contracts</i> on fresh copies of itself (same laws, new random
start). Memorised trajectories are useless; only laws transfer.</li>
</ul>

<h3>What the agent can see and do</h3>
<p>The agent never sees the grid, the wiring, or any panel marked "god view"
on these pages. Its entire universe is:</p>
<ul>
<li><b>{n_in_range} input ports</b> ("dials"). Each port either projects a
smooth, invisible field onto one patch of the grid (a force on the world) —
or, in apparatus worlds, secretly operates a sensor instead. The agent does
not know which is which, or where anything points. It sets the dials tick by
tick, each in [−1, +1].</li>
<li><b>{n_out_range} output sensors</b> ("gauges"). Each live sensor reads the
average of one small random patch, times a random gain (possibly negative),
plus a random offset and fresh noise per tick. Several gauges are dead: pure
noise around a constant. Channel order is shuffled; nothing is labelled.</li>
<li><b>Actions</b> (through a fixed tool interface, no other access):
<code>run(program)</code> (hold/ramp dials, get per-sensor summaries),
<code>run_policy(code)</code> (closed-loop control executed inside the world
loop), <code>reset()</code> (fresh initial state, same laws, costs budget),
then <code>ready()</code> → contracts, <code>answer(...)</code>,
<code>answer_prep(policy)</code>, <code>submit_theory(simulator)</code>.</li>
<li><b>Scoring</b>, all on fresh world-copies the agent never touched:
prediction contracts answered with points or <b>quantiles</b> and scored by a
proper distributional rule (CRPS vs god-mode truth ensembles, noise floor
subtracted); preparation policies run on 5 fresh clones; optional executable
theories replayed against every contract. Full mechanics:
<a href="scoring.html">the scoring page</a>.</li>
</ul>
<p class="meta">Everything an agent can access runs in a separate process from
the world engine; hidden state, wiring, and ground-truth ensembles never cross
that boundary. Worlds are procedurally generated from a seed (plus an optional
evaluator-side salt, so public code cannot reproduce a live evaluation
world).</p>
"""

TRACK_META = {
    "bulk": {
        "title": "physim worlds — bulk matter (D)",
        "page": "worlds-bulk.html",
        "prefix": ("D",),
        "families": ("tanh",),
        "blurb": """
<h1>Bulk matter — the D track</h1>
<p class="note">One field per cell, updated as
<code>new x = tanh(J·(neighbour mix) + region bias + input field − fatigue·a) + noise</code>.
When the coupling J exceeds ~1.15, agreement between neighbours becomes
self-reinforcing and whole regions lock into the same sign: the grid stops
acting like independent cells and starts acting like a <i>material</i>. The
grid is cut into vertical stripes (regions) with no neighbour links across
boundaries — each stripe is its own quasi-independent magnet. Higher worlds
add per-region response speeds (some react in ~20 ticks, some 25× slower) and
a slow <b>fatigue</b> variable that integrates recent activation and pushes
back — hold a region "up" too long and it rebounds, even oscillates, after
release. The discoverable laws are collective: switching thresholds,
hysteresis, relaxation schedules, fatigue rebound.</p>
""",
    },
    "chemistry": {
        "title": "physim worlds — chemistry (C)",
        "page": "worlds-chemistry.html",
        "prefix": ("C",),
        "families": ("grayscott", "grayscott2", "excitable"),
        "blurb": """
<h1>Chemistry — the C track</h1>
<p class="note">Two fields per cell: <i>food</i> U and <i>substance</i> V.
Food drips in at a feed rate; V consumes food autocatalytically and decays at
a kill rate. Out of three processes come <b>self-sustaining localized
objects</b>: a spot of V is a little metabolism eating the food that diffuses
in, its own depletion halo capping its size and repelling neighbours. The
objects persist, starve if feed is suppressed, split if it is raised — none
of it programmed. Higher worlds add <b>apparatus ports</b> that secretly move
or toggle sensors (instruments to discover: a field port acts like a force,
an apparatus port like a stage), <b>drift</b> (objects wander; sensors see
transit traffic), a second <b>species</b> with a host–tenant dependency and
cascade extinctions (C3), and finally an <b>excitable wave medium</b> (C4):
a hidden pacemaker emits travelling rings; drive a port steadily and you
create a competing pacemaker; drive too fast and the refractory period blocks
conduction. C4's compact timing laws fit on an index card and currently
defeat every frontier model.</p>
""",
    },
    "life": {
        "title": "physim worlds — ecology (B)",
        "page": "worlds-life.html",
        "prefix": ("B",),
        "families": ("ecology", "ecowave"),
        "blurb": """
<h1>Ecology — the B track</h1>
<p class="note">Take the chemistry track's organisms and make their food
<b>finite</b>: a third field, the <i>resource</i>, regenerates slowly toward
a ceiling, diffuses, and is consumed where organisms live. That one change
turns chemistry into ecology, and the classical population laws emerge on
their own: <b>carrying capacity</b> (B0a — logistic saturation nobody
programmed), <b>competition</b> (B0b — a greedy and a frugal variant dividing
the map), <b>natural selection</b> (B0 — sustained scarcity drives the greedy
variant extinct, and the extinction persists after release because the dead
do not recolonize), the <b>exclusion boundary</b> (B1 — each instance secretly
starts coexist-side or excluded-side; long drives can push it across), and
<b>waves as weather</b> (B2 — the C4 wave layer is the food delivery system:
each passing wave locally boosts regeneration, "rain"; base regeneration alone
cannot sustain life, so the population tracks the wave rate and inherits the
refractory trap — pace the medium too fast and meals <i>fail</i>).
Biology-track sensors read organism density blind to variant ("two kinds of
life exist" is itself a discovery). Population aggregates respond smoothly to
most drives, which is why pure-ecology worlds sit mid-tier while wave-fed B2
breaks frontier models.</p>
""",
    },
    "evolution": {
        "title": "physim worlds — evolution (E)",
        "page": "worlds-evolution.html",
        "prefix": ("E",),
        "families": ("evo",),
        "blurb": """
<h1>Evolution — the E track</h1>
<p class="note">Ecology plus <b>heredity</b>. Organisms carry a continuous
trait field g — their genotype. New tissue <b>copies</b> the genotype of its
dominant parent neighbour (particulate inheritance) with small mutations at
growth sites; nothing else about the update rule mentions genes. The genotype
sets each cell's metabolism through a fixed "biochemistry" map — consumption
rises with g, robustness falls — so <i>greedy</i> and <i>frugal</i> stop
being built-in kinds (as in the B track) and become <b>regions of one
continuous trait space</b>. Then the environment writes into the gene pool:
under scarcity, high-g tissue starves first and the population's mean
genotype slides toward frugality; under plenty it drifts back. E0 is the
laboratory version (you supply the eras through the ports); E1 is the
<b>storm world</b> — recurring famines (hidden period, roughly half the time)
are part of the world's own weather, deep enough to select but not to
sterilize, so the population you meet has <i>already evolved to fit its
climate</i>, and keeps evolving on camera as you intervene. Two clocks to
discover: the storm cycle, and the slower clock of the gene pool tracking
it. A caution from our own measurement: inheritance must be particulate —
an early blending version destroyed variance geometrically (Jenkin's 1867
objection, reproduced in silico) and shipped no evolution at all
(<a href="https://github.com/swpo/physim/blob/main/REPORT.md">lab log</a>,
addendum 20).</p>
""",
    },
}

def _preset_section(name: str, p) -> list[str]:
    """Header + note + meta + static panels for one preset (no films)."""
    parts = []
    if p.reaction == "evo":
        parts.append(f"<h2 id='{name}'>{name} — evolution, "
                     f"{p.n_in} inputs / {p.n_out} sensors ({p.n_dead} dead)</h2>")
    elif p.reaction in ("ecology", "ecowave"):
        parts.append(f"<h2 id='{name}'>{name} — ecology, "
                     f"{p.n_in} inputs / {p.n_out} sensors ({p.n_dead} dead)</h2>")
    elif p.reaction in ("grayscott", "grayscott2", "excitable"):
        parts.append(f"<h2 id='{name}'>{name} — chemistry, "
                     f"{p.n_in} inputs / {p.n_out} sensors ({p.n_dead} dead"
                     + (f", {p.n_apparatus} apparatus ports" if p.n_apparatus else "")
                     + ")</h2>")
    else:
        parts.append(f"<h2 id='{name}'>{name} — {p.n_modules} module(s), "
                     f"{p.n_in} inputs / {p.n_out} sensors ({p.n_dead} dead)</h2>")
    parts.append(f'<p class="note">{preset_notes(name)}</p>')
    if p.reaction == "evo":
        parts.append(f'<p class="meta">lattice {p.L}×{p.L} · heritable trait field '
                     f'(mutation {p.evo_mut}, {"saturating-robustness" if p.evo_gp == "asym" else "linear"} GP map)'
                     + (f' · storms: regen ×{p.evo_storm_depth} for ~{p.evo_storm_dwell:,} ticks, '
                        f'calm ~{p.evo_storm_calm:,}' if p.evo_storm_depth > 0 else '')
                     + f' · resource ceiling '
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
    # static god/agent panels
    if p.reaction == "ecology" and not p.eco_single:
        parts.append('<div class="panel">' + panel_eco_populations(make_world(name, 0)) + "</div>")
        parts.append('<div class="panel">' + panel_eco_selection(make_world(name, 0)) + "</div>")
    elif p.reaction == "excitable":
        parts.append('<div class="panel">' + panel_ex_waves(make_world(name, 0)) + "</div>")
        parts.append('<div class="panel">' + panel_ex_laws(make_world(name, 0)) + "</div>")
    elif p.reaction == "grayscott2":
        parts.append('<div class="panel">' + panel_gs2_species(make_world(name, 0)) + "</div>")
        parts.append('<div class="panel">' + panel_gs2_cascade(make_world(name, 0)) + "</div>")
    elif p.reaction == "grayscott":
        parts.append('<div class="panel">' + panel_gs_objects(make_world(name, 0)) + "</div>")
        parts.append('<div class="panel">' + panel_gs_dynamics(make_world(name, 0)) + "</div>")
    elif p.reaction == "tanh":
        parts.append('<div class="panel">' + panel_wiring(make_world(name, 0)) + "</div>")
        parts.append('<div class="panel">' + panel_micro_snapshots(make_world(name, 0)) + "</div>")
        parts.append('<div class="panel">' + panel_hysteresis(make_world(name, 0)) + "</div>")
        parts.append('<div class="panel">' + panel_agent_timeseries(make_world(name, 0)) + "</div>")
        if p.eps_adapt > 0:
            parts.append('<div class="panel">' + panel_adaptation(make_world(name, 0)) + "</div>")
    return parts


# films per track: {preset: [(builder, caption), ...]} — rendered at the preset section
FILMS = {
    "D4": [("gif_bulk_switch", "FILM (god view, D4): a global −0.7 drive resets every "
            "region down; pushing the ports of ONE region flips just that stripe; after "
            "release, hysteresis holds the flip while fatigue slowly pushes back. This "
            "memory-with-rebound is the physics the S1 stratum probes — the one every "
            "frontier model still fails.")],
    "C2": [("gif_gs_drift", "FILM (god view, C2): living chemistry on the move — the "
            "objects drift along a hidden direction while sensors stay put, so every "
            "sensor sees transit traffic instead of a resident object.")],
    "C4": [("gif_excitable_waves", "FILM (god view, C4): the hidden pacemaker emits "
            "rings; driving port 0 with a pulse train creates a competing pacemaker "
            "whose waves collide and annihilate against the natural ones; after release "
            "the natural rhythm reclaims the medium. Faster source wins — that is the "
            "entrainment law contracts probe.")],
    "B0": [("gif_eco_selection", "FILM (god view, B0): coexistence, then a sustained "
            "poison era starves the greedy (red) variant to extinction while the frugal "
            "(blue) hangs on; after release the world regrows <i>without</i> red — "
            "selection is irreversible because the dead do not recolonize.")],
    "B2": [("gif_ecowave_rain", "FILM (god view, B2): waves water the world — each "
            "passing ring locally boosts resource regeneration (green brightens in "
            "trails), and the organisms (magma) persist only where rain keeps arriving. "
            "No waves, no life.")],
    "E0": [("gif_evo_free", "FILM (god view, E0): mutation keeps the colony mosaic "
            "colorful (genetic variance); a poison era then bleaches it toward blue — "
            "frugal genotypes — live, colony by colony. Watch sd g: variance drops "
            "under selection and recovers by mutation afterwards.")],
    "E1": [("gif_evo_storm", "FILM (god view, E1): a fertilize era first DE-adapts the "
            "gene pool (rich world favors greedy: reds spread), then the era ends and "
            "the world's own storm cycle re-selects frugality (blues return). The gene "
            "pool tracks the climate with a lag — that lag is the second clock agents "
            "must find."),
           ("panel_evo_ghist", None)],
}


def _render_films(name: str, parts: list[str]) -> None:
    import sys
    mod = sys.modules[__name__]
    for entry in FILMS.get(name, []):
        fn_name, caption = entry
        fn = getattr(mod, fn_name)
        if fn_name.startswith("gif_"):
            src = fn(name, 0)
            parts.append(film(src, caption))
        else:
            parts.append('<div class="panel">' + fn(name, 0) + "</div>")


TRACK_ORDER = {"life": ["B0a", "B0b", "B0", "B1", "B2"]}


def build_track(track: str, films: bool = True) -> str:
    meta = TRACK_META[track]
    parts = [html_head(meta["title"], active="worlds"), meta["blurb"]]
    parts.append('<p class="meta"><a href="worlds.html">← all tracks & how the '
                 'worlds work</a></p>')
    names = TRACK_ORDER.get(track) or [
        n for n, p in DIFFICULTY_PRESETS.items()]
    for name in names:
        p = DIFFICULTY_PRESETS[name]
        if p.reaction not in meta["families"]:
            continue
        parts.extend(_preset_section(name, p))
        if films:
            _render_films(name, parts)
    parts.append("""<p class="meta">Generated by <code>python -m physim.viz</code> from the
real engine (seed 0 of each preset). God-view panels and films use
evaluator-only accessors; agent-view panels use only the public interface.
<a href="scoring.html">How scoring works.</a></p></body></html>""")
    html = "\n".join(parts)
    import pathlib
    out = pathlib.Path("docs") / meta["page"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    return str(out)


def build(out_path: str = "docs/worlds.html", films: bool = True) -> list[str]:
    from physim.engine import WorldParams
    presets = list(DIFFICULTY_PRESETS.values())
    intro = INTRO.format(
        n_in_range=f"{min(p.n_in for p in presets)}–{max(p.n_in for p in presets)}",
        n_out_range=f"{min(p.n_out for p in presets)}–{max(p.n_out for p in presets)}",
    )
    # hub page: intro + track cards + one-line ladder per track
    parts = [html_head("physim worlds — visual guide", active="worlds"), intro]
    parts.append("<h2>The difficulty ladder, track by track</h2>")
    ladders = {
        "bulk": "D0 tutorial magnet → D1 sensor opacity → D2 multi-region → "
                "D3 budget pressure → D4 slow/moody regions + fatigue",
        "chemistry": "C0 static objects → C1 movable apparatus → C2 drifting objects "
                     "→ C3 two species + cascades → C4 excitable waves",
        "life": "B0a carrying capacity → B0b competition → B0 selection → "
                "B1 exclusion boundary → B2 wave-fed ecology",
        "evolution": "E0 heredity laboratory → E1 storm world (evolution as weather)",
    }
    for track, lad in ladders.items():
        meta = TRACK_META[track]
        parts.append(f'<p><a href="{meta["page"]}"><b>{meta["title"].split("— ")[1]}'
                     f'</b></a>: {lad}</p>')
    parts.append("""<p class="meta">Each track page carries god-view films of the
dynamics, static panels, and the per-world parameter cards.</p>
</body></html>""")
    html = "\n".join(parts)
    import pathlib
    out = pathlib.Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    written = [str(out)]
    for track in TRACK_META:
        written.append(build_track(track, films=films))
    return written


if __name__ == "__main__":
    import sys
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "docs/worlds.html"
    films = "--no-films" not in sys.argv
    for pth in build(out, films=films):
        print("wrote", pth)
