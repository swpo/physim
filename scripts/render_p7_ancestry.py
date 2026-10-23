#!/usr/bin/env python3
"""Present the first 101 frames of the retained P7 movie; no field arrays.

Requires Pillow, FFmpeg and ffprobe. The published provenance pins their versions.
All spatial/color information comes from the existing encoded movie. No simulator,
numerical field diagnostics, segmentation, tracking or interpolated motion is used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

import PIL
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat

SOURCE_SHA = "b23e458f986f05e50c7df259b8b9e01d9634e872bf88e4eb2d8b7f94fbc99d3d"
PANELS = {"A0": (158, 142, 482, 468), "A1": (750, 142, 1074, 468)}
DETAILS = {"A0": (220, 166, 316, 262), "A1": (812, 166, 908, 262)}
FPS = 8
COUNT = 101
INK = (24, 37, 46)
MUTED = (75, 89, 98)
MARK = (166, 55, 45)
BACKGROUND = (250, 250, 247)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def run(args: list[str]) -> None:
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)


def probe(path: Path) -> dict:
    return json.loads(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=width,height,r_frame_rate,nb_frames,duration,pix_fmt",
                "-of",
                "json",
                str(path),
            ],
            text=True,
        )
    )["streams"][0]


def font(size: int) -> ImageFont.FreeTypeFont:
    # Pillow's embedded scalable font avoids a machine-specific system font.
    return ImageFont.load_default(size=size)


def text(
    draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, size: int = 24, color: tuple[int, int, int] = INK
) -> None:
    draw.text(xy, value, font=font(size), fill=color)


def compose(source: Image.Image, index: int) -> Image.Image:
    im = Image.new("RGB", (1536, 1152), BACKGROUND)
    d = ImageDraw.Draw(im)
    text(d, (32, 18), "P7 | The retained early history", 34)
    text(d, (1054, 22), f"Simulation time {index * 2.5:g} / 250", 28)
    text(d, (32, 61), "All 101 saved observations, every 2.5 time units. Fixed views and color scales.", 22, MUTED)
    for name, x in (("A0", 32), ("A1", 800)):
        text(d, (x, 94), f"Full-world {name}  |  " + ("cyan" if name == "A0" else "cream"), 25)
        im.paste(source.crop(PANELS[name]).resize((648, 652), Image.Resampling.NEAREST), (x, 130))
        px0, py0, _, _ = PANELS[name]
        x0, y0, x1, y1 = DETAILS[name]
        d.rectangle(
            (x + 2 * (x0 - px0), 130 + 2 * (y0 - py0), x + 2 * (x1 - px0) - 1, 130 + 2 * (y1 - py0) - 1),
            outline=MARK,
            width=2,
        )
        text(d, (x, 797), f"Fixed {name} detail of the marked neighborhood", 22, MUTED)
        im.paste(source.crop(DETAILS[name]).resize((288, 288), Image.Resampling.NEAREST), (x + 180, 828))
    text(
        d,
        (32, 1123),
        f"Selected retrospectively at t=250. Source frame {index}/300; no interpolated motion.",
        20,
        MUTED,
    )
    return im


def overview(sources: dict[int, Image.Image], indices: list[int]) -> Image.Image:
    im = Image.new("RGB", (1872, 840), BACKGROUND)
    d = ImageDraw.Draw(im)
    text(d, (24, 17), "The selected P7 neighborhood, from initialization to t=250", 32)
    text(
        d,
        (24, 58),
        "Six illustrative observations only. Each pair shows fixed A0 (cyan) and A1 (cream) details.",
        23,
        MUTED,
    )
    for j, index in enumerate(indices):
        x, y = 24 + (j % 3) * 624, 104 + (j // 3) * 360
        text(d, (x, y), f"t = {index * 2.5:g}   |   source frame {index}", 26)
        for k, name in enumerate(("A0", "A1")):
            im.paste(
                sources[index].crop(DETAILS[name]).resize((288, 288), Image.Resampling.NEAREST), (x + k * 300, y + 42)
            )
    text(
        d,
        (24, 813),
        "Full surrounding context and all 101 observations are in early-history.mp4. This figure does not establish copying.",
        20,
        MUTED,
    )
    return im


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source", type=Path, default=root / "docs/assets/research/2026-10-23-p7-persistence/native-context.mp4"
    )
    parser.add_argument("--output", type=Path, default=root / "docs/assets/research/2026-10-23-p7-ancestry")
    parser.add_argument("--overview-indices", default="0,12,60,72,84,100")
    args = parser.parse_args()
    indices = [int(n) for n in args.overview_indices.split(",")]
    assert len(indices) == 6 and indices == sorted(set(indices)) and all(0 <= i < COUNT for i in indices)
    assert sha(args.source) == SOURCE_SHA, "The retained source movie changed"
    source_stream = probe(args.source)
    assert (
        source_stream["width"],
        source_stream["height"],
        source_stream["nb_frames"],
        source_stream["r_frame_rate"],
    ) == (1600, 900, "301", "16/1")
    args.output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="p7-ancestry-presentation-") as tmp:
        tmp = Path(tmp)
        raw, presented, decoded = (tmp / name for name in ("source", "presented", "decoded"))
        for folder in (raw, presented, decoded):
            folder.mkdir()
        run(
            [
                "ffmpeg",
                "-nostdin",
                "-v",
                "error",
                "-threads",
                "1",
                "-i",
                str(args.source),
                "-frames:v",
                str(COUNT),
                "-vsync",
                "0",
                "-threads",
                "1",
                "-start_number",
                "0",
                str(raw / "%06d.png"),
            ]
        )
        records, chosen = [], {}
        for i in range(COUNT):
            src = raw / f"{i:06d}.png"
            source = Image.open(src).convert("RGB")
            assert source.size == (1600, 900)
            target = presented / f"{i:06d}.png"
            composed = compose(source, i)
            composed.save(target)
            if i in indices:
                chosen[i] = source.copy()
            records.append(
                {
                    "source_frame_index": i,
                    "simulation_time": i * 2.5,
                    "source_decoded_png_sha256": sha(src),
                    "presentation_png_sha256": sha(target),
                }
            )
        overview(chosen, indices).save(args.output / "overview.png")
        Image.open(presented / "000100.png").save(args.output / "poster.png")
        movie = args.output / "early-history.mp4"
        run(
            [
                "ffmpeg",
                "-nostdin",
                "-v",
                "error",
                "-y",
                "-framerate",
                str(FPS),
                "-start_number",
                "0",
                "-i",
                str(presented / "%06d.png"),
                "-frames:v",
                str(COUNT),
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "18",
                "-pix_fmt",
                "yuv420p",
                "-threads",
                "1",
                "-movflags",
                "+faststart",
                str(movie),
            ]
        )
        stream = probe(movie)
        assert (stream["width"], stream["height"], stream["nb_frames"], stream["r_frame_rate"]) == (
            1536,
            1152,
            "101",
            "8/1",
        )
        assert abs(float(stream["duration"]) - COUNT / FPS) < 1e-6
        run(
            [
                "ffmpeg",
                "-nostdin",
                "-v",
                "error",
                "-threads",
                "1",
                "-i",
                str(movie),
                "-vsync",
                "0",
                "-threads",
                "1",
                "-start_number",
                "0",
                str(decoded / "%06d.png"),
            ]
        )
        assert len(list(decoded.glob("*.png"))) == COUNT
        errors = []
        for i, record in enumerate(records):
            actual = Image.open(decoded / f"{i:06d}.png").convert("RGB")
            expected = Image.open(presented / f"{i:06d}.png").convert("RGB")
            error = sum(ImageStat.Stat(ImageChops.difference(actual, expected)).mean) / 3
            assert error < 4.0, (i, error)
            record["encoded_frame_mean_absolute_rgb_error_0_to_255"] = error
            errors.append(error)
    manifest = {
        "schema_version": 1,
        "scope": "Presentation of existing encoded movie pixels, not numerical field analysis or a new trajectory.",
        "source": {
            "path": "../2026-10-23-p7-persistence/native-context.mp4",
            "sha256": SOURCE_SHA,
            "bytes": args.source.stat().st_size,
            "stream": source_stream,
        },
        "renderer": {
            "path": "../../../../scripts/render_p7_ancestry.py",
            "sha256": sha(Path(__file__)),
            "pillow_version": PIL.__version__,
            "font": "Pillow embedded default scalable font",
            "ffmpeg_version": subprocess.check_output(["ffmpeg", "-version"], text=True).splitlines()[0],
        },
        "display": {
            "full_panel_boxes_xyxy": PANELS,
            "fixed_detail_boxes_xyxy": DETAILS,
            "enlargement": "Nearest-neighbor: full panels2x and detail3x; source colors/scales unchanged.",
            "annotations": "Red rectangles mark the same fixed detail neighborhood in every full panel.",
            "scientific_input_kind": "Lossy encoded display pixels, not raw field concentrations.",
            "time_mapping": "simulation time = source frame index * 2.5",
            "cadence_simulation_units": 2.5,
            "fps": FPS,
            "frame_hold_seconds": 1 / FPS,
            "interpolated_motion": False,
            "overview_indices": indices,
            "overview_selection": "Illustrative retrospective samples; entire fixed window remains in the video.",
        },
        "video_validation": {
            "all_encoded_frames_checked": COUNT,
            "stream": stream,
            "maximum_frame_mean_absolute_rgb_error_0_to_255": max(errors),
            "verification_limit": "Lossy encoding comparison checks presentation fidelity; it is not a scientific metric.",
        },
        "frames": records,
        "outputs": {
            name: {"bytes": (args.output / name).stat().st_size, "sha256": sha(args.output / name)}
            for name in ("early-history.mp4", "overview.png", "poster.png")
        },
    }
    dump(args.output / "presentation-provenance.json", manifest)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "frames": COUNT,
                "max_frame_rgb_error": max(errors),
                "outputs": manifest["outputs"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
