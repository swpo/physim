"""Run a world and write a standard evidence pack.

    python -m labkit.run path/to/world.py --out path/to/pack --seeds 0 1 2 [--frames 200]
           [--spf N] [--size H W] [--damage FRAME:FRAC] [--no-movie] [--threshold T]

Per seed, the pack contains:
    FACTS.md        judge-facing summary of every measurement, with warnings
    metrics.json    the same numbers, machine readable
    sheet.png       24 frames over the whole run, fixed colour scales, sim times
    tracks.png      biography strips of the most persistent individuals (fixed crops)
    lineage.png     track lifetimes with split/merge links (replication evidence)
    timeseries.png  components, enclosures, channel totals, occupancy, events
    movie.mp4       up to 120 recorded frames (small; commit only for promising worlds)
    particles.png   (particle worlds) the same 24 times drawn as particles
    frames.npz      raw recorded fields (git-ignored; regenerate from world + seed)
With several seeds, SUMMARY.md tabulates them.
"""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

import numpy as np

from . import metrics as M
from . import render as R
from .world import load_world

THRESHOLDS = (0.2, 0.35, 0.5)  # relative to the robust matter range; 0.35 is primary


def _matter(W, F):
    if hasattr(W, "matter"):
        return np.asarray(W.matter(F), np.float32)
    idx = W.META["matter"]
    return (F if idx is None else F[list(idx)]).sum(0)


def _largest_component(m):
    lo, hi = np.percentile(m, [1, 99.9])
    seg = M.segment((m - lo) / max(hi - lo, 1e-12), 0.35)
    if seg["n"] == 0:
        return None
    k = int(np.argmax(seg["area"]))
    return seg["lab"] == k + 1, seg["cy"][k], seg["cx"][k], seg["area"][k]


