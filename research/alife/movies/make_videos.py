"""Comparison videos: a world next to its matched control, plus the lab highlight reel.

Each comparison re-runs the world files with one seed for every arm, renders all arms with
shared fixed colour scales (so brightness differences are real), and adds a live statistic
and the committee's verdict as a caption. Run from research/alife/:

    python movies/make_videos.py sim VIDEO ARM_INDEX     # one arm -> movies/_cache/VIDEO_ARM.npz
    python movies/make_videos.py compose VIDEO           # -> movies/VIDEO.mp4 (+ VIDEO.jpg poster)
    python movies/make_videos.py reel                    # -> movies/lab_reel.mp4 from threads/*/movies/showcase.mp4
    python movies/make_videos.py list
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.dont_write_bytecode = True
LAB = Path(__file__).resolve().parents[1]
OUT = LAB / "movies"
CACHE = OUT / "_cache"
FPS = 15  # reel; comparisons default to 10 fps (VIDEOS[...]['fps'])
WIDTH, HEIGHT = 1280, 720
BG = (12, 13, 18)
FG = (232, 234, 240)
DIM = (150, 155, 170)
ACCENT = (255, 196, 90)
ARM_COLORS = [(110, 200, 255), (255, 140, 80), (150, 230, 120)]

CYAN, ORANGE, MAGENTA, GREEN = (0.10, 0.85, 0.95), (1.00, 0.55, 0.10), (0.95, 0.20, 0.55), (0.45, 0.95, 0.30)
BLUE, WHITE, YELLOW = (0.40, 0.45, 1.00), (1.0, 1.0, 1.0), (0.95, 0.90, 0.25)

# show: (channel-name prefix, rgb weight); channels are matched by name per arm, because an
# ablation's world file may expose a different channel list than its parent.
VIDEOS = {
    "membrane_ring_does_work": dict(
        title="Does the membrane ring do work?",
        subtitle="autopoiesis: phase_membrane vs its matched chi = 0 control (seed 0, 128², t = 0-8000)",
        arms=[("threads/autopoiesis/worlds/phase_membrane/world.py", "phase_membrane: links adsorb at the wall"),
              ("threads/autopoiesis/worlds/phase_membrane_chi0/world.py", "control: chi = 0, no adsorption")],
        seed=0, frames=160, spf=50,
        show=[("K catalyst", CYAN), ("L link", (1.0, 0.35, 0.75))],
        stat="count", stat_label="cells",
        legend="cyan = catalyst K   pink = link L (the material channel of the ring)",
        caption=["Both form cells from noise and divide by pinching. Only the world with adsorption grows a link ring",
                 "(rim/core 1.51-1.72 vs 1.12-1.14). The ring does work: cells are ~2x larger and divide ~3x less",
                 "(15-17 vs 42-43 cells over 3 seeds). Verdict: phase_membrane L6[L3] medium; control L6[L2] medium."]),
    "selection_vs_twin": dict(
        title="Selection against an identical-event twin",
        subtitle="autopoiesis: membrane_evo arms (seed 4, 128², t = 0-40000). Same flips, same disk deaths, same RNG",
        arms=[("threads/autopoiesis/worlds/membrane_evo_up/world.py", "K2 link yield 1.3b"),
              ("threads/autopoiesis/worlds/membrane_evo/world.py", "neutral twin: K2 = K1"),
              ("threads/autopoiesis/worlds/membrane_evo_down/world.py", "K2 link yield 0.7b")],
        seed=4, frames=160, spf=250,
        show=[("K1", BLUE), ("K2", ORANGE), ("membrane", WHITE)],
        stat="share", stat_label="K2 share of catalyst", share=("K1", "K2"),
        legend="blue = kind K1 catalyst   orange = kind K2 catalyst   white = wall",
        caption=["Kinds differ only in link yield. Over 10 seeds the final K2 biomass share is 0.85-0.97 (up, 8/10 seeds),",
                 "0-0.46 (twin) and <= 0.04 (down). Conversions <= flips in 30/30 runs. Caveat: the sweep runs through",
                 "fragments cut by the random disk deaths that reseal and regrow. Verdict: L7[L3] low (skeptic dissents)."]),
    "gate_holds_cargo": dict(
        title="A membrane gate holds a fast cargo",
        subtitle="fisim-beyond-laplacian: xcell-a vs gate-off control (beta 5 -> 0) (seed 0, 160², t = 0-400)",
        arms=[("threads/fisim-beyond-laplacian/worlds/xcell-a/world.py", "xcell-a: cargo D = 4 exp(-5 m)"),
              ("threads/fisim-beyond-laplacian/worlds/xcell-a-nogate/world.py", "control: gate off, D = 4")],
        seed=0, frames=200, spf=100,
        show=[("m ", ORANGE), ("c ", CYAN)],
        stat="inside", stat_label="cargo inside cells", inside=("u ", "c "),
        legend="orange = membrane m (band-deposited, Cahn-Hilliard sharpened)   cyan = cargo c",
        caption=["Gliding m4 cells deposit a membrane ring (orange wakes trail behind them). With the gate the fast cargo",
                 "stays in the cell: 1.24 at the centre vs 0.43 gate off. Caveat: the control keeps D = 4 rather than a lowered",
                 "uniform D, and the body is plain m4, so the compartment is passive. Verdict: xcell-a L4b[L3] medium."]),
    "metabolism_needs_food": dict(
        title="Metabolism: replicators that need food",
        subtitle="lenia-multichannel: mcf-MIRd vs no-regrowth control (seed 0, 192², t = 0-400)",
        arms=[("threads/lenia-multichannel/worlds/mcf-MIRd/world.py", "mcf-MIRd: food regrows (rho = 0.01)"),
              ("threads/lenia-multichannel/worlds/mcf-MIRd-norefill/world.py", "control: no regrowth (rho = 0)")],
        seed=0, frames=200, spf=20,
        show=[("A0", ORANGE), ("A1", CYAN), ("A2", MAGENTA), ("F", (0.10, 0.30, 0.12))],
        stat="count", stat_label="cells",
        legend="orange/cyan/magenta = Lenia channels A0-A2   green = food F (matter is built only from food)",
        caption=["Chan's planted replicator, rewritten so matter can only be built from a consumed, regrowing food.",
                 "Without regrowth the population is extinct in 3/3 seeds; with it 11-16 cells survive.",
                 "Replication itself is Chan's result. Verdict: mcf-MIRd L6[L2] + L4c, high."]),
    "trail_propulsion": dict(
        title="Self-propulsion from a self-repellent trail",
        subtitle="chemotaxis-motility: kstrail vs chi_h = 0 (seed 0, 192², t = 0-600)",
        arms=[("threads/chemotaxis-motility/worlds/kstrail/world.py", "kstrail: repelled by own trail h"),
              ("threads/chemotaxis-motility/worlds/kstrail/world.py", "control: chi_h = 0", {"chi_h": 0.0})],
        seed=0, frames=200, spf=60,
        show=[("rho", WHITE), ("a", ORANGE), ("h", CYAN)],
        stat="speed", stat_label="body speed (px per unit t)",
        legend="white = cells rho   orange = attractant a   cyan = slow repellent trail h",
        caption=["Keller-Segel aggregation plus a second, slow repellent each cell secretes. Spots become rings, then",
                 "crescents that swim away from their own trail; with chi_h = 0 they stay static spots. Passes dt/2 and",
                 "2x resolution. Known drift-bifurcation physics; no Laplacian-only control yet. Verdict: kstrail L4b[L2] high."]),
    "spores_were_overshoot": dict(
        title="A judge catch: the spores were integrator overshoot",
        subtitle="particle-life: sporecell2-sel at three time steps (seed 0, same physical time t = 0-200)",
        arms=[("threads/particle-life/worlds/sporecell2-sel/world.py", "dt = 0.02 (the sprint 1-2 map)"),
              ("threads/particle-life/worlds/sporecell2-sel-dt2/world.py", "dt = 0.01"),
              ("threads/particle-life/worlds/sporecell2-sel/world.py", "dt = 0.005", {}, {"dt": 0.005})],
        seed=0, frames=100, spf=(100, 200, 400), fps=7,
        particles={0: ((90, 90, 100), 0.7), 1: ((0, 220, 255), 1.6), 2: ((255, 150, 40), 1.6), 3: ((255, 60, 150), 1.6)},
        stat="pfree", stat_label="free cores", stat2="pcells", stat2_label="cells",
        legend="grey = food   cyan = core kind 0   magenta = core kind 1   orange = membrane",
        caption=["Same world, seed and physical time at three step sizes. The thread's convergence test: mean free cores",
                 "(t = 60-200) 127 / 40 / 6, cells at t = 200 24 / 14 / 5. The skeptic saw cores jump farther than the interaction",
                 "range in one step at dt = 0.02. Spores, and the selection built on them, belonged to the discrete map. Final: L2."]),
}


# ------------------------------------------------------------------ simulation
def sim(name, k):
    spec = VIDEOS[name]
    arm = spec["arms"][k]
    if len(arm) > 2 and arm[2]:  # parameter override, read by worlds that honour WORLD_P
        os.environ["WORLD_P"] = json.dumps(arm[2])
    sys.path.insert(0, str(LAB))
    from labkit.run import _fields, _matter
    from labkit.world import load_world

    W = load_world(str(LAB / arm[0]))
    if len(arm) > 3:  # META override (e.g. a time step for worlds whose step() reads META["dt"])
        W.META.update(arm[3])
    spf = spec["spf"][k] if isinstance(spec["spf"], tuple) else spec["spf"]
    state = W.init(spec["seed"], tuple(W.META["size"]))
    F, mat, parts = [], [], []
    for f in range(spec["frames"] + 1):
        if f:
            for _ in range(spf):
                state = W.step(state)
        fr = _fields(W, state)
        F.append(fr.astype(np.float16))
        mat.append(_matter(W, fr))
        if hasattr(W, "particles"):
            parts.append(np.asarray(W.particles(state), np.float32))
        if f % 20 == 0:
            print(f"{name}[{k}] frame {f}/{spec['frames']}", flush=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    extra = {}
    if parts:
        n = np.array([len(p) for p in parts])
        extra = {"parts": np.concatenate(parts), "parts_n": n}
    np.savez_compressed(CACHE / f"{name}_{k}.npz", fields=np.stack(F), matter=np.stack(mat),
                        channels=np.array(W.META["channels"]), dt_frame=spf * float(W.META["dt"]),
                        meta=json.dumps({key: W.META.get(key) for key in ("smooth", "threshold", "periodic", "domain")}),
                        **extra)


# ------------------------------------------------------------------ drawing helpers
def font(size, bold=False):
    for path in ([f"/usr/share/fonts/opentype/inter/Inter-{'SemiBold' if bold else 'Regular'}.otf",
                  f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf"]):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def chan(names, prefix):
    for i, n in enumerate(names):
        if str(n).startswith(prefix) or str(n).split()[0] == prefix.strip():
            return i
    raise KeyError(f"no channel {prefix!r} in {list(names)}")


def counts(d):
    """labkit's component count per frame (same normalization, threshold and min area as the packs)."""
    sys.path.insert(0, str(LAB))
    from labkit import metrics as M
    from labkit.run import _default_min_area, _normalize_matter

    meta = json.loads(str(d["meta"]))
    mat = d["matter"].astype(np.float32)
    mn, thr, _, _ = _normalize_matter(mat, meta, True, meta.get("threshold"))
    area = _default_min_area(*mat.shape[1:])
    return mn, thr, [M.segment(x, thr, area, True) for x in mn]


