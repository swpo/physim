"""bench/make_figs.py — figures for the post from results/gpu_bench.json.
Produces docs/assets/blobs/gpu_roofline.png, gpu_throughput.png, gpu_parity.png.
"""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
GPU = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, GPU)
from bench.roofline import (step_flops_per_field, step_bytes_per_field, A100)

DOCS = os.path.normpath(os.path.join(GPU, "..", "..", "..", "docs", "assets",
                                     "blobs"))
BENCH = json.load(open(os.path.join(GPU, "results", "gpu_bench.json")))


def rows(kind, **match):
    out = []
    for r in BENCH:
        if r.get("kind") != kind:
            continue
        if all(r.get(k) == v for k, v in match.items()):
            out.append(r)
    return out


def latest(rws, key):
    """Keep the last row per unique key tuple."""
    d = {}
    for r in rws:
        d[tuple(r.get(k) for k in key)] = r
    return list(d.values())


# ------------------------------------------------------------------ roofline
def fig_roofline(pod_rows_f32, pod_rows_f64, out):
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    bw = A100["bw_GBs"] * 1e9
    peak32 = A100["fp32_TFLOPS"] * 1e12
    peak64 = A100["fp64_TFLOPS"] * 1e12
    ai = np.logspace(-1, 2.2, 200)
    ax.plot(ai, np.minimum(ai * bw, peak32) / 1e12, "-", color="#0969da",
            lw=2, label="A100 roofline (fp32 non-tensor, 1.56 TB/s)")
    ax.plot(ai, np.minimum(ai * bw, peak64) / 1e12, "--", color="#8250df",
            lw=1.5, label="fp64 ceiling")
    # measured points: achieved flops = model flops / measured time
    for rws, mk, lab in ((pod_rows_f32, "o", "f32"), (pod_rows_f64, "s", "f64")):
        xs, ys, ann = [], [], []
        for r in rws:
            N = r["N"]; nf = r.get("nf", 9); B = r.get("B", 1)
            fl, _, _ = step_flops_per_field(N)
            by = step_bytes_per_field(N, r["dtype"])
            t = r["ms_per_step"] * 1e-3
            xs.append(fl / by)
            ys.append(fl * nf * B / t / 1e12)
            ann.append(f"B{B} N{N}")
        ax.plot(xs, ys, mk, ms=7, label=f"measured ({lab})",
                color="#d1242f" if lab == "f32" else "#9a6700", zorder5 := 5)
        for x, y, a in zip(xs, ys, ann):
            ax.annotate(a, (x, y), textcoords="offset points",
                        xytext=(6, -4), fontsize=7, color="#57606a")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("arithmetic intensity (flop / byte)")
    ax.set_ylabel("achieved Tflop/s")
    ax.set_title("blob step kernel on the A100 roofline")
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=9, loc="upper left")
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    print("wrote", out)


# ---------------------------------------------------------------- throughput
def fig_throughput(out):
    f32 = latest(rows("batch_sweep", dtype="f32"), ("B",))
    f64 = latest(rows("batch_sweep", dtype="f64"), ("B",))
    grid32 = latest(rows("grid_sweep", dtype="f32"), ("N",))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6))
    for rws, mk, lab, col in ((f32, "o-", "f32", "#0969da"),
                              (f64, "s--", "f64", "#8250df")):
        rws = sorted(rws, key=lambda r: r["fields"])
        ax1.plot([r["fields"] for r in rws],
                 [r["us_per_field_step"] for r in rws], mk, label=lab,
                 color=col)
    ax1.axhline(440, color="#d1242f", ls=":", lw=1.5)
    ax1.text(14, 470, "CPU single-core (measured 0.44 ms/field-step)",
             fontsize=8, color="#d1242f")
    ax1.set_xscale("log"); ax1.set_yscale("log")
    ax1.set_xlabel("total fields in batch (worlds x fields/world), 256$^2$")
    ax1.set_ylabel("$\\mu$s per field-step")
    ax1.set_title("batching amortizes everything")
    ax1.grid(alpha=0.3, which="both"); ax1.legend(fontsize=9)
    grid32 = sorted(grid32, key=lambda r: r["N"])
    ax2.plot([r["N"] for r in grid32], [r["ms_per_step"] for r in grid32],
             "o-", color="#0969da", label="GPU f32 (9-field world)")
    cpu = {256: 4.10, 512: 18.75, 1024: 86.0}
    ax2.plot(list(cpu), list(cpu.values()), "^:", color="#d1242f",
             label="CPU 1-core (records incl.)")
    ax2.set_xscale("log", base=2); ax2.set_yscale("log")
    ax2.set_xlabel("grid N (single world)")
    ax2.set_ylabel("ms per step")
    ax2.set_title("single-world scaling")
    ax2.grid(alpha=0.3, which="both"); ax2.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    print("wrote", out)


# -------------------------------------------------------------------- parity
def fig_parity(out):
    par = json.load(open(os.path.join(GPU, "results", "gate_parity.json")))[-1]
    ref = json.load(open(os.path.normpath(os.path.join(
        GPU, "..", "l0", "complexity", "v1_scores_all.json"))))
    names = ["m0", "m4", "xv", "bf", "pred", "coex", "mv3"]
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    xs = np.arange(len(names))
    for i, n in enumerate(names):
        cpu = [ref[f"gt_{n}_s{s}"]["interest"] for s in (1, 2, 3)]
        v = par["verdicts"][n]
        gpu = v["gpu"]
        band = v["band"]
        ax.add_patch(plt.Rectangle((i - 0.32, band[0]), 0.64,
                                   band[1] - band[0], alpha=0.15,
                                   color="#0969da", lw=0))
        ax.plot([i - 0.13] * 3, cpu, "o", color="#57606a", ms=6,
                label="CPU seeds" if i == 0 else None)
        ax.plot([i + 0.13] * 3, gpu, "o", color="#d1242f", ms=6,
                label="GPU seeds" if i == 0 else None)
    ax.set_xticks(xs, names)
    ax.set_ylabel("interest score (metrics_v1, locked)")
    ax.set_title("descriptor parity: locked assay battery, CPU vs GPU runs\n"
                 "(shaded = acceptance band from CPU seed scatter)")
    ax.grid(alpha=0.3, axis="y")
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    print("wrote", out)


if __name__ == "__main__":
    os.makedirs(DOCS, exist_ok=True)
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "roofline"):
        f32 = latest(rows("batch_sweep", dtype="f32"), ("B",)) + \
              latest(rows("grid_sweep", dtype="f32"), ("N",))
        f64 = latest(rows("batch_sweep", dtype="f64"), ("B",))
        f32 = [r for r in f32 if r.get("backend", "").startswith("cuda")]
        f64 = [r for r in f64 if r.get("backend", "").startswith("cuda")]
        fig_roofline(f32, f64, os.path.join(DOCS, "gpu_roofline.png"))
    if which in ("all", "throughput"):
        fig_throughput(os.path.join(DOCS, "gpu_throughput.png"))
    if which in ("all", "parity"):
        fig_parity(os.path.join(DOCS, "gpu_parity.png"))