def simulate(W, seed, frames, spf, size, render_max=120, damage=None, log=print):
    """Advance the world, keeping every matter field and up to render_max full frames."""
    state = W.init(seed, size)
    render_idx = set(np.unique(np.linspace(0, frames, min(render_max, frames + 1)).round().astype(int)).tolist())
    rec = {"matter": [], "render": [], "render_f": [], "particles": [], "totals": [], "status": "ok",
           "damage": None}
    t0 = time.time()
    for f in range(frames + 1):
        if f > 0:
            for _ in range(spf):
                state = W.step(state)
        if damage and f == damage[0] and hasattr(W, "damage"):
            F = np.asarray(W.fields(state), np.float32)
            F = F[None] if F.ndim == 2 else F
            comp = _largest_component(_matter(W, F))
            if comp is not None:
                mask, cy, cx, area = comp
                from .ops import disk
                rad = np.sqrt(damage[1] * area / np.pi)
                hole = disk(*mask.shape, cy, cx, rad) & mask
                state = W.damage(state, hole)
                rec["damage"] = {"frame": f, "cy": float(cy), "cx": float(cx), "radius": float(rad),
                                 "erased_px": int(hole.sum()), "component_area": float(area)}
        F = np.asarray(W.fields(state), np.float32)
        F = F[None] if F.ndim == 2 else F
        if not np.isfinite(F).all():
            rec["status"] = f"non-finite fields at frame {f}"
            log(rec["status"])
            break
        rec["matter"].append(_matter(W, F))
        rec["totals"].append(F.reshape(F.shape[0], -1).sum(1))
        if hasattr(W, "particles"):
            rec["particles"].append(np.array(W.particles(state), np.float32))
        if f in render_idx:
            rec["render"].append(F.astype(np.float16))
            rec["render_f"].append(f)
        if f and f % max(1, frames // 10) == 0:
            log(f"  frame {f}/{frames}  {time.time() - t0:.1f}s")
    rec["wall"] = time.time() - t0
    return rec


def analyze(W, rec, spf, periodic=True, threshold=None, min_area=None):
    meta = W.META
    dt_frame = spf * float(meta["dt"])
    mat = np.stack(rec["matter"])
    T = len(mat)
    lo = float(np.percentile(mat[:: max(1, T // 40)], 1))
    hi = float(np.percentile(mat[:: max(1, T // 40)], 99.9))
    span = max(hi - lo, 1e-12)
    mn = (mat - lo) / span
    sm = float(meta.get("smooth", 1.0))  # light blur so thin filaments do not flicker as debris
    if sm > 0:
        from scipy import ndimage
        mn = np.stack([ndimage.gaussian_filter(x, sm, mode="wrap" if periodic else "nearest") for x in mn])
    thr = THRESHOLDS[1] if threshold is None else (threshold - lo) / span
    H, Wd = mn.shape[1:]
    min_area = min_area or max(6, int(H * Wd / 20000))
    comps, links, labs = [], [None], []
    n_comp, n_encl, holes_tot, occ = [], [], {t: [] for t in THRESHOLDS}, []
    prev = None
    for f in range(T):
        seg = M.segment(mn[f], thr, min_area, periodic)
        comps.append(seg)
        nh, _ = M.holes(seg["lab"], seg["n"], periodic=periodic)
        seg["holes"] = nh
        n_comp.append(seg["n"])
        n_encl.append(int((nh > 0).sum()))
        occ.append(float((seg["lab"] > 0).mean()))
        if prev is not None:
            links.append(M.overlaps(prev["lab"], prev["n"], seg["lab"], seg["n"]))
        prev = seg
    for t in THRESHOLDS:
        for f in np.linspace(0, T - 1, min(T, 24)).round().astype(int):
            s = M.segment(mn[f], t, min_area, periodic)
            holes_tot[t].append(int(M.holes(s["lab"], s["n"], periodic=periodic)[0].sum()))
    tracks, events = M.track(comps, links, (H, Wd), periodic)
    lin = M.lineage_stats(tracks, events, T, dt_frame, (H, Wd), periodic)

    # topology of the matter field and of each channel
    tda_frames = np.unique(np.linspace(0, T - 1, min(T, 12)).round().astype(int))
    tda = {int(f): M.persistence_counts(mn[f], periodic=periodic) for f in tda_frames}
    render = np.stack([r.astype(np.float32) for r in rec["render"]])
    scales = R.channel_scales(render)
    ch_tda = {}
    for k in np.unique(np.linspace(0, len(render) - 1, min(len(render), 6)).round().astype(int)):
        ch_tda[int(rec["render_f"][k])] = [M.persistence_counts(R.normalize(render[k], scales)[c], periodic=periodic)
                                           for c in range(render.shape[1])]

    # inside / boundary / outside organization of the most persistent tracks
    life = lin["lifetimes"]
    order = sorted(range(len(tracks)), key=lambda i: (-life[i], -(tracks[i]["end"] == T - 1)))
    top = order[:3]
    gen = lin["generation"]
    deep = sorted(range(len(tracks)), key=lambda i: (-gen[i], -life[i]))
    if deep and gen[deep[0]] > 0 and deep[0] not in top:
        top.append(deep[0])  # also show the most-derived lineage member
    else:
        top = order[:4]
    rf = rec["render_f"]
    struct = []
    for i in top:
        t = tracks[i]
        cand = [k for k, f in enumerate(rf) if t["start"] <= f <= t["end"]]
        if not cand:
            continue
        k = cand[len(cand) // 2]
        f = rf[k]
        seg = M.segment(mn[f], thr, min_area, periodic)
        j = int(np.argmin([np.hypot(M._wrap(seg["cy"][q] - t["cy"][f - t["start"]], H),
                                    M._wrap(seg["cx"][q] - t["cx"][f - t["start"]], Wd)) for q in range(seg["n"])])) if seg["n"] else None
        if j is None:
            continue
        s = M.structure(R.normalize(render[k], scales), seg["lab"] == j + 1)
        if s:
            struct.append({"track": i, "frame": int(f), "holes": int(seg_holes(seg, j, periodic)), **s})

    totals = np.stack(rec["totals"])
    ok_tot = np.abs(totals[0]) > 1e-9
    drift = np.where(ok_tot, (totals[-1] - totals[0]) / np.where(ok_tot, np.abs(totals[0]), 1), np.nan)
    persistent = [i for i in range(len(tracks)) if life[i] >= 0.5 * T]
    moving = [m for m in lin["motion"] if m["body_lengths"] >= 1.0 and life[m["id"]] >= lin["K_frames"]]
    persist_area = [(min(tracks[i]["area"]), max(tracks[i]["area"])) for i in persistent]
    summary = {
        "frames": T, "time": (T - 1) * dt_frame, "grid": [int(H), int(Wd)],
        "threshold_rel": float(thr), "matter_range": [lo, hi], "min_area": int(min_area),
        "components_final": int(n_comp[-1]), "components_mean": float(np.mean(n_comp)),
        "components_max": int(np.max(n_comp)),
        "occupancy_final": occ[-1], "occupancy_max": float(np.max(occ)),
        "tracks": len(tracks), "persistent_tracks": len(persistent),
        "longest_track_frames": int(life.max()) if len(life) else 0,
        "alive_at_end_from_start": int(sum(1 for t in tracks if t["start"] == 0 and t["end"] == T - 1)),
        "persistent_area_ratio_max": float(max((b / max(a, 1) for a, b in persist_area), default=0)),
        "enclosed_components_mean": float(np.mean(n_encl)), "enclosed_components_final": int(n_encl[-1]),
        "holes_final_by_threshold": {str(t): holes_tot[t][-1] for t in THRESHOLDS},
        "holes_mean_by_threshold": {str(t): float(np.mean(holes_tot[t])) for t in THRESHOLDS},
        "splits": sum(e["type"] == "split" for e in events),
        "persistent_splits": len(lin["persistent_splits"]),
        "max_generation": int(lin["max_generation"]),
        "merges": sum(e["type"] == "merge" for e in events),
        "nucleations": sum(t["birth"] == "nucleation" for t in tracks),
        "moving_tracks": len(moving),
        "max_speed": float(max((m["speed"] for m in moving), default=0.0)),
        "max_body_lengths": float(max((m["body_lengths"] for m in lin["motion"]), default=0.0)),
        "channel_total_drift": [None if np.isnan(d) else round(float(d), 4) for d in drift],
        "tda_matter_final": tda[int(tda_frames[-1])],
    }
    return {
        "summary": summary, "series": {"n_comp": n_comp, "n_enclosed": n_encl, "occupancy": occ,
                                       "totals": totals.tolist()},
        "tracks": tracks, "events": events, "lineage": lin, "tda": tda, "channel_tda": ch_tda,
        "structure": struct, "scales": scales, "top": top, "mn": mn, "comps": comps, "render": render,
    }


def seg_holes(seg, j, periodic):
    nh, _ = M.holes(seg["lab"], seg["n"], periodic=periodic)
    return nh[j] if j < len(nh) else 0


# ------------------------------------------------------------------ figures
def figures(W, rec, A, out, spf, movie=True):
    meta = W.META
    dt_frame = spf * float(meta["dt"])
    render, scales, rf = A["render"], A["scales"], rec["render_f"]
    rgb = [R.composite(R.normalize(fr, scales)) for fr in render]
    pick = np.unique(np.linspace(0, len(rgb) - 1, min(24, len(rgb))).round().astype(int))
    chans = meta["channels"] or [f"c{i}" for i in range(render.shape[1])]
    legend = "  ".join(f"{n}" for n in chans)
    title = f"{meta['name']}  |  channels: {legend}  |  fixed colour scales"
    R.contact_sheet([rgb[k] for k in pick], [f"t={rf[k] * dt_frame:g}" for k in pick], ncols=6,
                    title=title, tile=256).save(out / "sheet.png")

    if rec["particles"]:
        P = rec["particles"]
        dom = meta.get("domain")
        if dom:
            view = (0, 0, dom[0], dom[1])
        else:
            allp = np.concatenate([p[:, :2] for p in P[:: max(1, len(P) // 20)]])
            lo, hi = np.percentile(allp, 1, 0), np.percentile(allp, 99, 0)
            c, half = (lo + hi) / 2, max(hi - lo) / 2 * 1.15 + 1
            view = (c[0] - half, c[1] - half, c[0] + half, c[1] + half)
        idx = np.unique(np.linspace(0, len(P) - 1, 24).round().astype(int))
        ims = [R.particle_canvas(P[k][:, :2], P[k][:, 2] if P[k].shape[1] > 2 else None, view, 256,
                                 radius=max(1.0, 256 / (view[2] - view[0]) * 0.4)) for k in idx]
        R.contact_sheet(ims, [f"t={k * dt_frame:g}" for k in idx], ncols=6,
                        title=f"{meta['name']} particles  |  view {tuple(round(float(v), 1) for v in view)}").save(out / "particles.png")

    # biographies of the top tracks
    tracks, top = A["tracks"], A["top"]
    rows, labels = [], []
    H, Wd = render.shape[2:]
    for i in top:
        t = tracks[i]
        cand = [k for k, f in enumerate(rf) if t["start"] <= f <= t["end"]]
        if not cand:
            continue
        sel = [cand[int(j)] for j in np.unique(np.linspace(0, len(cand) - 1, min(8, len(cand))).round().astype(int))]
        half = int(np.clip(1.6 * np.sqrt(max(t["area"]) / np.pi) + 6, 12, min(H, Wd) // 2))
        for k in sel:
            f = rf[k]
            crop = R.crop_periodic(rgb[k], t["cy"][f - t["start"]], t["cx"][f - t["start"]], half)
            rows.append(np.asarray(R.Image.fromarray(crop).resize((112, 112), R.Image.NEAREST)))
            labels.append(f"#{i} t={f * dt_frame:g}")
        while len(rows) % 8:
            rows.append(np.zeros((112, 112, 3), np.uint8))
            labels.append("")
    if rows:
        R.contact_sheet(rows, labels, ncols=8, title="most persistent individuals (fixed crops follow the tracked centroid)").save(out / "tracks.png")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    s = A["series"]
    tt = np.arange(len(s["n_comp"])) * dt_frame
    fig, ax = plt.subplots(2, 2, figsize=(11, 6.5))
    ax[0, 0].plot(tt, s["n_comp"], label="components")
    ax[0, 0].plot(tt, s["n_enclosed"], label="components with a hole")
    ax[0, 0].legend(); ax[0, 0].set_title("individuals")
    tot = np.array(s["totals"])
    for c in range(tot.shape[1]):
        base = np.abs(tot[0, c]) if abs(tot[0, c]) > 1e-9 else 1.0
        ax[0, 1].plot(tt, tot[:, c] / base, label=(meta["channels"] or [f"c{c}" for c in range(tot.shape[1])])[c])
    ax[0, 1].set_title("channel totals / initial"); ax[0, 1].legend(fontsize=7)
    ax[1, 0].plot(tt, s["occupancy"]); ax[1, 0].set_title("occupied fraction (matter > threshold)")
    for e in A["events"]:
        ax[1, 1].axvline(e["frame"] * dt_frame, color="tab:green" if e["type"] == "split" else "tab:red", alpha=0.35)
    for e in A["lineage"]["persistent_splits"]:
        ax[1, 1].axvline(e["frame"] * dt_frame, color="k", lw=2)
    ax[1, 1].set_title("events: split (green), merge (red), persistent split (black)")
    for a in ax.flat:
        a.set_xlabel("time")
    fig.tight_layout(); fig.savefig(out / "timeseries.png", dpi=80); plt.close(fig)

    # lineage chart
    life = A["lineage"]["lifetimes"]
    K = A["lineage"]["K_frames"]
    keep = [t for t in tracks if life[t["id"]] >= K or t["children"] or t["birth"] == "split"]
    keep = sorted(keep, key=lambda t: -life[t["id"]])[:150]
    keep_ids = {t["id"] for t in keep}
    ypos = {t["id"]: k for k, t in enumerate(sorted(keep, key=lambda t: (t["start"], t["id"])))}
    fig, ax = plt.subplots(figsize=(11, max(3, min(12, 0.08 * len(keep) + 2))))
    gen = A["lineage"]["generation"]
    cmap = plt.get_cmap("viridis")
    gmax = max(1, max(gen.values(), default=1))
    for t in keep:
        y = ypos[t["id"]]
        ax.plot([t["start"] * dt_frame, t["end"] * dt_frame], [y, y], color=cmap(gen[t["id"]] / gmax), lw=2)
        for p in t["parents"]:
            if p in keep_ids:
                ax.plot([t["start"] * dt_frame] * 2, [ypos[p], y], color="0.6", lw=0.8)
    ax.set_xlabel("time"); ax.set_ylabel("track")
    ax.set_title(f"lineage: colour = generation (max {A['summary']['max_generation']}), "
                 f"{A['summary']['persistent_splits']} persistent splits, {len(keep)} tracks shown")
    fig.tight_layout(); fig.savefig(out / "lineage.png", dpi=80); plt.close(fig)

    if movie:
        R.save_movie(rgb, str(out / "movie.mp4"), fps=15)


def facts(W, rec, A, out, seed, spf, args_line):
    meta, s = W.META, A["summary"]
    warn = []
    if rec["status"] != "ok":
        warn.append(f"RUN FAILED: {rec['status']} (only {s['frames']} frames analysed)")
    if s["occupancy_max"] > 0.8:
        warn.append("matter fills >80% of the domain at some point: components may be one connected sea")
    if s["components_final"] == 0:
        warn.append("no components at the end: matter died out or fell below threshold")
    drift = [d for d in s["channel_total_drift"] if d is not None]
    if drift and max(abs(d) for d in drift) > 0.5:
        warn.append("a channel total changed by more than 50% (not conserved; may be fine if the model is open)")
    if s["frames"] < 30:
        warn.append("fewer than 30 recorded frames: tracking statistics are weak")
    lines = [
        f"# Evidence pack: {meta['name']} (seed {seed})",
        "",
        f"- world: `{os.path.relpath(meta['path'], out)}`, family `{meta['family']}`",
        f"- parent: {meta['parent']}; mutation: {meta['mutation'] or '-'}",
        f"- run: {s['frames']} frames x {spf} steps x dt {meta['dt']} = time {s['time']:g}; grid {s['grid']}; "
        f"wall {rec['wall']:.0f}s; status {rec['status']}",
        f"- command: `{args_line}`",
        f"- segmentation: matter > {s['threshold_rel']:.2f} of robust range {[round(v, 4) for v in s['matter_range']]}, "
        f"min area {s['min_area']} px",
        "",
        "## Measurements",
        f"- components: final {s['components_final']}, mean {s['components_mean']:.1f}, max {s['components_max']}; "
        f"occupancy final {s['occupancy_final']:.2f}",
        f"- tracks: {s['tracks']}; persistent (alive >= 50% of run): {s['persistent_tracks']}; "
        f"longest {s['longest_track_frames']} frames; alive start-to-end: {s['alive_at_end_from_start']}",
        f"- size of persistent tracks: max/min area ratio {s['persistent_area_ratio_max']:.2f} (1 = constant size)",
        f"- enclosures: components with a hole mean {s['enclosed_components_mean']:.2f}, final {s['enclosed_components_final']}; "
        f"holes at thresholds 0.2/0.35/0.5 final {list(s['holes_final_by_threshold'].values())}",
        f"- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 {s['tda_matter_final']['H0']}, "
        f"H1 {s['tda_matter_final']['H1']}",
        f"- motion: {s['moving_tracks']} long-lived tracks moved >= 1 body length; max speed {s['max_speed']:.3g}/time; "
        f"max body lengths {s['max_body_lengths']:.1f}",
        f"- replication: splits {s['splits']}, persistent splits {s['persistent_splits']}, "
        f"max generation {s['max_generation']}, merges {s['merges']}, nucleations {s['nucleations']}",
        f"- channel total drift (end/start - 1): {s['channel_total_drift']}",
    ]
    if A["structure"]:
        lines.append("- internal organization of top tracks (normalized channel means; rim = outer layer):")
        for st in A["structure"]:
            lines.append(f"  - track {st['track']} at frame {st['frame']}: holes {st['holes']}, "
                         f"rim-vs-core {st['rim_vs_core']:.2f}, rim-vs-outside {st['rim_vs_outside']:.2f}, "
                         f"heterogeneity {st['heterogeneity']:.2f}; core {st['core_mean']} rim {st['rim_mean']}")
    if rec["damage"]:
        d = rec["damage"]
        lines.append(f"- damage applied at frame {d['frame']}: erased {d['erased_px']} px of a {d['component_area']:.0f} px component")
    lines += ["", "## Warnings"] + ([f"- {w}" for w in warn] or ["- none"])
    lines += ["", "## Files", "sheet.png, tracks.png, lineage.png, timeseries.png"
              + (", particles.png" if rec["particles"] else "") + ", movie.mp4, metrics.json",
              "", "Measurements are screens, not verdicts: judge them against the images."]
    (out / "FACTS.md").write_text("\n".join(lines) + "\n")
    return warn


def run_pack(world_path, out, seed=0, frames=200, spf=None, size=None, damage=None, movie=True,
             threshold=None, min_area=None, save_frames=True, quiet=False, args_line=""):
    log = (lambda *a: None) if quiet else print
    W = load_world(world_path)
    spf = int(spf or W.META["steps_per_frame"])
    size = tuple(size or W.META["size"])
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    log(f"[{W.META['name']}] seed {seed}: {frames} frames x {spf} steps, grid {size}")
    rec = simulate(W, seed, frames, spf, size, damage=damage, log=log)
    if len(rec["matter"]) < 2:
        (out / "FACTS.md").write_text(f"# {W.META['name']} seed {seed}\n\nRUN FAILED: {rec['status']}\n")
        return {"seed": seed, "status": rec["status"]}
    periodic = W.META.get("periodic", True)
    if threshold is None:
        threshold = W.META.get("threshold")  # META documents an absolute threshold; honour it
    A = analyze(W, rec, spf, periodic, threshold, min_area)
    figures(W, rec, A, out, spf, movie)
    warn = facts(W, rec, A, out, seed, spf, args_line)
    lin = A["lineage"]
    top_tracks = [{k: (v if k not in ("area", "cy", "cx") else [round(float(x), 2) for x in v[:: max(1, len(v) // 50)]])
                   for k, v in A["tracks"][i].items()} for i in A["top"]]
    doc = {
        "world": {k: (list(v) if isinstance(v, tuple) else v) for k, v in W.META.items()},
        "seed": seed, "steps_per_frame": spf, "status": rec["status"], "wall_seconds": rec["wall"],
        "damage": rec["damage"], "summary": A["summary"], "warnings": warn,
        "structure": A["structure"], "top_tracks": top_tracks,
        "persistent_splits": lin["persistent_splits"][:50],
        "motion_top": sorted(lin["motion"], key=lambda m: -m["body_lengths"])[:10],
        "tda_matter": A["tda"], "tda_channels": A["channel_tda"], "series": A["series"],
    }
    (out / "metrics.json").write_text(json.dumps(doc, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)))
    if save_frames:
        np.savez_compressed(out / "frames.npz", render=A["render"].astype(np.float16), render_f=np.array(rec["render_f"]),
                            matter=np.stack(rec["matter"]).astype(np.float16))
    log(f"  -> {out}/FACTS.md  ({rec['wall']:.0f}s sim)")
    return {"seed": seed, "status": rec["status"], **A["summary"]}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("world")
    ap.add_argument("--out", required=True)
    ap.add_argument("--seeds", type=int, nargs="+", default=[0])
    ap.add_argument("--frames", type=int, default=200)
    ap.add_argument("--spf", type=int, default=None)
    ap.add_argument("--size", type=int, nargs=2, default=None)
    ap.add_argument("--damage", default=None, help="FRAME:FRACTION erase a central disk of the largest component")
    ap.add_argument("--threshold", type=float, default=None, help="absolute matter threshold")
    ap.add_argument("--min-area", type=int, default=None)
    ap.add_argument("--no-movie", action="store_true")
    a = ap.parse_args(argv)
    import sys
    args_line = "python -m labkit.run " + " ".join(sys.argv[1:] if argv is None else argv)
    dmg = tuple(float(x) for x in a.damage.split(":")) if a.damage else None
    dmg = (int(dmg[0]), dmg[1]) if dmg else None
    rows = []
    for s in a.seeds:
        out = Path(a.out) / (f"seed{s}" if len(a.seeds) > 1 else "")
        rows.append(run_pack(a.world, out, s, a.frames, a.spf, a.size, dmg, not a.no_movie, a.threshold,
                             a.min_area, args_line=args_line))
    if len(a.seeds) > 1:
        keys = ["status", "components_final", "persistent_tracks", "longest_track_frames", "enclosed_components_final",
                "moving_tracks", "persistent_splits", "max_generation", "occupancy_final"]
        lines = ["| seed | " + " | ".join(keys) + " |", "|" + "---|" * (len(keys) + 1)]
        for r in rows:
            lines.append(f"| {r['seed']} | " + " | ".join(str(round(r[k], 2) if isinstance(r.get(k), float) else r.get(k, "-")) for k in keys) + " |")
        (Path(a.out) / "SUMMARY.md").write_text(f"# {a.world} across seeds\n\n" + "\n".join(lines) + "\n")
        print("\n".join(lines))


if __name__ == "__main__":
    main()