def speeds(d):
    """Mean centroid speed of bodies between consecutive frames (nearest-centroid matching, periodic)."""
    from scipy import ndimage

    _, _, segs = counts(d)
    H, Wd = d["matter"].shape[1:]
    out, prev = [0.0], None
    for seg in segs:
        lab, n = seg["lab"], seg["n"]
        # centroids on the torus via angle averaging
        yy, xx = np.mgrid[0:H, 0:Wd]
        c = []
        for j in range(1, n + 1):
            m = lab == j
            ay = np.angle(np.exp(2j * np.pi * yy[m] / H).mean()) * H / (2 * np.pi) % H
            ax = np.angle(np.exp(2j * np.pi * xx[m] / Wd).mean()) * Wd / (2 * np.pi) % Wd
            c.append((ay, ax))
        c = np.array(c).reshape(-1, 2)
        if prev is not None and len(c) and len(prev):
            dy = (c[:, None, 0] - prev[None, :, 0] + H / 2) % H - H / 2
            dx = (c[:, None, 1] - prev[None, :, 1] + Wd / 2) % Wd - Wd / 2
            dist = np.sqrt(dy ** 2 + dx ** 2).min(1)
            out.append(float(np.median(dist[dist < 8])) / float(d["dt_frame"]) if (dist < 8).any() else 0.0)
        elif prev is not None:
            out.append(0.0)
        prev = c
    del ndimage
    return np.array(out)


