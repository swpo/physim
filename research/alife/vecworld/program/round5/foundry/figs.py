"""figs -- posters, short videos and charts of the foundry screen (CPU, seconds).

    python -B figs.py <job_out_dir> [--out results] [--n-gif 6]

Reads the job's outputs (screen thumbnails, cert frames) and results/analysis.json + per_draw.json
(analyze.py first). Writes under results/fig/:
  types_sheet.png      thumbnails of the first draws of every world type (kind 0 orange, kind 1 blue)
  top_candidates.png   the certified worlds by score: six frames of member 0 over 400 ticks
  top_<draw>.gif       short videos of the best worlds (member 0, every 4th tick, 2x upscaled)
  types_bar.png        share of every type over the prior
  closure_profiles.png closure ceiling against horizon: certified worlds and the gliders world
  weights_auc.png      which statistics of the weights predict structure and movers
  speed_closure.png    active worlds in the (ceiling at 8 ticks, net speed) plane
Colours of the charts: the reference categorical palette of the dataviz skill (slots in fixed order).
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

import criteria as CR  # noqa: E402

BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"


def font(size):
    try:
        import matplotlib
        p = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf", "DejaVuSans.ttf")
        return ImageFont.truetype(p, size)
    except Exception:
        return ImageFont.load_default()


def rgb(u8):
    """uint8 (C, H, W) (already scaled to its own 99.9th percentile) -> RGB uint8: kind 0 orange, kind 1 blue."""
    x = np.asarray(u8, np.float32) / 255.0
    a = x[0] ** 0.6
    b = x[1] ** 0.6 if x.shape[0] > 1 else 0 * a
    img = np.stack([a * 1.0 + b * 0.10, a * 0.55 + b * 0.60, a * 0.10 + b * 1.0], -1)
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


def up(img, k):
    return np.kron(img, np.ones((k, k, 1), np.uint8))


def load_thumbs(D):
    files = sorted(f for f in os.listdir(os.path.join(D, "screen")) if f.startswith("chunk_"))
    U, I = [], []
    for f in files:
        z = np.load(os.path.join(D, "screen", f))
        if "thumb_u8" in z.files:
            U.append(z["thumb_u8"])
            I.append(z["thumb_index"])
    return (np.concatenate(U), np.concatenate(I)) if U else (None, None)


def types_sheet(D, per, out, ncol=12, k=2, pad=3, left=190):
    U, I = load_thumbs(D)
    if U is None:
        return None
    pos = {int(d): j for j, d in enumerate(per["draw"])}
    t = np.array([per["type"][pos[int(i)]] for i in I])
    names = per["types"]
    rows = [i for i in range(len(names)) if (t == i).any()]
    cell = 64 * k
    Wd, Hd = left + ncol * (cell + pad) + pad, len(rows) * (cell + pad) + pad
    im = Image.new("RGB", (Wd, Hd), (252, 252, 251))
    dr = ImageDraw.Draw(im)
    tall = np.array(per["type"])
    for r, ti in enumerate(rows):
        y = pad + r * (cell + pad)
        share = float((tall == ti).mean())
        dr.text((8, y + 8), names[ti], fill=(11, 11, 11), font=font(15))
        dr.text((8, y + 30), f"{100 * share:.1f}% of draws", fill=(82, 81, 78), font=font(12))
        dr.text((8, y + 48), f"n = {int((tall == ti).sum())}", fill=(82, 81, 78), font=font(12))
        for c, j in enumerate(np.nonzero(t == ti)[0][:ncol]):
            im.paste(Image.fromarray(up(rgb(U[j]), k)), (left + pad + c * (cell + pad), y))
            dr.text((left + pad + c * (cell + pad) + 3, y + 2), str(int(I[j])), fill=(230, 230, 230), font=font(10))
    p = os.path.join(out, "types_sheet.png")
    im.save(p, optimize=True)
    return p


def top_sheet(D, ana, out, n=12, k=2, pad=3, left=250):
    rows = ana["certification"]["worlds"][:n]
    cell = 64 * k
    nfr = 6
    Wd, Hd = left + nfr * (cell + pad) + pad, len(rows) * (cell + pad) + pad + 18
    im = Image.new("RGB", (Wd, Hd), (252, 252, 251))
    dr = ImageDraw.Draw(im)
    for r, w in enumerate(rows):
        z = np.load(os.path.join(D, "cert", f"frames_{w['draw']:05d}.npz"))
        fr = z["frames"]
        fe = int(z["frame_every"])
        sel = np.linspace(0, len(fr) - 1, nfr).round().astype(int)
        y = 18 + pad + r * (cell + pad)
        cand = w["gates"]["candidate"]
        dr.text((8, y + 4), f"draw {w['draw']}  score {w['score']:.2f}" + ("  *" if cand else ""), fill=(11, 11, 11),
                font=font(13))
        lines = [f"{w['type']}",
                 f"bodies {w['nb_mean']:.1f}, {w['v_net']:.2f} px/tick, r {w['rg']:.1f} px",
                 f"events {w['events100']:.0f} per 100 ticks",
                 f"c(1,8,32) {w['ceil'][0]:.2f} {w['ceil'][3]:.2f} {w['ceil'][5]:.2f}",
                 f"V_orc(8) {w['v_orc'][3]:.3f}  gap {w['gap_max']:.2f}",
                 f"PL(8) at 10% {w['pl'][3]:.3f}"]
        for li, s in enumerate(lines):
            dr.text((8, y + 24 + 15 * li), s, fill=(82, 81, 78), font=font(11))
        for c, j in enumerate(sel):
            im.paste(Image.fromarray(up(rgb(fr[j]), k)), (left + pad + c * (cell + pad), y))
            if r == 0:
                dr.text((left + pad + c * (cell + pad) + 2, 2), f"tick {j * fe}", fill=(82, 81, 78), font=font(11))
    p = os.path.join(out, "top_candidates.png")
    im.save(p, optimize=True)
    return p


def gif(D, draw, out, k=2, max_kb=700):
    z = np.load(os.path.join(D, "cert", f"frames_{draw:05d}.npz"))
    fr = z["frames"]
    p = os.path.join(out, f"top_{draw:05d}.gif")
    for step in (1, 2, 3):
        ims = [Image.fromarray(up(rgb(f), k)).quantize(48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
               for f in fr[::step]]
        ims[0].save(p, save_all=True, append_images=ims[1:], duration=80 * step, loop=0, optimize=True)
        if os.path.getsize(p) <= max_kb * 1024:
            break
    return p, os.path.getsize(p), step * int(z["frame_every"])


# ----------------------------------------------------------------------------- charts
def _mpl():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                         "axes.edgecolor": INK2, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "figure.facecolor": SURF,
                         "axes.facecolor": SURF, "savefig.facecolor": SURF, "axes.axisbelow": True,
                         "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlecolor": INK})
    return plt


def types_bar(ana, out):
    plt = _mpl()
    tab = ana["types"]["table"]
    names = [n for n in CR.TYPES if tab[n]["n"] > 0 or n not in ("invalid", "point", "noisy")]
    fr = [100 * tab[n]["frac"] for n in names]
    se = [100 * tab[n]["se"] for n in names]
    fig, ax = plt.subplots(figsize=(6.4, 0.42 * len(names) + 1.1))
    y = np.arange(len(names))[::-1]
    ax.barh(y, fr, height=0.56, color=BLUE, xerr=se, error_kw=dict(ecolor=INK2, lw=1, capsize=2))
    for yi, f, n in zip(y, fr, names):
        ax.text(f + max(se) + 1.0, yi, f"{f:.1f}%  (n = {tab[n]['n']})", va="center", color=INK, fontsize=9)
    ax.set_yticks(y, names)
    ax.set_xlim(0, max(fr) * 1.32 + 2)
    ax.set_xlabel("share of prior draws (%)")
    ax.grid(axis="y", visible=False)
    ax.set_title(f"World types over the prior ({ana['types']['n']} draws)", loc="left")
    fig.tight_layout()
    p = os.path.join(out, "types_bar.png")
    fig.savefig(p, dpi=140)
    plt.close(fig)
    return p


def closure_profiles(ana, out):
    plt = _mpl()
    hz = list(CR.HZ)
    x = np.arange(len(hz))
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    rows = ana["certification"]["worlds"]
    for w in rows:
        ax.plot(x, w["ceil"], color="#b9b8b2", lw=1.0, zorder=1)
    hi = [w for w in rows if w["gates"]["candidate"]][:2] or rows[:2]
    for w, col in zip(hi, (ORANGE, AQUA)):
        ax.plot(x, w["ceil"], color=col, lw=2, marker="o", ms=5, zorder=3, label=f"foundry draw {w['draw']}")
        ax.text(x[-1] + 0.08, w["ceil"][-1], f"draw {w['draw']}", color=INK, va="center", fontsize=9)
    g = ana.get("gliders_cert_size") or ana.get("gliders_same_estimator")
    if g:
        gc = [c["mean"] for c in g["ceil"]]
        ax.plot(x, gc, color=BLUE, lw=2, marker="o", ms=5, zorder=4, label="gliders, same estimator")
        ax.text(x[-1] + 0.08, gc[-1] - 0.04, "gliders", color=INK, va="center", fontsize=9)
        ax.plot(x, g["published"]["ceiling_linear_set"], color=BLUE, lw=1.2, ls=(0, (4, 2)), zorder=2,
                label="gliders, published (linear predictors)")
    ax.plot([], [], color="#b9b8b2", lw=1.0, label=f"other certified worlds ({len(rows)} in all)")
    ax.set_xticks(x, [str(h) for h in hz])
    ax.set_xlim(-0.2, len(hz) - 0.2)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel("horizon (ticks)")
    ax.set_ylabel("closure ceiling of the cheap level-1 predictor")
    ax.set_title("Block-view closure: certified foundry worlds and the gliders world", loc="left")
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")
    fig.tight_layout()
    p = os.path.join(out, "closure_profiles.png")
    fig.savefig(p, dpi=140)
    plt.close(fig)
    return p


def weights_auc(ana, out):
    plt = _mpl()
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.6))
    for ax, tn in zip(axs, ("structured", "movers")):
        rows = [r for r in ana["weights"]["single"][tn] if np.isfinite(r["auc"])][:8][::-1]
        y = np.arange(len(rows))
        ax.barh(y, [r["auc"] - 0.5 for r in rows], left=0.5, height=0.56, color=BLUE)
        for yi, r in zip(y, rows):
            ax.text(r["auc"] + (0.008 if r["auc"] >= 0.5 else -0.008), yi, f"{r['auc']:.2f}", va="center",
                    ha="left" if r["auc"] >= 0.5 else "right", color=INK, fontsize=9)
        ax.set_yticks(y, [r["feature"] for r in rows])
        ax.axvline(0.5, color=INK2, lw=0.8)
        ax.set_xlim(0.0, 1.0)
        ax.set_xlabel("AUC of the single statistic (0.5 = no information)")
        ax.grid(axis="y", visible=False)
        tg = ana["weights"]["targets"][tn]
        allg = ana["weights"]["groups"][tn]["all"]["auc"]
        ax.set_title(f"{tn}: {100 * tg['frac']:.1f}% of draws; all statistics together {allg:.2f}", loc="left",
                     fontsize=10)
    fig.tight_layout()
    p = os.path.join(out, "weights_auc.png")
    fig.savefig(p, dpi=140)
    plt.close(fig)
    return p


def speed_closure(ana, per, out):
    plt = _mpl()
    t = np.array(per["type"])
    c8 = np.array([np.nan if v is None else v for v in per["ceil8"]], float)
    vn = np.array([np.nan if v is None else v for v in per["v_net"]], float)
    cand = np.array(per["candidate"])
    act = (t >= 5) & np.isfinite(c8) & np.isfinite(vn)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    floor = 3e-3
    ax.scatter(np.clip(c8[act & ~cand], -0.05, 1.05), np.maximum(vn[act & ~cand], floor), s=14, color=BLUE, alpha=0.55,
               lw=0, label=f"active worlds ({int((act & ~cand).sum())})")
    ax.scatter(np.clip(c8[act & cand], -0.05, 1.05), np.maximum(vn[act & cand], floor), s=30, color=ORANGE,
               edgecolor=SURF, lw=0.8, label=f"candidates ({int((act & cand).sum())})", zorder=3)
    g = ana.get("gliders_same_estimator")
    if g:
        # gliders speed in its own px (128^2 grid); halve it to compare at equal box fraction
        ax.scatter([g["ceil"][3]["mean"]], [g["v_net"]["mean"] / 2.0], s=90, marker="D", color=AQUA, edgecolor=SURF,
                   lw=0.8, zorder=4, label="gliders (speed in 1/64 of the box)")
        ax.annotate("gliders", (g["ceil"][3]["mean"], g["v_net"]["mean"] / 2.0), xytext=(6, 6),
                    textcoords="offset points", color=INK, fontsize=9)
    ax.set_yscale("log")
    ax.set_xlabel("closure ceiling at 8 ticks (cheap level-1 predictor)")
    ax.set_ylabel("net body speed (px per tick)")
    ax.set_title("Active worlds: closure at 8 ticks against body speed", loc="left")
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")
    fig.tight_layout()
    p = os.path.join(out, "speed_closure.png")
    fig.savefig(p, dpi=140)
    plt.close(fig)
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job_out")
    ap.add_argument("--out", default=os.path.join(HERE, "results"))
    ap.add_argument("--n-gif", type=int, default=6)
    a = ap.parse_args()
    ana = json.load(open(os.path.join(a.out, "analysis.json")))
    import gzip
    per = json.load(gzip.open(os.path.join(a.out, "per_draw.json.gz"), "rt"))
    fd = os.path.join(a.out, "fig")
    os.makedirs(fd, exist_ok=True)
    made = {}
    made["types_sheet"] = types_sheet(a.job_out, per, fd)
    made["types_bar"] = types_bar(ana, fd)
    made["weights_auc"] = weights_auc(ana, fd)
    made["speed_closure"] = speed_closure(ana, per, fd)
    if "certification" in ana:
        made["top_candidates"] = top_sheet(a.job_out, ana, fd)
        made["closure_profiles"] = closure_profiles(ana, fd)
        gifs = []
        rows = ana["certification"]["worlds"]
        pick = [w for w in rows if w["gates"]["candidate"]][:a.n_gif]
        pick += [w for w in rows if w not in pick][:a.n_gif - len(pick)]
        for w in pick:
            p, size, tpf = gif(a.job_out, w["draw"], fd)
            gifs.append(dict(draw=w["draw"], file=os.path.relpath(p, a.out), bytes=size, ticks_per_frame=tpf))
        made["gifs"] = gifs
    out = {k: (os.path.relpath(v, a.out) if isinstance(v, str) else v) for k, v in made.items() if v}
    with open(os.path.join(a.out, "figs.json"), "w") as f:
        json.dump(out, f, indent=1)
    tot = sum(os.path.getsize(os.path.join(fd, f)) for f in os.listdir(fd))
    print(json.dumps(out, indent=1))
    print(f"fig folder: {tot / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
