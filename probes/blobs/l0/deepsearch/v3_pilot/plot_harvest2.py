"""Build POST12 audit charts; optionally make posters from local captured films.

Run from the repository root:
    ~/.venvs/bk3/bin/python -B probes/blobs/l0/deepsearch/v3_pilot/plot_harvest2.py --posters

Reads the frozen audit CSV/JSON files and, with --posters, already-extracted
film.npz captures. Does not execute metrics or simulations, modify audit data,
extract archives, or write videos. All score labels refer to original assays.
"""
from pathlib import Path
import argparse
import csv
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
AUDIT = HERE / "harvest2_audit"
OUT = ROOT / "docs/blobs/media/v3pilot"
BLUE, ORANGE, GREEN = "#2166a5", "#bd570d", "#24834d"


def read_csv(name):
    with (AUDIT / name).open(newline="") as stream:
        return list(csv.DictReader(stream))


def save(fig, name):
    fig.savefig(OUT / name, dpi=115, facecolor="white",
                pil_kwargs={"optimize": True})
    plt.close(fig)
    # Display-only palette compression keeps the page light; source arrays stay untouched.
    with Image.open(OUT / name) as image:
        palette = image.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT,
                                                dither=Image.Dither.NONE)
        palette.save(OUT / name, optimize=True)
    print(name, (OUT / name).stat().st_size, "bytes", flush=True)


def charts():
    rows = read_csv("screen_by_generation.csv")
    partial = sorted((r for r in rows if r["island"] == "both" and
                      r["C9_mode"] == "partial"), key=lambda r: int(r["gen"]))
    all_screens = sorted((r for r in rows if r["island"] == "both" and
                          r["C9_mode"] == "all"), key=lambda r: int(r["gen"]))
    assert len(partial) == len(all_screens) == 12
    assert sum(int(r["n"]) for r in all_screens) == 2099
    assert sum(int(r["c9_full_n"]) for r in all_screens) == 13
    x = np.array([int(r["gen"]) for r in partial])
    means = [float(r["c9_mean"]) for r in partial]
    maxima = [float(r["c9_max"]) for r in partial]
    measured = [int(r["c9_measured_n"]) for r in partial]
    denominators = np.array([int(r["n"]) for r in all_screens])
    successes = np.array([int(r["qualifying_040_n"]) for r in all_screens])
    assert (int(successes[:7].sum()), int(successes[7:].sum())) == (241, 159)

    fig, axes = plt.subplots(2, 1, figsize=(9.6, 6.1), sharex=False,
                             gridspec_kw={"height_ratios": [1.35, 1]})
    fig.subplots_adjust(left=.09, right=.985, top=.87, bottom=.18, hspace=.36)
    fig.suptitle("Creative screens only: two islands, generations 1–12",
                 x=.09, ha="left", fontsize=14, fontweight="bold", y=.975)
    fig.text(.09, .922, "No selected reseeds or imports in either panel.",
             fontsize=10, color="#57606a")
    for ax in axes:
        ax.axvspan(7.5, 8.5, color="#fff1cf", zorder=0)
        ax.axvspan(8.5, 12.5, color="#eaf3fb", zorder=0)
        ax.axvline(7.5, color="#999999", lw=.8, ls="--")
        ax.axvline(8.5, color="#999999", lw=.8, ls="--")
        ax.set_xlim(.5, 12.5)
        ax.grid(axis="y", alpha=.2)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].plot(x, maxima, "s-", color=ORANGE, ms=4, lw=1.5,
                 label="Screen maximum")
    axes[0].plot(x, means, "o-", color=BLUE, ms=4, lw=1.7,
                 label="Screen mean")
    axes[0].set_ylim(0, 1)
    axes[0].set_ylabel("Partial C9")
    axes[0].set_title("Partial mode only; n = measured screens; missing C9 is not zero", loc="left", fontsize=10)
    axes[0].legend(loc="upper left", ncol=2, frameon=False, fontsize=9)
    axes[0].tick_params(axis="x", labelbottom=True)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels([f"{g}\nn={n}" for g, n in zip(x, measured)], fontsize=8)

    rates = successes / denominators
    axes[1].plot(x, rates, "o-", color=GREEN, ms=5, lw=1.5)
    axes[1].set_ylim(0, .32)
    axes[1].yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    axes[1].set_ylabel("Qualifying / emitted")
    axes[1].set_xlabel("Generation")
    axes[1].set_title("Common W9 = 0.40; status=ok, C9 ≥ 0.4, common interest ≥ 60",
                      loc="left", fontsize=10)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels([str(g) for g in x], fontsize=9)
    for g, q, n, rate in zip(x, successes, denominators, rates):
        axes[1].annotate(f"{q}/{n}", (g, rate), xytext=(0, 7),
                         textcoords="offset points", ha="center", fontsize=8)
    axes[1].tick_params(axis="x", labelsize=8)
    fig.text(.09, .03,
             "Top excludes 13 full-C9 screens in generation 1. Bottom includes those 13; "
             "all later measured screens are partial.\n"
             "Bottom denominators include failed/missing screens. Shading marks g8 and g9–12 "
             "configuration phases.\n"
             "Descriptive counts, not IID trials or a causal comparison. Source: harvest2_audit/screen_by_generation.csv",
             fontsize=8, color="#57606a", linespacing=1.5)
    save(fig, "v3pilot_trajectory.png")

    rows = read_csv("operator_rates.csv")
    selected = {(r["cohort"], r["op"]): r for r in rows
                if r["island"] == "both" and r["W9"] == "0.4" and
                r["cohort"] in ("baseline_g1_7", "continuation_g8_12")}
    ops = ["merge_spatial_ic", "mint_bilin", "delete_bilin", "merge_cross_edge",
           "add_chan", "merge_slow_tanh", "mutate", "merge_share_chan", "dup_act", "immigrate"]
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 6.2), sharey=True)
    fig.subplots_adjust(left=.215, right=.985, top=.79, bottom=.225, wspace=.12)
    fig.suptitle("Operator screen yield at common W9 = 0.40", x=.03,
                 ha="left", fontsize=14, fontweight="bold", y=.97)
    fig.text(.03, .918, "Qualifying screens / all emitted screens for that origin operator; "
             "no confirmation rows in numerators.", fontsize=9, color="#57606a")
    y = np.arange(len(ops))
    for ax, cohort, color, title in zip(axes,
            ("baseline_g1_7", "continuation_g8_12"), (BLUE, ORANGE),
            ("Baseline g1–7 · 241/1,376", "Continuation g8–12 · 159/723")):
        ax.set_title(title, loc="left", fontsize=10, pad=10)
        ax.set_xlim(0, .64)
        ax.set_xticks([0, .2, .4, .6])
        ax.xaxis.set_major_formatter(PercentFormatter(1, decimals=0))
        ax.grid(axis="x", alpha=.2)
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
        for j, op in enumerate(ops):
            r = selected.get((cohort, op))
            if r is None:
                ax.text(.015, j, "not emitted", va="center", fontsize=8, color="#777777")
                continue
            q, n = int(r["screen_success_n"]), int(r["base_candidates_n"])
            rate = q / n
            assert abs(rate - float(r["screen_success_rate"])) < 1e-12
            ax.barh(j, rate, height=.65, color=color, alpha=.88)
            ax.text(rate + .012, j, f"{q}/{n} · {rate:.1%}", va="center", fontsize=8)
        ax.set_xlabel("Observed screen yield", fontsize=9)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels([op + (" *" if op == "merge_spatial_ic" else "")
                            for op in ops], fontsize=9)
    axes[0].invert_yaxis()
    fig.text(.03, .03,
             "* Baseline SIC includes 13 full-C9 measurements (4 qualifying); "
             "the other measured screens are partial.\n"
             "  Continuation is entirely partial. Missing/failed screens remain in each denominator.\n"
             "  Parent choice, ICs, genotypes and settings differ; these are not randomized operator effects.\n"
             "Source: harvest2_audit/operator_rates.csv. SIC = merge_spatial_ic.",
             fontsize=8, color="#57606a", linespacing=1.5)
    save(fig, "v3pilot_operators.png")