def particle_clusters(d, r=3.0, smin=15):
    """Cells = clusters of >= smin matter particles (link length r grid px, periodic); free = core particles outside them.

    With r = 3 px (3/8 of the interaction range) and smin = 15 this reproduces the particle-life
    thread's own counts (14 cells at t = 200 for sporecell2-sel at dt = 0.01, seed 0)."""
    from scipy.sparse.csgraph import connected_components
    from scipy.spatial import cKDTree

    off = np.concatenate([[0], np.cumsum(d["parts_n"])])
    box = float(d["fields"].shape[-1])
    cells, free = [], []
    for f in range(len(d["parts_n"])):
        P = d["parts"][off[f]:off[f + 1]]
        P = P[P[:, 2] > 0]
        if not len(P):
            cells.append(0)
            free.append(0)
            continue
        tree = cKDTree(P[:, :2] % box, boxsize=box)
        _, lab = connected_components(tree.sparse_distance_matrix(tree, r, output_type="coo_matrix"), directed=False)
        size = np.bincount(lab)
        core = (P[:, 2] == 1) | (P[:, 2] == 3)
        cells.append(int((size >= smin).sum()))
        free.append(int((core & (size[lab] < smin)).sum()))
    return np.array(cells), np.array(free)


def stat_series(spec, d, kind=None):
    names = list(d["channels"])
    F = d["fields"].astype(np.float32)
    kind = kind or spec["stat"]
    if kind == "count":
        return np.array([s["n"] for s in counts(d)[2]], float), "{:.0f}"
    if kind == "share":
        a, b = (chan(names, p) for p in spec["share"])
        A, B = np.clip(F[:, a], 0, None).sum((1, 2)), np.clip(F[:, b], 0, None).sum((1, 2))
        return B / np.maximum(A + B, 1e-12), "{:.2f}"
    if kind == "inside":
        u, c = (chan(names, p) for p in spec["inside"])
        mn, thr, _ = counts(d)
        body = mn > thr
        C = np.clip(F[:, c], 0, None)
        return (C * body).sum((1, 2)) / np.maximum(C.sum((1, 2)), 1e-12), "{:.0%}"
    if kind == "speed":
        return speeds(d), "{:.2f}"
    if kind in ("pcells", "pfree"):
        cells, free = particle_clusters(d)
        return (cells if kind == "pcells" else free).astype(float), "{:.0f}"
    raise ValueError(kind)


