"""make_cards -- job outputs -> results/: one card per world (card.md + card.png + card.json), the comparison
table (table.md, table.csv), robustness.json (seed, size, late window), derived.json (every run).

usage: python -B make_cards.py <job_id>=<job out dir> [<job_id>=<job out dir> ...] [--rate USD_PER_HOUR] [--no-fig]
A later directory overrides an earlier one for the same (world, run); the earlier card is kept as run "<run>_first"
(the same seeds run twice: a rerun check). numpy + matplotlib; no JAX.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402

import gates as GT  # noqa: E402

RES = os.path.join(HERE, "results")
HZ = (1, 2, 4, 8, 16, 32)
C_LEVEL = {"grid": "#2a78d6", "bodies": "#eb6834", "pop": "#1baf7a"}        # validated (dataviz skill, light surface)
INK, INK2, GRID_C, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
SEQ = ["#9ec5f4", "#3987e5", "#104281"]                                       # one hue, light -> dark (magnitude)
ROBUST_KEYS = ["grid.pf8", "grid.ceil8", "grid.gap8", "grid.sigma_hat", "grid.w_theta8", "grid.pl_ratio0.03_8",
               "grid.pl_ratio0.1_8", "grid.act_ms", "grid.aim_ratio", "grid.xresp", "grid.tick_share", "grid.member_share",
               "pop.pf8", "pop.ceil8", "pop.sigma_hat", "pop.tick_share", "pop.act_ms", "s.nb_mean", "s.half_life_ticks",
               "s.v_net", "s.events100", "b.pf_disp8", "b.ceil_disp8", "b.ceil_field_disp8", "b.quiet8",
               "x.bodies_to_grid8", "l.dceil8_AB", "l.dceil16_AB", "t.l1_8", "k.law32"]
# entries that scale with the area or with the input per block are not compared across sizes (the Mac's review of
# the first job, item 6): the body count and the events are compared per 64 x 64 px, the action entries are left out
SIZE_SKIP = {"grid.act_ms", "grid.aim_ratio", "pop.act_ms", "grid.xresp"}
SIZE_PER_AREA = {"s.nb_mean", "s.events100"}
GATE_KEYS = ["exam_worthy", "structure", "interaction", "reading_worthy", "actions", "stationary", "levels_add",
             "learned_differs"]


def fmt(v, nd=2):
    if v is None:
        return "n/a"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, str):
        return v
    v = float(v)
    if not np.isfinite(v):
        return "inf" if v > 0 else ("n/a" if np.isnan(v) else "-inf")
    a = abs(v)
    if a >= 1000:
        return f"{v:.0f}"
    if a >= 100:
        return f"{v:.0f}"
    if a >= 10:
        return f"{v:.1f}"
    if a >= 0.1 or a == 0:
        return f"{v:.{nd}f}"
    return f"{v:.3f}" if a >= 0.001 else f"{v:.1e}"


def row(vals, nd=2):
    return " / ".join(fmt(v, nd) for v in vals)


def load(dirs):
    cards, series = {}, {}
    for spec in dirs:
        job, d = spec.split("=", 1) if "=" in spec else ("?", spec)
        for f in sorted(glob.glob(os.path.join(d, "cards", "*.json"))):
            c = json.load(open(f))
            if not c.get("finite", True):
                print("NON-FINITE run left out:", f)
                continue
            c["_job"] = job
            key = (c["world"], c["run"])
            if key in cards:
                cards[(c["world"], c["run"] + "_first")] = cards[key]
                if key in series:
                    series[(c["world"], c["run"] + "_first")] = series[key]
            cards[key] = c
            s = os.path.join(d, "series", os.path.basename(f)[:-5] + ".npz")
            if os.path.exists(s):
                series[key] = s
    return cards, series


def rederive(c):
    """Derived numbers and gates recomputed here from the card (the job's copies are kept in the card)."""
    d = GT.derive(c)
    return d, GT.gates(d)


# ----------------------------------------------------------------------------- figure
def figure(world, runs, series, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    c = runs.get("A") or next(iter(runs.values()))
    plt.rcParams.update({"font.size": 8, "axes.edgecolor": INK2, "axes.labelcolor": INK2, "xtick.color": INK2,
                         "ytick.color": INK2, "text.color": INK, "axes.spines.top": False, "axes.spines.right": False,
                         "axes.facecolor": SURF, "figure.facecolor": SURF, "axes.titlesize": 8.5, "axes.titleweight": "bold"})
    fig = plt.figure(figsize=(11.0, 5.3), dpi=100)
    gs = fig.add_gridspec(2, 8, height_ratios=[1.0, 1.25], hspace=0.42, wspace=1.3, left=0.045, right=0.985, top=0.9, bottom=0.1)
    # frames of one member at the four snapshot ticks
    key = (world, c["run"])
    if key in series:
        z = np.load(series[key])
        fr = z["frames"].astype(float) / 255.0                                # (4, C, H, W)
        T, seg = c["sizes"]["T"], c["sizes"]["T"] // max(1, len(fr))
        for i in range(min(4, len(fr))):
            ax = fig.add_subplot(gs[0, 2 * i:2 * i + 2])
            a, b = fr[i, 0], fr[i, 1] if fr.shape[1] > 1 else fr[i, 0]
            g = np.clip((a + b) ** 0.6, 0, 1)
            img = np.stack([1 - 0.85 * g * (0.35 + 0.65 * a / np.maximum(a + b, 1e-9)),
                            1 - 0.75 * g, 1 - 0.85 * g * (0.35 + 0.65 * b / np.maximum(a + b, 1e-9))], -1)
            ax.imshow(np.clip(img, 0, 1), interpolation="nearest")
            ax.set_xticks([]), ax.set_yticks([])
            ax.set_title(f"tick {c['burn'] + (i + 1) * seg}", fontweight="normal", color=INK2)
    hz = c["grid"]["hz"]

    def base(ax, title, ylab=None, logy=False):
        ax.set_xscale("log", base=2)
        ax.set_xticks(hz)
        ax.set_xticklabels([str(h) for h in hz])
        ax.minorticks_off()
        ax.grid(True, color=GRID_C, lw=0.6)
        ax.set_axisbelow(True)
        ax.set_title(title, loc="left")
        ax.set_xlabel("horizon (ticks)")
        if logy:
            ax.set_yscale("log")

    def lv(name):
        if name == "grid":
            return c["grid"]
        if name == "pop":
            return None if c["pop"].get("empty") else c["pop"]["lin"]
        return c["bodies"]["single"]["disp"]
    labels = {"grid": "block view", "bodies": "bodies (quiet steps)", "pop": "population"}
    for j, (k, title) in enumerate((("pf_med", "Predictable fraction"), ("ceil_med", "Closure ceiling of the cheap family"))):
        ax = fig.add_subplot(gs[1, 2 * j:2 * j + 2])
        base(ax, title)
        for name in ("grid", "bodies", "pop"):
            L = lv(name)
            if L is None:
                continue
            y = np.array([np.nan if v is None else v for v in L[k]], float)
            ax.plot(hz, y, color=C_LEVEL[name], lw=2, marker="o", ms=4, label=labels[name])
        ax.set_ylim(-0.05, 1.05)
        ax.legend(frameon=False, fontsize=7, loc="lower left", labelcolor=INK)
    ax = fig.add_subplot(gs[1, 4:6])
    base(ax, "Hidden part: plug-in loss / oracle variance", logy=True)
    for i, e in enumerate(("0.03", "0.1", "1.0")):
        if e in c["grid"]["pl"]:
            y = np.array(c["grid"]["pl"][e]["pl_over_vorc_med"], float)
            ax.plot(hz, np.where(y > 0, y, np.nan), color=SEQ[i], lw=2, marker="o", ms=4, label=f"{e} of the prior")
    ax.axhline(1.0, color=INK2, lw=0.8, ls=(0, (3, 3)))
    ax.legend(frameon=False, fontsize=7, title="block view; move of", title_fontsize=7, labelcolor=INK)
    ax = fig.add_subplot(gs[1, 6:8])
    base(ax, "Actions: displacement / twin floor", logy=True)
    for i, n in enumerate(("aimed_50", "aimed_200", "aimed_800")):
        if n in c["grid"]["act"]:
            y = np.array(c["grid"]["act"][n]["D_over_floor"], float)
            ax.plot(hz, np.where(y > 0, y, np.nan), color=SEQ[i], lw=2, marker="o", ms=4, label=f"aimed, {n[6:]} nats")
    if "blind_200" in c["grid"]["act"]:
        y = np.array(c["grid"]["act"]["blind_200"]["D_over_floor"], float)
        ax.plot(hz, np.where(y > 0, y, np.nan), color=INK2, lw=1.5, ls=(0, (4, 2)), marker="s", ms=3.5, label="blind, 200 nats")
    ax.axhline(1.0, color=INK2, lw=0.8, ls=(0, (3, 3)))
    ax.legend(frameon=False, fontsize=7, labelcolor=INK, loc="lower left")
    g = c.get("_gates", {})
    fig.suptitle(f"{world}: {g.get('verdict', '')}   (run {c['run']}, {c['meta'].get('lattice')}, "
                 f"{c['sizes']['M']} members x {c['sizes']['T']} ticks)", x=0.045, ha="left", fontsize=10, fontweight="bold")
    fig.savefig(path, dpi=100)
    plt.close(fig)
    return os.path.getsize(path)


# ----------------------------------------------------------------------------- card.md
def card_md(world, runs, D, G, late, rob, rate):
    c = runs.get("A") or next(iter(runs.values()))
    r0 = c["run"]
    d, g = D[r0], G[r0]
    m = c["meta"]
    L = []
    A = L.append
    A(f"# World card: {world}")
    A("")
    A(f"Family {c['family']}, role {c['role']}. Lattice {m.get('lattice')}, {m.get('substeps_per_tick')} substeps per tick; "
      f"input: {m.get('input')}. Hidden part: {m.get('hidden')} (prior: {m.get('prior')}). Views: {m.get('views')}."
      + (f" Timeline: {m['timeline']}." if m.get("timeline") else ""))
    A("")
    A("**Verdict** " + "; ".join(f"run {r}: {G[r]['verdict']}" for r in runs)
      + f". sigma_hat {fmt(g['sigma_hat_best'])} at the {g['sigma_hat_level']} level.")
    A("")
    A("![card](card.png)")
    A("")
    sz = c["sizes"]
    A(f"Sizes: {sz['M']} members ({sz['M_fit']} fit), {sz['T']} ticks after {c['burn']} of burn-in, {sz['NS']} test states x "
      f"{sz['R']} replicas x {sz['HB']} ticks; neighbours at {sz['eps']} of the prior ({sz['n_dir']} directions x {sz['R2']}). "
      "Ratios are from medians over test states (typical state); `mean` marks the mean-based value.")
    A("")
    A("## 1. Predictability at 1 / 2 / 4 / 8 / 16 / 32 ticks")
    A("")
    A("| level | predictable fraction | closure ceiling (cheap family) | ceiling at 8, mean-based |")
    A("|---|---|---|---|")
    A(f"| block view | {row(c['grid']['pf_med'])} | {row(c['grid']['ceil_med'])} | {fmt(d.get('grid.ceil8_mean'))} |")
    b = c["bodies"]["single"]
    A(f"| bodies, displacement on quiet steps | {row(b['disp']['pf_med'])} | {row(b['disp']['ceil_med'])} | {fmt(d.get('b.ceil_disp8_mean'))} |")
    if not c["pop"].get("empty"):
        p = c["pop"]["lin"]
        A(f"| population ({', '.join(n for n, l in zip(c['pop']['names'], c['pop']['live']) if l)}) | {row(p['pf_med'])} | "
          f"{row(p['ceil_med'])} | {fmt(d.get('pop.ceil8_mean'))} |")
    A("")
    s = c["structure"]
    A("## 2. Structure")
    A("")
    A(f"- Bodies: {fmt(s['nb_mean'])} +- {fmt(s['nb_std'])} (slots {s['K']}, full {fmt(100 * s['slots_full_share'], 1)}% of the time), "
      f"{fmt(100 * s['body_frac'], 0)}% of the matter, radius {fmt(s['rg'])} px, half-life {fmt(s['half_life_ticks'], 0)} ticks, "
      f"net speed {fmt(s.get('v_net'))} px/tick.")
    A(f"- Events per 100 ticks and member: {fmt(s['fusions100'])} fusions, {fmt(s['fissions100'])} fissions, "
      f"{fmt(s['births100'])} births, {fmt(s['deaths100'])} deaths.")
    A(f"- Scales: wavelength {fmt(s['wavelength_px'])} px; neighbouring-block correlation {fmt(c['grid'].get('block_corr1'))}; "
      f"block-view autocorrelation at 1 / 8 / 32 ticks {row([c['grid']['autocorr'][i] for i in (0, 3, 5)])}; "
      f"{fmt(100 * s['moved'], 1)}% of the matter relocated per tick.")
    bb = c["bodies"]
    A(f"- Single-body law (displacement, quiet steps) at 1 / 4 / 8 / 16 ticks: ceiling {row([bb['single']['disp']['ceil_med'][i] for i in (0, 2, 3, 4)])}; "
      f"constant velocity alone {row([bb['single']['disp']['ceil_pers_med'][i] for i in (0, 2, 3, 4)])}; with the surrounding block view "
      f"{row([bb['field']['disp']['ceil_med'][i] for i in (0, 2, 3, 4)])}. Quiet share of 8-tick steps {fmt(d.get('b.quiet8'))} "
      f"({fmt(d.get('b.n_test8'), 0)} test rows).")
    A("")
    A("## 3. Stationarity")
    A("")
    A(f"- Share of the variance that is a function of the tick alone (mean over channels; largest channel in brackets): "
      f"block view {fmt(d.get('grid.tick_share'), 3)} [{fmt(d.get('grid.tick_share_max'), 3)}], "
      f"population {fmt(d.get('pop.tick_share'), 3)} [{fmt(d.get('pop.tick_share_max'), 3)}]"
      + (" (" + ", ".join(f"{k} {fmt(v, 2)}" for k, v in c['pop'].get('tick_share_q', {}).items()) + ")" if not c["pop"].get("empty") else "") + ".")
    A(f"- Share between members' time-means: block view {fmt(d.get('grid.member_share'), 3)}, population {fmt(d.get('pop.member_share'), 3)}.")
    if late:
        A(f"- Late window (+{m.get('late_gap')} ticks) against early: largest shift of a block-channel mean {fmt(np.max(np.abs(late['d_mean'])))} sd, "
          f"largest log sd ratio {fmt(np.max(np.abs(late['log_sd_ratio'])))}, body count x {fmt(late['count_ratio'])}, "
          f"events {fmt(late['events_early'])} -> {fmt(late['events_late'])}, ceiling at 8 {fmt(late['ceil8'][0])} -> {fmt(late['ceil8'][1])}, "
          f"sigma_hat {fmt(late['sigma_hat'][0])} -> {fmt(late['sigma_hat'][1])}. Same statistics: **{fmt(late['same'])}**.")
    A("")
    A("## 4. Effective laws")
    A("")
    below = [h for h, v in zip(c["grid"]["hz"], c["grid"]["ceil_med"]) if v is not None and v < 0.5]
    A(f"- Linear local law on the block view: ceiling {fmt(c['grid']['ceil_med'][0], 3)} at 1 tick; falls below 0.5 "
      + (f"at {below[0]} ticks" if below else "at no horizon up to 32 ticks")
      + f"; the worst tenth of (state, block) cells carries {fmt(100 * (c['grid']['excess_top10pct_share'].get('8') or float('nan')), 0)}% of its excess error at 8 ticks.")
    if not c["pop"].get("empty"):
        A(f"- Population law at 8 ticks: linear ceiling {fmt(c['pop']['lin']['ceil_med'][3])}, quadratic {fmt(c['pop']['quad']['ceil_med'][3])}.")
    k = c["pop"].get("kind_share_law", {})
    if k.get("law"):
        A(f"- Kind-share law ds = b1 s(1-s) + b2 (1-2s) at 8 / 32 ticks: ceiling {fmt(d.get('k.law8'))} / {fmt(d.get('k.law32'))}, "
          f"a constant drift {fmt(d.get('k.const8'))} / {fmt(d.get('k.const32'))}, a line in s {fmt(d.get('k.lin8'))} / {fmt(d.get('k.lin32'))} "
          f"(predictable fraction of the change {fmt(d.get('k.pf8'))} / {fmt(d.get('k.pf32'))}).")
    A("")
    A("## 5. Levels")
    A("")
    A(f"- The slot list added to the block view's predictor lowers its error at 8 ticks by {fmt(d.get('x.bodies_to_grid8'), 3)} of the variance; "
      f"the block view added to the body law by {fmt(d.get('x.grid_to_bodies8'), 3)}; block moments added to the population law by "
      f"{fmt(d.get('x.grid_to_pop8'), 3)}; the population law beats persistence by {fmt(d.get('x.pop_over_pers8'), 3)}.")
    A("")
    if "learned" in c:
        A("## 6. Learned variable (slow features of the 2 x 2 sub-blocks against the hand block view)")
        A("")
        A(f"- Ceiling gain at 8 / 16 / 32 ticks, halves AB: {row([d.get('l.dceil8_AB'), d.get('l.dceil16_AB'), d.get('l.dceil32_AB')])}; "
          f"BA: {row([d.get('l.dceil8_BA'), d.get('l.dceil16_BA'), d.get('l.dceil32_BA')])}. Predictable-fraction gain at 8: "
          f"{fmt(d.get('l.dpf8_AB'), 3)} / {fmt(d.get('l.dpf8_BA'), 3)}. Smallest R^2 of a learned component on the hand channels: {fmt(d.get('l.r2_min'))}.")
        A("")
    A("## 7. Actions (block view, 4 ticks after the input starts)")
    A("")
    A(f"- The aimed 200-nat shift is {fmt(d.get('grid.act_ms_var'), 3)} of the block view's variance, {fmt(d.get('grid.act_ms_over_vcheap'), 3)} of the cheap family's error.")
    A(f"- Predictable shift / oracle variance: aimed 50 / 200 / 800 nats {row([d.get('grid.act_ms_50'), d.get('grid.act_ms'), d.get('grid.act_ms_800')])}; "
      f"displacement of the aimed 200-nat input / twin floor {fmt(d.get('grid.act_D_floor'))}; aimed / blind {fmt(d.get('grid.aim_ratio'))}. "
      f"Population level: {fmt(d.get('pop.act_ms'))}.")
    A("")
    A("## 8. Hidden part")
    A("")
    A(f"- Plug-in loss / oracle variance at 8 ticks for a move of 3% / 10% / 100% of the prior: block view "
      f"{row([d.get('grid.pl_ratio0.03_8'), d.get('grid.pl_ratio0.1_8'), d.get('grid.pl_ratio1.0_8')])}; population "
      f"{row([d.get('pop.pl_ratio0.03_8'), d.get('pop.pl_ratio0.1_8'), d.get('pop.pl_ratio1.0_8')])}.")
    A(f"- Weight of a prior-sized error, w_theta at 4 / 8 / 16 ticks: block view {row([d.get('grid.w_theta4'), d.get('grid.w_theta8'), d.get('grid.w_theta16')])}; "
      f"sigma_hat block view {fmt(d.get('grid.sigma_hat'))}, population {fmt(d.get('pop.sigma_hat'))}.")
    A(f"- Response to the aimed 200-nat input changes by {fmt(d.get('grid.xresp'))} oracle variances when the hidden part moves by the prior. "
      f"Evidence index for a 10% move: {fmt(d.get('grid.evidence0.1'))} nats per tick (3 nats in {fmt(d.get('grid.ticks_to_3nats0.1'), 3)} ticks).")
    A(f"- Noise twins: {fmt(100 * (d.get('t.l1_8') or float('nan')), 1)}% of the matter placed differently after 8 ticks; doubling time {fmt(d.get('t.doubling'), 1)} ticks.")
    A("")
    A("## 9. Cost")
    A("")
    spt, inc = cost_of(runs, True)
    A(f"- {fmt(1e3 * spt, 3)} ms per member-tick on the job's {c.get('backend', 'gpu').upper()} with the tracker on every member, "
      + ("COMPILE INCLUDED (this world's only run was the first call of its program)" if inc else "compile excluded")
      + f" ({fmt(1.0 / spt, 0)} member-ticks/s)"
      + (f"; USD {fmt(rate * spt / 3600 * 1e6)} per million member-ticks at USD {rate}/h." if rate else "."))
    A("")
    A("## Gates and robustness")
    A("")
    A("| gate | " + " | ".join(f"run {r}" for r in runs) + " |")
    A("|---|" + "---|" * len(runs))
    for k in GATE_KEYS:
        A(f"| {k} | " + " | ".join(fmt(G[r][k]) for r in runs) + " |")
    if rob.get("seed"):
        bad = [k for k, v in rob.get("seed", {}).items() if v is False]
        A("")
        A(f"Seed (A against B): {len([v for v in rob.get('seed', {}).values() if v])} of {len(rob.get('seed', {}))} entries agree"
          + (f"; not robust: {', '.join(bad)}." if bad else "."))
    if rob.get("size") is not None:
        if True:
            bad = [k for k, v in rob["size"].items() if v is False]
            A("")
            A(f"Size (64 px against {rob.get('size_against')}; counts per area, action entries left out): "
              f"{len([v for v in rob['size'].values() if v])} of {len(rob['size'])} entries agree"
              + (f"; not robust: {', '.join(bad)}." if bad else "."))
    sh = rob.get("split_half")
    if sh:
        A("")
        A(f"Estimator size (even against odd test states, block view at 8 ticks): predictable fraction {row(sh['pf8'])}, "
          f"ceiling {row(sh['ceil8'])}.")
    A("")
    A("Source: " + "; ".join(f"run {r}: job {c_['_job']}" for r, c_ in runs.items())
      + f"; files `out/cards/{world}__<run>.json` on origin/gpu-jobs; numbers recomputed by `make_cards.py` from those cards "
      "(`card.json` here holds the derived numbers and gates of every run). Pilot: never an exam instance.")
    return "\n".join(L) + "\n"


def cost_of(runs, flag=False):
    """Seconds per member-tick, compile excluded: runs that were not the first call of their program. Where a
    world's only runs were first calls the value includes the compile (flag True)."""
    t = [r["timing"] for r in runs.values() if not r["timing"].get("first_call_of_program", False)]
    inc = not t
    if inc:
        t = [r["timing"] for r in runs.values()]
    v = float(np.median([(x["main_s"] + x["branch_s"]) / (x["main_member_ticks"] + x["branch_member_ticks"]) for x in t]))
    return (v, inc) if flag else v


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--rate", type=float, default=0.0)
    ap.add_argument("--no-fig", action="store_true")
    ap.add_argument("--res", default=RES)
    a = ap.parse_args()
    cards, series = load(a.dirs)
    worlds = {}
    for (w, r), c in cards.items():
        worlds.setdefault(w, {})[r] = c
    order = json.load(open(os.path.join(HERE, "worlds.json")))["worlds"] + json.load(open(os.path.join(HERE, "worlds2.json")))["worlds"]
    seen_names = set()
    order = [w for w in order if not (w["name"] in seen_names or seen_names.add(w["name"]))]
    names = [w["name"] for w in order if w["name"] in worlds] + [w for w in worlds if w not in {x["name"] for x in order}]
    os.makedirs(os.path.join(a.res, "cards"), exist_ok=True)
    derived, robust, rows = {}, {}, []
    for w in names:
        runs = {r: worlds[w][r] for r in ("A", "B", "late") if r in worlds[w]}
        if "A_first" in worlds[w]:
            df, gf = rederive(worlds[w]["A_first"])
        D, G = {}, {}
        for r, c in runs.items():
            D[r], G[r] = rederive(c)
            c["_gates"] = G[r]
        derived[w] = {r: dict(derived=D[r], gates=G[r]) for r in runs}
        if "A_first" in worlds[w]:
            derived[w]["A_first"] = dict(derived=df, gates=gf)
        late = GT.late_vs_early(runs["A"], runs["late"]) if "A" in runs and "late" in runs else None
        rob = {}
        if "A" in runs and "B" in runs:
            rob["seed"] = {k: GT.robust(D["A"].get(k), D["B"].get(k)) for k in ROBUST_KEYS}
            rob["seed_gates"] = {k: bool(G["A"][k] == G["B"][k]) for k in GATE_KEYS + ["dull"]}
        big = w.replace("foundry_", "foundry128_") if w.startswith("foundry_") else None
        if w == "vortex64":
            big = "vortex128g16" if "vortex128g16" in worlds else "vortex128"
        if big and big in worlds and "A" in worlds[big] and "A" in runs:
            db, gb = rederive(worlds[big]["A"])
            area = (worlds[big]["A"]["meta"]["Hpx"] / runs["A"]["meta"]["Hpx"]) ** 2
            same_blocks = worlds[big]["A"]["meta"]["Hpx"] / worlds[big]["A"]["meta"]["G"] == runs["A"]["meta"]["Hpx"] / runs["A"]["meta"]["G"]
            keys = [k for k in ROBUST_KEYS if k not in SIZE_SKIP and (same_blocks or not k.startswith(("grid.", "x.", "l.")))]
            rob["size"] = {k: GT.robust(D["A"].get(k), None if db.get(k) is None else db[k] / (area if k in SIZE_PER_AREA else 1.0))
                           for k in keys}
            rob["size_against"] = big
            rob["size_gates"] = {k: bool(G["A"][k] == gb[k]) for k in GATE_KEYS + ["dull"]}
        if late:
            rob["late"] = late
        if "A_first" in worlds[w]:                # the same seeds simulated in two jobs
            rob["rerun"] = {k: GT.robust(D["A"].get(k), df.get(k)) for k in ROBUST_KEYS if k not in ("grid.xresp",)}
            rob["rerun_values"] = {k: [df.get(k), D["A"].get(k)] for k in ("grid.pf8", "grid.ceil8", "grid.sigma_hat", "s.nb_mean", "b.ceil_disp8")}
            rob["rerun_jobs"] = [worlds[w]["A_first"]["_job"], runs["A"]["_job"]]
            rob["xresp_first_biased"] = df.get("grid.xresp")
        if ("A" in runs) and (w, "A") in series:                  # estimator size: even against odd test states
            z = np.load(series[(w, "A")])
            hz = runs["A"]["grid"]["hz"]
            i8 = hz.index(8)
            half = []
            for sl in (slice(0, None, 2), slice(1, None, 2)):
                vc, vo, vp = (np.median(z[k][i8, sl]) for k in ("per_state_v_clim", "per_state_v_orc", "per_state_v_pred"))
                half.append(dict(pf8=float(1 - vo / max(vc, 1e-300)),
                                 ceil8=float((vc - min(vp, vc)) / (vc - vo)) if abs(vc - vo) > 1e-12 else float("nan")))
            rob["split_half"] = dict(pf8=[h["pf8"] for h in half], ceil8=[h["ceil8"] for h in half],
                                     pf8_agree=GT.robust(half[0]["pf8"], half[1]["pf8"]),
                                     ceil8_agree=GT.robust(half[0]["ceil8"], half[1]["ceil8"]),
                                     note="block view, ridge or climatology, medians over 16 states each")
        robust[w] = rob
        wd = os.path.join(a.res, "cards", w)
        os.makedirs(wd, exist_ok=True)
        fig_bytes = None
        if not a.no_fig:
            fig_bytes = figure(w, runs, series, os.path.join(wd, "card.png"))
        open(os.path.join(wd, "card.md"), "w").write(card_md(w, runs, D, G, late, rob, a.rate))
        c0 = runs.get("A") or next(iter(runs.values()))
        curves = {r: dict(hz=c["grid"]["hz"], grid_pf=c["grid"]["pf_med"], grid_ceil=c["grid"]["ceil_med"],
                          grid_ceil_se=c["grid"].get("ceil_med_se"), grid_ceil_mean=c["grid"]["ceil"],
                          bodies_ceil=c["bodies"]["single"]["disp"]["ceil_med"], bodies_pf=c["bodies"]["single"]["disp"]["pf_med"],
                          pop_pf=None if c["pop"].get("empty") else c["pop"]["lin"]["pf_med"],
                          pop_ceil=None if c["pop"].get("empty") else c["pop"]["lin"]["ceil_med"],
                          pl_over_vorc={e: v["pl_over_vorc_med"] for e, v in c["grid"]["pl"].items()},
                          act_D_over_floor={k: v["D_over_floor"] for k, v in c["grid"]["act"].items()},
                          timing=c["timing"], burn=c["burn"], seed=c["seed"]) for r, c in runs.items()}
        json.dump(dict(world=w, role=c0["role"], family=c0["family"], meta=c0["meta"], sizes=c0["sizes"],
                       jobs={r: c["_job"] for r, c in runs.items()},
                       runs={r: dict(derived=D[r], gates=G[r]) for r in runs}, curves=curves, robustness=rob,
                       figure_bytes=fig_bytes, PILOT_NEVER_REUSE_AS_EXAM=True),
                  open(os.path.join(wd, "card.json"), "w"), indent=1, default=float)
        d, g = D[c0["run"]], G[c0["run"]]
        rows.append(dict(world=w, role=c0["role"], family=c0["family"], job=c0["_job"], run=c0["run"], verdict=g["verdict"],
                         sigma_hat=g["sigma_hat_best"], level=g["sigma_hat_level"], pf8=d.get("grid.pf8"), ceil8=d.get("grid.ceil8"),
                         ceil8_mean=d.get("grid.ceil8_mean"), w_theta8=d.get("grid.w_theta8"), pl01=d.get("grid.pl_ratio0.1_8"),
                         pl003=d.get("grid.pl_ratio0.03_8"), bodies=d.get("s.nb_mean"), half_life=d.get("s.half_life_ticks"),
                         v_net=d.get("s.v_net"), events=d.get("s.events100"), body_pf8=d.get("b.pf_disp8"),
                         body_ceil8=d.get("b.ceil_disp8"), quiet8=d.get("b.quiet8"), act_ms=d.get("grid.act_ms"),
                         act_ms_over_vcheap=d.get("grid.act_ms_over_vcheap"),
                         aim_ratio=d.get("grid.aim_ratio"), xresp=d.get("grid.xresp"), tick_share=d.get("grid.tick_share"),
                         pop_tick_share=d.get("pop.tick_share"), member_share=d.get("grid.member_share"),
                         pop_pf8=d.get("pop.pf8"), pop_ceil8=d.get("pop.ceil8"), x_bg=d.get("x.bodies_to_grid8"),
                         l_dceil8=None if d.get("l.dceil8_AB") is None else min(d["l.dceil8_AB"], d["l.dceil8_BA"]),
                         l_dceil16=None if d.get("l.dceil16_AB") is None else min(d["l.dceil16_AB"], d["l.dceil16_BA"]),
                         twin_l1_8=d.get("t.l1_8"), ms_per_mt=1e3 * cost_of(runs), cost_includes_compile=cost_of(runs, True)[1],
                         late_same=None if not late else late["same"],
                         seed_gates_same=None if "seed_gates" not in rob else all(rob["seed_gates"].values()),
                         **{k: g[k] for k in GATE_KEYS}))
    derived["_jobs"] = {w: {r: c["_job"] for r, c in worlds[w].items()} for w in names}
    json.dump(derived, open(os.path.join(a.res, "derived.json"), "w"), default=float)
    json.dump(robust, open(os.path.join(a.res, "robustness.json"), "w"), indent=1, default=float)
    json.dump(rows, open(os.path.join(a.res, "table.json"), "w"), indent=1, default=float)
    # comparison table
    cols = [("world", "world"), ("role", "role"), ("verdict", "verdict"), ("sigma_hat", "sigma_hat"), ("pf8", "PF(8)"),
            ("ceil8", "c(8)"), ("w_theta8", "w_theta(8)"), ("pl01", "PL10%/Vorc"), ("bodies", "bodies"), ("half_life", "half-life"),
            ("body_ceil8", "body law c(8)"), ("act_ms", "act_ms"), ("tick_share", "tick share"), ("member_share", "member share"),
            ("pop_ceil8", "pop c(8)"), ("l_dceil16", "learned dc(16)"), ("late_same", "late = early"), ("ms_per_mt", "ms/member-tick")]
    T = ["| " + " | ".join(h for _, h in cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        T.append("| " + " | ".join(fmt(r[k]) for k, _ in cols) + " |")
    open(os.path.join(a.res, "table.md"), "w").write(
        "# World cards: comparison table (run A; ratios from medians over test states)\n\n" + "\n".join(T) + "\n")
    keys = list(rows[0].keys())
    with open(os.path.join(a.res, "table.csv"), "w") as f:
        f.write(",".join(keys) + "\n")
        for r in rows:
            f.write(",".join(str(r[k]).replace(",", ";") for k in keys) + "\n")
    print(f"{len(names)} worlds, {len(cards)} runs -> {a.res}")


if __name__ == "__main__":
    main()
