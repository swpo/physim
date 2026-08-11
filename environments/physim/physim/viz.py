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


def build(out_path: str = "docs/worlds.html") -> str:
    parts = [HTML_HEAD]
    for name in DIFFICULTY_PRESETS:
        p = DIFFICULTY_PRESETS[name]
        w = make_world(name, seed=0)
        parts.append(f"<h2>{name} — {p.n_modules} module(s), "
                     f"{p.n_in} inputs / {p.n_out} sensors ({p.n_dead} dead)</h2>")
        parts.append(f'<p class="note">{preset_notes(name)}</p>')
        parts.append(f'<p class="meta">lattice {p.L}×{p.L} · coupling J={p.J} · '
                     f'micro noise σ={p.sigma} · sensor noise {p.meas_noise} · '
                     f'sign-flip prob {p.p_flip} · tick budget {p.max_ticks:,}</p>')
        parts.append('<div class="panel">' + panel_wiring(make_world(name, 0)) + "</div>")
        parts.append('<div class="panel">' + panel_micro_snapshots(make_world(name, 0)) + "</div>")
        parts.append('<div class="panel">' + panel_hysteresis(make_world(name, 0)) + "</div>")
        parts.append('<div class="panel">' + panel_agent_timeseries(make_world(name, 0)) + "</div>")
        if p.eps_adapt > 0:
            parts.append('<div class="panel">' + panel_adaptation(make_world(name, 0)) + "</div>")
    parts.append("""<h2>How scoring works</h2>
<p>After exploration the evaluator issues <b>prediction contracts</b>: fully
specified input protocols applied to a fresh draw of the same world, asking for
the mean of one sensor over the final 20 ticks, with an uncertainty interval.
Contracts are stratified: S1 weak push + relaxation, S2 steady drives, S3
strong drive + release (branch memory), S4 multi-stage sequences with long
settling windows. Accuracy per contract is exp(−|error|/scale) with
scale = max(3·ensemble_sd, 10% of the channel's dynamic range), evaluated
against a 12-clone ground-truth ensemble the agent can never touch.</p>
<p class="meta">Generated by <code>python -m physim.viz</code> from the real
engine (seed 0 of each preset). God-view panels use evaluator-only accessors;
agent-view panels use only the public interface.</p>
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