def field_rgb(F, idx, colors, scales):
    acc = np.zeros(F.shape[1:] + (3,), np.float32)
    for i, col, (lo, hi) in zip(idx, colors, scales):
        x = np.clip((F[i].astype(np.float32) - lo) / (hi - lo), 0, 1)
        acc += x[..., None] * np.array(col, np.float32)
    return (np.clip(1 - np.exp(-1.6 * acc), 0, 1) * 255).astype(np.uint8)


def particle_rgb(P, view, size, styles):
    img = Image.new("RGB", (size, size), (6, 6, 10))
    dr = ImageDraw.Draw(img)
    s = size / view[0]
    order = np.argsort(P[:, 2] != 0)  # food first, matter on top
    for (x, y, t) in P[order]:  # particles(): grid-unit (x, y) then type
        col, r = styles.get(int(t), ((230, 230, 230), 1.2))
        r = r * size / 512
        px, py = x * s, y * s
        dr.ellipse([px - r, py - r, px + r, py + r], fill=col)
    return np.asarray(img)


def wrap_text(dr, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if dr.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def spark(dr, box, series, upto, color, fmt, vmax):
    x0, y0, x1, y1 = box
    dr.rectangle(box, outline=(45, 48, 60))
    T = len(series)
    if upto < 1 or vmax <= 0:
        return
    pts = [(x0 + (x1 - x0) * i / (T - 1), y1 - (y1 - y0) * min(series[i] / vmax, 1.0)) for i in range(upto + 1)]
    dr.line(pts, fill=color, width=2)


# ------------------------------------------------------------------ composition
def encode(frames_iter, path, fps=FPS, crf=22):
    import imageio_ffmpeg

    ff = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}",
           "-r", str(fps), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", str(crf), "-preset", "slow",
           "-movflags", "+faststart", str(path)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    last = None
    for fr in frames_iter:
        p.stdin.write(fr.tobytes())
        last = fr
    p.stdin.close()
    p.wait()
    return last


