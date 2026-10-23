"""Render already quantized P7 frames; no simulation, raw fields or new metrics.

Uses only Python's standard library and Pillow. Integer display codes are mapped
to the same fixed palettes, orientation and readout as the accepted static view.
All 101 observations are rendered for every arm, without interpolation.
"""

import argparse
import ast
import base64
import hashlib
import io
import json
import math
import re
import struct
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ARMS = ("S", "B", "C", "D", "DB", "DC")
LABELS = (
    "No pulse",
    "Boundary pulse",
    "Exterior pulse",
    "Interior pulse",
    "Interior + boundary",
    "Interior + exterior",
)
PALETTES = [
    bytes(round(i * f) for i in range(256) for f in factors) for factors in ((0.40, 0.94, 1.0), (1.0, 0.92, 0.72))
]
BBOX = (368, 448, 132, 212)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def npy(data, dtype, shape):
    stream = io.BytesIO(data)
    assert stream.read(6) == b"\x93NUMPY"
    version = stream.read(2)
    assert version in (b"\x01\x00", b"\x02\x00")
    width = 2 if version == b"\x01\x00" else 4
    size = int.from_bytes(stream.read(width), "little")
    header = ast.literal_eval(stream.read(size).decode("latin1").strip())
    assert header == {"descr": dtype, "fortran_order": False, "shape": shape}
    raw = stream.read()
    assert len(raw) == math.prod(shape) * int(dtype[-1])
    return raw


def load_arm(path, arm):
    with zipfile.ZipFile(path) as z:
        assert set(z.namelist()) == {
            name + ".npy"
            for name in ("readout_q8", "context_q4", "readout_indices", "baseline_readout_q8", "times", "arm_code")
        }
        assert all(item.file_size < 2680000 for item in z.infolist())
        codes = npy(z.read("readout_q8.npy"), "|u1", (101, 2, 4748))
        context = npy(z.read("context_q4.npy"), "|u1", (101, 128, 128))
        indices = [x[0] for x in struct.iter_unpack("<I", npy(z.read("readout_indices.npy"), "<u4", (4748,)))]
        times = struct.unpack("<101d", npy(z.read("times.npy"), "<f8", (101,)))
        assert times == tuple(i * 2.5 for i in range(101))
        assert npy(z.read("arm_code.npy"), "|u1", (2,)).rstrip(b"\0").decode() == arm
        baseline = npy(z.read("baseline_readout_q8.npy"), "|u1", (2, 4748))
    return dict(codes=codes, context=context, indices=indices, times=times, baseline=baseline)


def interior(data, frame, field):
    y0, y1, x0, x1 = BBOX
    im = Image.new("RGB", (x1 - x0, y1 - y0), (190, 190, 190))
    pixels = im.load()
    offset = (frame * 2 + field) * 4748
    palette = PALETTES[field]
    for index, value in zip(data["indices"], data["codes"][offset : offset + 4748]):
        y, x = divmod(index, 512)
        assert y0 <= y < y1 and x0 <= x < x1
        pixels[x - x0, y1 - 1 - y] = tuple(palette[value * 3 : value * 3 + 3])
    return im


def context(data, frame, field):
    packed = data["context"][frame * 16384 : (frame + 1) * 16384]
    values = bytes(((v >> 4) if field == 0 else (v & 15)) * 17 for v in packed)
    im = Image.frombytes("P", (128, 128), values)
    im.putpalette(PALETTES[field])
    return im.convert("RGB").transpose(Image.Transpose.FLIP_TOP_BOTTOM)


