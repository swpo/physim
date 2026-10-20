"""Render the 20 October 2026 research update from immutable saved evidence.

This is a presentation-only tool. It imports no simulator, advances no state,
fits no model, and does not recompute scientific outcomes. Captions and numerical
readouts come from the saved summaries. Pixel transforms are display operations.
Requires NumPy, Pillow, FFmpeg and ffprobe.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from PIL import __version__ as PIL_VERSION

ROOT = Path(__file__).resolve().parents[1]
EPOCHS = "handoff/swarm_continuous_20261017/epochs/"
SOURCES = {
    "x1-fields.npz": (
        "0006/results/p07-exterior-x1-restoration-v1/evidence.npz",
        "32855845491af10adaf70f43322ca6717e13b7ca22524dcbc22bd34a44fd9853",
    ),
    "x1-observations.json": (
        "0006/results/p07-exterior-x1-restoration-v1/observations.json",
        "c09b0c1a64b774b02a7c43125c35532bdc2b941da5bff7285ec4e1b3f6dfb3f2",
    ),
    "x1-summary.json": (
        "0006/results/p07-exterior-x1-restoration-v1/summary.json",
        "bc858fb867e8b5ea523adca1040bf6b0221c20ad700adf8107cbdb0561fded41",
    ),
    "protection-masks.npz": (
        "0005/results/l144-protection-action-necessity-v1/core_masks.npz",
        "25ba365bb1de25baebd448dad2374e336e4a631c70bb4e5213b7f452518d3295",
    ),
    "protection-summary.json": (
        "0005/results/l144-protection-action-necessity-v1/summary.json",
        "60893be7fecd50f976236fec096a724f69386dd618021ab4788f6c7847ce99b2",
    ),
    "protection-audit-summary.json": (
        "0006/results/l144-action-raw-evidence-audit-v1/summary.json",
        "907de2f88ba56c924e01a5b532f210e455bf73451f25b01576945ce83df7cf82",
    ),
}
BG, PANEL = "#0b1421", "#111e2c"
INK, MUTED, TEAL, GOLD = "#ecf3f7", "#b1c2d0", "#68d5bf", "#f2cf83"
FPS = 20
SIZE = (1920, 1080)
PALETTE = ["#081220", "#214863", "#208f9b", "#7ed3bb", "#ffe28e"]
FONT_PATHS = (
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)
BOLD_PATHS = (
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def font_path(given, choices):
    if given:
        return Path(given)
    return next(Path(p) for p in choices if Path(p).exists())


def load_fonts(regular, bold):
    return {
        n: ImageFont.truetype(str(bold if n in (46, 34, 30) else regular), n)
        for n in (20, 22, 24, 26, 28, 30, 32, 34, 46)
    }


def label(draw, xy, text, fonts, size=26, fill=INK):
    draw.text(xy, text, font=fonts[size], fill=fill)


def field_image(values):
    """One fixed, clipped color scale for raw signed A; no per-frame rescaling."""
    f = np.clip((values.astype(np.float64) + 1.5) / 3.0, 0, 1)
    colors = np.array([tuple(bytes.fromhex(c[1:])) for c in PALETTE])
    pixels = np.stack([np.interp(f, np.linspace(0, 1, 5), colors[:, c]) for c in range(3)], axis=-1).astype(np.uint8)
    return Image.fromarray(pixels)


def base(fonts, number, title, subtitle, t, horizon):
    frame = Image.new("RGB", SIZE, BG)
    d = ImageDraw.Draw(frame)
    label(d, (48, 25), f"PHYSIM  /  RESEARCH NOTES  /  20 OCT 2026  /  {number}", fonts, 22, TEAL)
    label(d, (48, 65), title, fonts, 46)
    label(d, (48, 125), subtitle, fonts, 28, MUTED)
    label(d, (1520, 25), f"Saved time  {t:g} / {horizon:g}", fonts, 28)
    d.line((48, 172, 1872, 172), fill="#2d4153", width=2)
    d.rectangle((48, 1050, 1872, 1056), fill="#213449")
    if t:
        d.rectangle((48, 1050, 48 + int(1824 * t / horizon), 1056), fill=TEAL)
    return frame, d


def period_crop(a):
    # Fixed display window centered on the initial target (grid x=40,y=26).
    # Row wrap is periodic. No dynamic recentering or numerical interpolation.
    return a[np.ix_(np.arange(-6, 58) % 128, np.arange(8, 72))]


def geometry_frames(evidence, fonts):
    with np.load(evidence / "x1-fields.npz", allow_pickle=False) as src:
        fields, times = src["A"], src["elapsed"]
        region = np.unpackbits(src["selection_masks"][1], bitorder="big").reshape(128, 128).astype(bool)
    if fields.shape != (4, 29, 128, 128):
        raise ValueError("Unexpected recorded geometry panel")
    summary = json.loads((evidence / "x1-summary.json").read_text())
    observations = json.loads((evidence / "x1-observations.json").read_text())["cases"]
    boundary = region & ~(
        np.roll(region, 1, 0) & np.roll(region, -1, 0) & np.roll(region, 1, 1) & np.roll(region, -1, 1)
    )
    outline = Image.fromarray((period_crop(boundary) * 140).astype(np.uint8)).resize(
        (448, 448), Image.Resampling.NEAREST
    )
    headings = [
        ("W", "Whole surroundings", "Original environment retained"),
        ("I", "Isolated target", "Target + 4-unit neighborhood"),
        ("S", "Restore X1 profile", "Saved exterior profile at t = 0"),
        ("U", "Uniform X1", "Same signed exterior mean at t = 0"),
    ]
    frames = []
    for j, t in enumerate(times):
        im, d = base(
            fonts,
            "01",
            "Restoring initial X1 does not prevent branching",
            "One target, four preparations. Every arm follows the same native equations after t = 0.",
            t,
            100,
        )
        for c, (name, title, detail) in enumerate(headings):
            x = 38 + c * 474
            d.rounded_rectangle((x, 190, x + 452, 838), radius=12, fill=PANEL)
            label(d, (x + 12, 204), f"{name}   {title}", fonts, 30)
            label(d, (x + 12, 250), detail, fonts, 20, MUTED)
            field = field_image(period_crop(fields[c, j])).resize((448, 448), Image.Resampling.NEAREST)
            field.paste(Image.new("RGB", field.size, INK), (0, 0), outline)
            im.paste(field, (x + 2, 288))
            end = summary["cases"][name]["decision"]["identity_end"]
            ended = end is not None and t >= end["time"]
            if not ended:
                if observations[name][j]["target"]["phase"] != "high":
                    raise ValueError("Published phase caption no longer matches saved readout")
                label(d, (x + 12, 753), "Original tracked · Q high", fonts, 26, TEAL)
                label(d, (x + 12, 795), "No split observed yet", fonts, 22, MUTED)
            else:
                label(d, (x + 12, 753), "Original identity ended", fonts, 26, GOLD)
                label(
                    d,
                    (x + 12, 795),
                    f"Sampled threshold split ({end['previous_time']:g}, {end['time']:g}]",
                    fonts,
                    22,
                    MUTED,
                )
        if t < 45:
            caption = "The target and its retained neighborhood start identical in all four preparations."
        elif t < 50:
            caption = "Connected growth beyond the initial neighborhood is not itself a split."
        elif t < 52.5:
            caption = "I has split; S and U are still connected at this recorded time."
        else:
            caption = "S and U also split. Initial X1 restoration was insufficient in this preparation."
        label(d, (48, 860), caption, fonts, 32)
        label(
            d,
            (48, 909),
            "Fixed 32 × 32 spatial-unit crop of a 64 × 64 periodic world. White outline: initial retained neighborhood.",
            fonts,
            24,
            MUTED,
        )
        label(
            d,
            (48, 946),
            "Saved frames held at 5 simulation units per video second; no interpolation. Original phase is undefined after splitting.",
            fonts,
            24,
            MUTED,
        )
        gradient = field_image(np.linspace(-1.5, 1.5, 280)[None, :]).resize((280, 16))
        im.paste(gradient, (48, 1000))
        label(d, (346, 987), "Raw A:  −1.5                         +1.5   (fixed clipped scale)", fonts, 22, MUTED)
        label(d, (1160, 987), "Q status is a saved readout; Q is not the color.", fonts, 22, MUTED)
        frames.append(im)
    return frames, times.tolist()


def protection_frames(evidence, fonts):
    summary = json.loads((evidence / "protection-summary.json").read_text())
    names = ["intact_source", "protection_action_off"]
    with np.load(evidence / "protection-masks.npz", allow_pickle=False) as src:
        masks = [np.unpackbits(src[n + "_packed"][:, 1], axis=-1, bitorder="big") for n in names]
        times = src[names[0] + "_elapsed_times"]
        if not np.array_equal(times, src[names[1] + "_elapsed_times"]):
            raise ValueError("Arm timestamps differ")
    if masks[0].shape != (31, 288, 288) or masks[1].shape != masks[0].shape:
        raise ValueError("Unexpected saved mask geometry")
    frames = []
    for j, t in enumerate(times):
        im, d = base(
            fonts,
            "02",
            "Activity fades when protective action is removed",
            "Matched initial fields and noise state. Only the protective-action coefficient changes; its production law stays.",
            t,
            150,
        )
        for c, name in enumerate(names):
            x = 80 + 960 * c
            label(d, (x, 191), "Intact protection" if c == 0 else "Protective action off", fonts, 34)
            label(d, (x, 237), "Action coefficient = 2" if c == 0 else "Action coefficient = 0", fonts, 24, MUTED)
            rgb = np.where(masks[c][j][..., None], np.array([104, 213, 191]), np.array([17, 30, 44])).astype(np.uint8)
            im.paste(Image.fromarray(rgb).resize((576, 576), Image.Resampling.NEAREST), (x, 282))
            d.rectangle((x, 282, x + 575, 857), outline="#2d4153", width=2)
            row = summary["cases"][name]["observations"][j]
            if row["elapsed_time"] != t:
                raise ValueError("Saved observations no longer align with mask timestamps")
            readout = row["thresholds"][1]
            label(d, (x + 600, 310), "ACTIVE AREA", fonts, 20, MUTED)
            label(d, (x + 600, 343), f"{readout['raw_area']:g}", fonts, 46, TEAL if c == 0 else GOLD)
            label(d, (x + 600, 401), "spatial units²", fonts, 20, MUTED)
            label(d, (x + 600, 470), "ELIGIBLE CORES", fonts, 20, MUTED)
            label(d, (x + 600, 505), str(readout["eligible_count"]), fonts, 46)
            label(d, (x + 600, 565), "area ≥ 2 each", fonts, 20, MUTED)
        if t < 85:
            caption = "The same prepared pattern follows different futures after one action term is disabled."
        else:
            caption = "By sampled t = 85, the action-off arm has no eligible cores at any of the three thresholds."
        label(d, (48, 882), caption, fonts, 30)
        label(
            d,
            (48, 928),
            "Threshold-mask movie: normalized U₀ > 0.45. All above-threshold pixels are shown. Each panel is the full 144 × 144 domain.",
            fonts,
            24,
            MUTED,
        )
        label(
            d,
            (48, 968),
            "Saved every 5 simulation units, held for 1 second. No interpolation. Area and counts are saved summary readouts.",
            fonts,
            24,
            MUTED,
        )
        label(
            d,
            (48, 1007),
            "Intact growth from 88.5 to 599.25 area units does not establish bounded homeostasis or autonomy.",
            fonts,
            24,
            GOLD,
        )
        frames.append(im)
    return frames, times.tolist()


def encode(frames, times, path, poster_time, check_time):
    counts = [int(round((b - a) / 5 * FPS)) for a, b in zip(times, times[1:])] + [2 * FPS]
    if any(n <= 0 for n in counts):
        raise ValueError("Nonpositive frame hold")
    p = subprocess.Popen(
        [
            "ffmpeg",
            "-v",
            "error",
            "-y",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{SIZE[0]}x{SIZE[1]}",
            "-r",
            str(FPS),
            "-i",
            "-",
            "-an",
            "-c:v",
            "libx264",
            "-crf",
            "19",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            "-threads",
            "1",
            str(path),
        ],
        stdin=subprocess.PIPE,
    )
    try:
        for im, count in zip(frames, counts):
            if im.mode != "RGB" or im.size != SIZE:
                raise ValueError("Unexpected frame layout")
            for _ in range(count):
                p.stdin.write(im.tobytes())
    finally:
        p.stdin.close()
        if p.wait():
            raise RuntimeError(f"Encoder failed: {path}")
    total = sum(counts)
    frames[times.index(poster_time)].save(path.with_suffix(".jpg"), quality=95, subsampling=0)
    key = times.index(check_time)
    # Verify the first, turning-point and final frames of the encoded file.
    indices = [0, sum(counts[:key]), total - 1]
    expression = "+".join(f"eq(n\\,{n})" for n in indices)
    raw = subprocess.run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(path),
            "-vf",
            f"select={expression}",
            "-vsync",
            "0",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-",
        ],
        check=True,
        capture_output=True,
    ).stdout
    decoded = np.frombuffer(raw, np.uint8).reshape(3, SIZE[1], SIZE[0], 3)
    errors = [
        float(np.abs(a.astype(np.float64) - np.asarray(b)).mean())
        for a, b in zip(decoded, [frames[0], frames[key], frames[-1]])
    ]
    if max(errors) > 5:
        raise ValueError(f"Decoded frames mismatch: {errors}")
    # The review contact sheet is made from decoded video frames, not source posters.
    sheet = Image.new("RGB", (960, 1620), BG)
    for i, a in enumerate(decoded):
        sheet.paste(Image.fromarray(a).resize((960, 540), Image.Resampling.LANCZOS), (0, 540 * i))
    sheet.save(path.with_name(path.stem + "-encoded-check.jpg"), quality=94)
    probe = json.loads(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "stream=codec_name,width,height,pix_fmt,avg_frame_rate,nb_frames:format=duration",
                "-of",
                "json",
                str(path),
            ]
        )
    )
    if len(probe["streams"]) != 1 or int(probe["streams"][0]["nb_frames"]) != total:
        raise ValueError("Encoded stream/frame count differs")
    return {
        "file": path.name,
        "sha256": sha(path),
        "poster": path.with_suffix(".jpg").name,
        "poster_sha256": sha(path.with_suffix(".jpg")),
        "poster_simulation_time": poster_time,
        "saved_times": times,
        "hold_frames": counts,
        "fps": FPS,
        "last_frame_hold_seconds": 2,
        "simulation_units_per_video_second": 5,
        "interpolation": "none; zero-order frame hold",
        "encoded_checks": {"frame_indices": indices, "mean_absolute_rgb_errors": errors},
        "ffprobe": probe,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assets", type=Path, default=ROOT / "docs/assets/research/2026-10-20")
    parser.add_argument(
        "--capture-from",
        type=Path,
        help="Copy only the exact hash-pinned existing evidence from this checkout; no simulation",
    )
    parser.add_argument("--font")
    parser.add_argument("--font-bold")
    args = parser.parse_args()
    evidence = args.assets / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    sources = {}
    for name, (original, digest) in SOURCES.items():
        target = evidence / name
        if args.capture_from:
            original_path = args.capture_from / EPOCHS / original
            if sha(original_path) != digest:
                raise ValueError(f"Original source hash differs: {original}")
            shutil.copyfile(original_path, target)
        if sha(target) != digest:
            raise ValueError(f"Published evidence hash differs: {target}")
        sources[name] = {
            "sha256": digest,
            "bytes": target.stat().st_size,
            "original_repository_relative_path": EPOCHS + original,
        }
    regular, bold = font_path(args.font, FONT_PATHS), font_path(args.font_bold, BOLD_PATHS)
    fonts = load_fonts(regular, bold)
    records = {}
    frames, times = geometry_frames(evidence, fonts)
    records["initial-x1"] = encode(frames, times, args.assets / "initial-x1.mp4", 52.5, 52.5)
    del frames
    frames, times = protection_frames(evidence, fonts)
    records["protective-action"] = encode(frames, times, args.assets / "protective-action.mp4", 150.0, 85.0)
    manifest = {
        "schema": "physim-research-publication-v1",
        "update_date": "2026-10-20",
        "scope": "Presentation of already reviewed saved evidence. No native dynamics or new scientific inference.",
        "sources": sources,
        "renderer": {
            "path": "scripts/render_research_update.py",
            "sha256": sha(__file__),
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pillow": PIL_VERSION,
            "fonts": [{"name": p.name, "sha256": sha(p)} for p in (regular, bold)],
            "ffmpeg": subprocess.check_output(["ffmpeg", "-version"], text=True).splitlines()[0],
        },
        "display": {
            "geometry": {
                "field": "raw signed A, not Q or X1",
                "scale": [-1.5, 1.5],
                "palette": PALETTE,
                "pixel_interpolation": "nearest",
                "panel_order": ["W", "I", "S", "U"],
                "array_rows": "[-6,58) modulo 128",
                "array_columns": "[8,72)",
                "orientation": "array row increases downward; column increases rightward",
                "crop_physical_size": [32, 32],
                "domain_physical_size": [64, 64],
                "outline": "fixed original retained-neighborhood mask boundary; not a live tracker",
                "status": "original identity and phase copied from saved summary/observations",
            },
            "protection": {
                "field": "saved binary mask of normalized U0 > 0.45",
                "normalization": "(U0-u0)/(sqrt(2)-u0)",
                "u0": -0.5897545123014584,
                "archive_threshold_index": 1,
                "bit_order": "big",
                "packed_axis": -1,
                "pixel_interpolation": "nearest",
                "all_raw_threshold_pixels_shown": True,
                "view": "full domain, no crop",
                "domain_physical_size": [144, 144],
                "orientation": "array row increases downward; column increases rightward",
                "area_and_count_source": "recorded summary, not recomputed by renderer",
                "eligible_component_minimum_area": 2,
                "not_a_concentration_movie": True,
            },
        },
        "videos": records,
        "limitations": [
            "The two movies use different 19-field and 20-field preparations; they are not paired across movies.",
            "Geometry first-split intervals are sampled brackets, not exact event times or an exact delay.",
            "No original phase or material lineage is assigned after the first split.",
            "Protection concentrations at intermediate times 5 through 120 were not saved; those frames are masks.",
            "The evidence audit is not an independent dynamics replicate.",
            "Source-driven persistence and growth do not establish bounded homeostasis or autonomy.",
        ],
    }
    (args.assets / "provenance.json").write_text(json.dumps(manifest, indent=2, allow_nan=False) + "\n")
    print(
        json.dumps(
            {
                k: {
                    "file": v["file"],
                    "seconds": v["ffprobe"]["format"]["duration"],
                    "sha256": v["sha256"],
                    "checks": v["encoded_checks"],
                }
                for k, v in records.items()
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