def posters():
    identity = json.loads((AUDIT / "production_film_identity_checks.json").read_text())
    # Activator overlays, not species labels. All channels use the same mapping.
    colors = np.array([[.15, .50, 1.0], [1.0, .35, .10],
                       [.10, .90, .45], [.85, .30, .90]], dtype=np.float32)
    for entry in identity["production_requests"]:
        name = entry["capture_name"]
        assert entry["request_genome_matches_row_core"]
        assert not entry["known_wrong_genome_confirmation"]
        request_path = Path(entry["request_path"])
        req = json.loads(request_path.read_text())
        with np.load(request_path.with_name("film.npz"), allow_pickle=False) as data:
            ts = data["ts"]
            na = int(data["na"])
            assert na == 4
            assert float(data["seed"]) == req["original"]["seed"]
            assert str(data["cand"]) == req["original"]["cand"]
            assert float(ts[-1]) == req["replay"]["T"]
            indices = [int(np.argmin(np.abs(ts - fraction * ts[-1])))
                       for fraction in (.5, .75, 1.0)]
            frames = data["frames"][indices].astype(np.float32)
            show_ts = ts[indices]
        u0 = np.array([a["u0"] for a in req["genome"]["acts"]], dtype=np.float32)
        excess = np.maximum(frames - u0[None, :, None, None], 0)
        maxima = np.maximum(excess.max(axis=(0, 2, 3)), 1e-9)
        scaled = excess / maxima[None, :, None, None]
        rgb = np.clip(np.einsum("tahw,ac->thwc", scaled, colors), 0, 1)
        fig, axes = plt.subplots(1, 3, figsize=(8.4, 3.45))
        fig.subplots_adjust(left=.01, right=.99, bottom=.16, top=.83, wspace=.025)
        fig.suptitle(name + " · GPU re-simulation", x=.015, ha="left", y=.98,
                     fontsize=11, fontweight="bold")
        for ax, image, t in zip(axes, rgb, show_ts):
            ax.imshow(image, origin="lower", interpolation="nearest")
            ax.set_title(f"Replay t = {t:,.0f} tu", fontsize=9, pad=5)
            ax.set_axis_off()
        fig.text(.015, .1, "Activator-field overlay (not species):", fontsize=8, color="#57606a")
        for j, color in enumerate(colors):
            fig.text(.40 + .085*j, .1, f"u{j + 1}", color=color*.8, fontsize=9, fontweight="bold")
        fig.text(.015, .045,
                 "Positive excess above u0; per-film / per-activator maximum scale, fixed across these three times.",
                 fontsize=7.7, color="#57606a")
        save(fig, "late_" + name + ".png")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--posters", action="store_true",
                        help="Also read the six local film.npz files to create late-time poster strips")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.labelcolor": "#333333", "text.color": "#222222"})
    charts()
    if args.posters:
        posters()


if __name__ == "__main__":
    main()