def render_overview(output, font_path):
    """Lay out saved PNG crops at three fixed times, without field analysis."""
    output = Path(output)
    title = ImageFont.truetype(str(font_path), 24)
    small = ImageFont.truetype(str(font_path), 17)
    result = Image.new("RGB", (1536, 1280), "white")
    draw = ImageDraw.Draw(result)
    draw.text((16, 12), "P7: the same fixed interior after each pulse", font=title, fill="#152334")
    draw.text(
        (16, 48),
        "A0 (cyan) left / A1 (cream) right. Fixed [0,1] display range. Gray = outside the readout.",
        font=small,
        fill="#334155",
    )
    selected = (
        (0, "t = 0 | immediately after pulse"),
        (80, "t = 200 | late window starts"),
        (100, "t = 250 | window ends"),
    )
    inputs = []
    for column, (frame, label) in enumerate(selected):
        path = output / "frames" / "interior" / f"frame-{frame:03d}.png"
        saved = Image.open(path).convert("RGB")
        inputs.append(dict(frame=frame, relative_time=frame * 2.5, sha256=sha(path)))
        x = 220 + column * 432
        draw.text((x, 86), label, font=small, fill="#152334")
        for row, arm in enumerate(ARMS):
            y = 120 + row * 190
            if column == 0:
                draw.text((16, y + 12), arm, font=title, fill="#152334")
                draw.text((16, y + 48), LABELS[row], font=small, fill="#334155")
            sx = 12 + (row % 3) * 512
            sy = 84 + (row // 3) * 310 + 53
            pair = saved.crop((sx, sy, sx + 488, sy + 240))
            result.paste(pair.resize((366, 180), Image.Resampling.NEAREST), (x, y))
    draw.text(
        (16, 1258),
        "Relative model time. See the movies and contact sheets for all 101 observations, including every late sample.",
        font=small,
        fill="#334155",
    )
    path = output / "overview.png"
    result.save(path)
    return dict(
        path=path.name,
        bytes=path.stat().st_size,
        sha256=sha(path),
        source_frames=inputs,
        method="Fixed PNG crops at t=0,200,250 for all six cases; nearest-neighbor resizing; no new field calculation.",
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    repo = Path(__file__).resolve().parents[1]
    asset = repo / "docs/assets/research/2026-10-23-p7-recovery"
    parser.add_argument("--evidence", type=Path, default=asset / "evidence")
    parser.add_argument("--font", type=Path, default=Path("/System/Library/Fonts/Supplemental/Arial.ttf"))
    parser.add_argument("--expected", type=Path, default=asset / "provenance.json")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--static-html", type=Path, default=repo / "research/evidence/2026-10-23-p7-static-construction/review.html"
    )
    parser.add_argument(
        "--static-provenance",
        type=Path,
        default=repo / "docs/assets/research/2026-10-23-p7-static-construction/provenance.json",
    )
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    font_path = args.font
    expected = json.loads(args.expected.read_text()) if args.expected.is_file() else None
    if expected:
        assert sha(font_path) == expected["presentation"]["font_sha256"], (
            "Use the recorded font for byte-identical output"
        )
    title_font = ImageFont.truetype(str(font_path), 24)
    small_font = ImageFont.truetype(str(font_path), 17)
    provenance = json.loads(args.static_provenance.read_text())
    assert sha(args.static_html) == provenance["saved_png_extraction"]["source_html_sha256"]
    static_pngs = [
        base64.b64decode(v, validate=True)
        for v in re.findall(rb"data:image/png;base64,([^\x27\x22]+)", args.static_html.read_bytes())
    ]
    static_rows = provenance["saved_png_extraction"]["images"]
    data, sources, outputs, checks = {}, [], [], []

    def save(im, name):
        target = args.out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        im.save(target)
        outputs.append(dict(path=name, bytes=target.stat().st_size, sha256=sha(target)))

    for arm in ARMS:
        folder = args.evidence / arm.lower()
        summary = json.loads((folder / "summary.json").read_text())
        assert summary["complete"] is True and summary["execution_valid"] is True
        data[arm] = load_arm(folder / "trajectory.npz", arm)
        sources.append(
            dict(arm=arm, trajectory_sha256=sha(folder / "trajectory.npz"), summary_sha256=sha(folder / "summary.json"))
        )
        for kind, renderer, caption in [
            ("interior", interior, "interior readout"),
            ("context", context, "future context representation"),
        ]:
            rows = [r for r in static_rows if r["arm"] == arm and caption in r["caption"]]
            assert len(rows) == 2
            for field in (0, 1):
                prior = Image.open(io.BytesIO(static_pngs[rows[field]["figure_index"]])).convert("RGB")
                current = renderer(data[arm], 0, field)
                assert current.size == prior.size and current.tobytes() == prior.tobytes()
                checks.append(dict(arm=arm, view=kind, field=field, initial_pixels_match_static=True))
        for page, first in enumerate(range(0, 101, 36)):
            count = min(36, 101 - first)
            atlas = Image.new("RGB", (1360, 70 + math.ceil(count / 4) * 202), "white")
            draw = ImageDraw.Draw(atlas)
            draw.text(
                (12, 10),
                f"{arm}: {LABELS[ARMS.index(arm)]} | all saved observations, page {page + 1}/3",
                font=title_font,
                fill="#152334",
            )
            draw.text(
                (12, 42),
                "Fixed interior readout; A0 left / A1 right. Relative time after pulse. Gray = outside readout.",
                font=small_font,
                fill="#334155",
            )
            for j in range(count):
                i = first + j
                x, y = 10 + (j % 4) * 340, 70 + (j // 4) * 202
                draw.text((x, y), f"t = {i * 2.5:g}", font=small_font, fill="#152334")
                for field in (0, 1):
                    atlas.paste(
                        interior(data[arm], i, field).resize((160, 160), Image.Resampling.NEAREST),
                        (x + field * 164, y + 27),
                    )
            save(atlas, f"atlases/{arm.lower()}-{page + 1}.png")
    for kind, renderer, size in [("interior", interior, 240), ("context", context, 240)]:
        for frame in range(101):
            im = Image.new("RGB", (1536, 720), "white")
            draw = ImageDraw.Draw(im)
            draw.text(
                (16, 12),
                f"P7 recovery comparison | {kind} | relative time {frame * 2.5:g} / 250",
                font=title_font,
                fill="#152334",
            )
            draw.text(
                (16, 46),
                "All six cases share one new noise branch. Fixed display scales; no time interpolation.",
                font=small_font,
                fill="#334155",
            )
            for j, arm in enumerate(ARMS):
                x, y = 12 + (j % 3) * 512, 84 + (j // 3) * 310
                draw.text((x, y), arm + ": " + LABELS[j], font=title_font, fill="#152334")
                for field in (0, 1):
                    draw.text((x + field * 248, y + 31), "A" + str(field), font=small_font, fill="#334155")
                    im.paste(
                        renderer(data[arm], frame, field).resize((size, size), Image.Resampling.NEAREST),
                        (x + field * 248, y + 53),
                    )
            save(im, f"frames/{kind}/frame-{frame:03d}.png")
    record = dict(
        method="Presentation of existing quantized frames only; fixed accepted pixels, palettes, readout and orientation. No raw-field analysis, metric, recentering or simulation.",
        observations_per_arm=101,
        arms=list(ARMS),
        sources=sources,
        checks=checks,
        renderer_sha256=sha(Path(__file__)),
        font_sha256=sha(font_path),
        outputs=outputs,
    )
    (args.out / "render-provenance.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if expected:
        expected_outputs = {x["path"]: x["sha256"] for x in expected["presentation"]["outputs"]}
        assert len(outputs) == len(expected_outputs) == 220
        for result in outputs:
            assert result["sha256"] == expected_outputs[result["path"]], result["path"]
    overview = render_overview(args.out, font_path)
    if expected and expected.get("overview"):
        assert overview["sha256"] == expected["overview"]["sha256"]
    print(
        json.dumps(
            dict(
                rendered_frames=202,
                atlases=18,
                static_pixel_checks=len(checks),
                verified_outputs=len(outputs) if expected else 0,
                overview_sha256=overview["sha256"],
            )
        )
    )


if __name__ == "__main__":
    main()