def compose(name, poster_at=0.85, hold=3.0):
    spec = VIDEOS[name]
    fps = spec.get("fps", 10)
    data = [dict(np.load(CACHE / f"{name}_{k}.npz", allow_pickle=False)) for k in range(len(spec["arms"]))]
    n = len(data)
    T = min(len(d["fields"]) for d in data)
    gap = 24
    top = 112
    panel = min(HEIGHT - top - 36 - 22 - 22 * len(spec["caption"]) - 10, (WIDTH - gap * (n + 1)) // n)
    stats = [stat_series(spec, d) for d in data]
    stats2 = [stat_series(spec, d, spec["stat2"]) for d in data] if "stat2" in spec else None
    vmax = max(float(np.nanmax(s[0][:T])) for s in stats) * 1.05 or 1.0
    if spec["stat"] in ("share", "inside"):
        vmax = 1.0

    if "particles" not in spec:
        idx = [[chan(list(d["channels"]), p) for p, _ in spec["show"]] for d in data]
        colors = [c for _, c in spec["show"]]
        scales = []
        for j in range(len(colors)):  # pooled over arms: one colour scale for the whole video
            x = np.concatenate([np.clip(d["fields"][::4, idx[a][j]].astype(np.float32), 0, None).ravel()
                                for a, d in enumerate(data)])
            x = x[np.random.default_rng(0).integers(0, x.size, min(x.size, 3_000_000))]
            lo, hi = np.percentile(x, [1.0, 99.5])
            scales.append((float(lo), float(max(hi, lo + 1e-9))))

    f_title, f_sub, f_lab, f_stat, f_cap, f_small = (font(30, True), font(17), font(18, True), font(17),
                                                      font(17), font(14))
    x_of = [gap + a * (panel + gap) + (WIDTH - n * panel - (n + 1) * gap) // 2 for a in range(n)]

    def frame(f):
        img = Image.new("RGB", (WIDTH, HEIGHT), BG)
        dr = ImageDraw.Draw(img)
        dr.text((32, 18), spec["title"], font=f_title, fill=FG)
        dr.text((32, 58), spec["subtitle"], font=f_sub, fill=DIM)
        t = f * float(data[0]["dt_frame"])
        tt = f"t = {t:,.0f}"
        dr.text((WIDTH - 32 - dr.textlength(tt, font=f_lab), 22), tt, font=f_lab, fill=ACCENT)
        for a, d in enumerate(data):
            x = x_of[a]
            dr.text((x, top - 26), spec["arms"][a][1], font=f_lab, fill=ARM_COLORS[a])
            if "particles" in spec:
                off = np.concatenate([[0], np.cumsum(d["parts_n"])])
                P = d["parts"][off[f]:off[f + 1]]
                rgb = particle_rgb(P, d["fields"].shape[2:], panel, spec["particles"])
                im = Image.fromarray(rgb)
            else:
                rgb = field_rgb(d["fields"][f], idx[a], colors, scales)
                im = Image.fromarray(rgb).resize((panel, panel), Image.BICUBIC)
            img.paste(im, (x, top))
            dr.rectangle([x - 1, top - 1, x + panel, top + panel], outline=ARM_COLORS[a])
            series, fmt = stats[a]
            val = f"{spec['stat_label']}: {fmt.format(series[f])}"
            if stats2:
                val += f"   {spec['stat2_label']}: {stats2[a][1].format(stats2[a][0][f])}"
            dr.text((x, top + panel + 6), val, font=f_stat, fill=FG)
            spark(dr, (x + panel - 170, top + panel + 6, x + panel, top + panel + 26), series[:T], f, ARM_COLORS[a],
                  fmt, vmax)
        y = top + panel + 36
        dr.text((32, y), spec["legend"], font=f_small, fill=DIM)
        y += 22
        for line in spec["caption"]:
            dr.text((32, y), line, font=f_cap, fill=FG)
            y += 22
        return np.asarray(img)

    if top + panel + 36 + 22 + 22 * len(spec["caption"]) > HEIGHT:
        raise SystemExit(f"{name}: layout overflows {HEIGHT}px")

    def frames():
        for f in range(T):
            yield frame(f)
        last = frame(T - 1)
        for _ in range(int(hold * fps)):
            yield last

    OUT.mkdir(exist_ok=True)
    encode(frames(), OUT / f"{name}.mp4", fps=fps)
    Image.fromarray(frame(int(poster_at * (T - 1)))).save(OUT / f"{name}.jpg", quality=88)
    print(f"wrote {OUT / name}.mp4 ({T} frames)")


# ------------------------------------------------------------------ highlight reel
REEL = [
    ("autopoiesis", "Autopoiesis: cells with their own membrane", "membrane_evo_up, seed 4, t = 0-40000", "L7[L3] low",
     "Smoothed noise condenses into walled protocells (the green rim is where links collect) that divide into blue K1 "
     "cells. From t = 8000 random whole-cell flips turn single cells orange (K2, 1.3x link yield). Orange cells are "
     "larger, survive the random disk deaths (black holes that refill) and take over.",
     "Against an identical-event twin, K2 share ends 0.85-0.97 in 8/10 seeds vs 0-0.46. The sweep runs mostly "
     "through fragments cut by the disk deaths, so it is disturbance-mediated. Best organized cell: phase_membrane "
     "L6[L3] medium."),
    ("active-droplets", "Active droplets: emulsions with a self-made shell", "ad7-gated family, seed 1", "L6[L3] medium",
     "Droplets build an amphiphile shell psi that gates fuel weakly and catalyst strongly. Alleles differ only in "
     "shell output kp: red kp = 4 with thick rims, green and yellow with thin rims dividing by dumbbell, blue kp = 0 "
     "blobs with no rim that leak.",
     "A permeability/retention trade-off with an interior optimum, reproduced under harmonic face means on 3 seeds. "
     "The earlier ad1-fuel division is Gray-Scott mitosis in a Cahn-Hilliard body: a Laplacian-only twin also divides."),
    ("chemotaxis-motility", "Chemotaxis: swimmers, prey and predators", "evopursuit, seed 0, t = 0-1500", "L5[L2]+L4b high",
     "A noisy soup condenses into crescent swimmers. Predators (magenta) chase prey and ride in their concave rears; "
     "dark green wakes are eaten food. Ancestral A prey (cyan) are eaten down while B prey with an evasion allele "
     "(orange) appear by rare mutation, divide and spread: 45 B and no A by t = 1460.",
     "Matched arms: the predator's net effect is positive on B (2.4-3.5x prey alone) and lethal on A (0.15-0.36x). B "
     "wins mainly by retention under consumption. A-to-B conversions (28) rival clean B fissions (23), so L6 and L7 "
     "stay Weak."),
    ("fisim-beyond-laplacian", "PhySim genome, extended beyond the Laplacian", "xcell-her, seed 0, t = 0-400", "L3 high",
     "Extended blobkit genome: body u (cyan), Cahn-Hilliard membrane m (orange), heritable marker h (magenta). Ten "
     "planted cells, half carrying h, grow, elongate and pinch in two; each daughter re-forms a complete membrane. "
     "White cells are h-on, cyan-centred cells h-off.",
     "The two planted kinds breed true (46 divisions, 0 mixed); removing the membrane gate on h erases every "
     "on-lineage. Heredity is regime-conditional and L7 was Contradicted. Lasting output: XGENOME_SPEC.md, the "
     "operators for PhySim."),
    ("flow-lenia", "Flow-Lenia: mass-conserving predators and prey", "fl_predator", "L4b[L2] medium",
     "Cyan prey gliders, orange predators that convert overlapped prey mass, magenta food. Reintegration tracking "
     "conserves mass exactly.",
     "Engulfment repeats, but chase and flee are imposed sensing and coexistence holds at 1 of 9 parameter points: "
     "L5 Weak. The thread's best world is fl_forager, L6[L2]+L4b medium (reticulate lineages)."),
    ("lenia-multichannel", "Multichannel Lenia: replicators that eat", "mcfd-MIRd, seed 2, t = 0-1400", "L6[L2]+L4c+L5 medium",
     "One planted MIRd+ cell (Chan's replicator: white core, orange cap, dotted magenta halo) divides into a colony "
     "that eats the food (green; black = eaten). The food crashes, most cells starve, and survivors divide again "
     "into the regrown food.",
     "Binary fissions after each trough, with daughters re-forming core and cap. The boom-bust is intermittent, not "
     "a cycle (damped at 192\u00b2). Sibling mcf-MIRd: L6[L2]+L4c high. Replication itself is Chan's result."),
    ("particle-life", "Particle life: membrane cells that shed spores", "sporecell2-gate, seed 1, dt = 0.02", "L2 medium",
     "Ringed cells (cyan and pink cores, orange membrane) grow on a food gas, then burst into clouds of spores that "
     "found bare daughters. The thread's most life-like image.",
     "The judges showed the burst is integrator overshoot: with step-safe motion and no explicit release rule, free "
     "spores fall 127 -> 3.4 and there is 1 birth against 22 deaths. Reproduction belonged to the discrete map."),
]


def card(lines):
    """A title card: the first line is the heading; the block is centred vertically."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    dr = ImageDraw.Draw(img)
    blocks = []
    for i, (txt, size, col) in enumerate(lines):
        f = font(size, bold=i == 0)
        blocks.append((wrap_text(dr, txt, f, WIDTH - 240), f, size, col))
    y = (HEIGHT - sum(len(b[0]) * int(b[2] * 1.35) + 22 for b in blocks)) // 2
    for k, (lns, f, size, col) in enumerate(blocks):
        for ln in lns:
            dr.text((120, y), ln, font=f, fill=col)
            y += int(size * 1.35)
        y += 22 + (12 if k == 0 else 0)
    return img


def reel():
    import imageio.v2 as imageio

    def read(path):
        r = imageio.get_reader(str(path))
        fps = r.get_meta_data()["fps"]
        fr = [np.asarray(x)[..., :3] for x in r]
        r.close()
        return fr, fps

    def segment_frames(thread, head, world, rung, seeing, verdict):
        src, fps = read(LAB / "threads" / thread / "movies" / "showcase.mp4")
        box = 680
        h, w = src[0].shape[:2]
        s = box / max(h, w)
        size = (int(w * s) // 2 * 2, int(h * s) // 2 * 2)
        panel = Image.new("RGB", (WIDTH, HEIGHT), BG)
        dr = ImageDraw.Draw(panel)
        px = 20 + box + 28
        tw = WIDTH - px - 32
        y = 40
        dr.text((px, y), thread, font=font(15), fill=DIM)
        y += 26
        for ln in wrap_text(dr, head, font(25, True), tw):
            dr.text((px, y), ln, font=font(25, True), fill=FG)
            y += 32
        y += 8
        dr.text((px, y), world, font=font(17), fill=DIM)
        y += 30
        fb = font(22, True)
        bw = dr.textlength(rung, font=fb) + 24
        dr.rounded_rectangle([px, y, px + bw, y + 36], radius=8, fill=(60, 48, 20), outline=ACCENT)
        dr.text((px + 12, y + 5), rung, font=fb, fill=ACCENT)
        y += 54
        for title, body in (("What you are seeing", seeing), ("Committee verdict", verdict)):
            dr.text((px, y), title.upper(), font=font(13, True), fill=ACCENT)
            y += 22
            for ln in wrap_text(dr, body, font(16), tw):
                dr.text((px, y), ln, font=font(16), fill=FG)
                y += 23
            y += 16
        # resample the showcase to the reel's frame rate
        n_out = int(round(len(src) / fps * FPS))
        for i in range(n_out):
            fr = src[min(len(src) - 1, int(i * fps / FPS))]
            img = panel.copy()
            img.paste(Image.fromarray(fr).resize(size, Image.BICUBIC), (20 + (box - size[0]) // 2, (HEIGHT - size[1]) // 2))
            yield np.asarray(img)

    title = card([("The ALife agent lab: seven threads, three sprints", 48, FG),
                  ("Seven researcher agents explored worlds beyond reaction-diffusion (Lenia, Flow-Lenia, particle life, "
                   "active emulsions, chemotaxis, autopoiesis, an extended PhySim genome). A committee of judge agents "
                   "reviewed every sprint against a rubric ladder L0-L8 and funded the next one.", 24, DIM),
                  ("Each clip is a thread's showcase world, with the committee's final consensus rung.", 24, ACCENT)])
    end = card([("Where the lab got to", 48, FG),
                ("Highest rungs: two L7 heredity-and-selection results, both low confidence (autopoiesis membrane_evo, "
                 "active-droplets ad5-evolve). No thread reached open-endedness (L8).", 24, FG),
                ("What transferred: gated mobility at boundaries, Allen-Cahn walls held up by the cell's own product, "
                 "self-repellent trails for propulsion, food that is consumed and regrows, exact mass ledgers.", 24, FG),
                ("What the judges caught: integrator overshoot, contagion counted as selection, unmatched controls, a "
                 "Cahn-Hilliard body replaceable by plain diffusion. Full record: research/alife/REPORT.md", 24, DIM)])

    def all_frames():
        for _ in range(int(6 * FPS)):
            yield np.asarray(title)
        for seg in REEL:
            yield from segment_frames(*seg)
        for _ in range(int(9 * FPS)):
            yield np.asarray(end)

    OUT.mkdir(exist_ok=True)
    encode(all_frames(), OUT / "lab_reel.mp4", crf=27)
    Image.fromarray(next(segment_frames(*REEL[0]))).save(OUT / "lab_reel.jpg", quality=88)
    print(f"wrote {OUT / 'lab_reel.mp4'}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "sim":
        sim(sys.argv[2], int(sys.argv[3]))
    elif cmd == "compose":
        compose(sys.argv[2])
    elif cmd == "reel":
        reel()
    else:
        for k, v in VIDEOS.items():
            print(f"{k}: {len(v['arms'])} arms, {v['frames']} frames")
