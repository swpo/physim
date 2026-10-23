"""Compose selected already-reviewed movie pixels for the public report."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
indices = [100, 140, 180, 220, 260, 300]
panels = {"A0": (158, 142, 482, 468), "A1": (750, 142, 1074, 468)}
details = {"A0": (220, 166, 316, 262), "A1": (812, 166, 908, 262)}
font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
title = ImageFont.truetype(font_path, 36)
body = ImageFont.truetype(font_path, 23)
small = ImageFont.truetype(font_path, 19)
canvas = Image.new("RGB", (1980, 1490), "white")
draw = ImageDraw.Draw(canvas)
draw.text((20, 16), "One selected enclosure keeps its nested feature", fill="#18283B", font=title)
draw.text((20, 62), "P7: t = 250 to 750. Six evenly spaced views from 201 inspected samples. A0 = cyan; A1 = cream.", fill="#334155", font=body)
draw.text((20, 94), "Yellow rectangles show the fixed viewing window, not a physical boundary or an automated tracker.", fill="#334155", font=small)
observations = json.loads((BASE / "visual-observations.json").read_text())
by_frame = {r["encoded_frame_index"]: r for r in observations["observations"]}
sources = []
for j, i in enumerate(indices):
    x, y = (j % 3) * 660, 140 + (j // 3) * 640
    p = BASE / "frames" / f"native-{i:06d}.png"
    frame = Image.open(p).convert("RGB")
    draw.text((x + 7, y), f"t = {i * 2.5:g} simulation units", fill="#18283B", font=body)
    for name, px, dx in [("A0", 5, 108), ("A1", 331, 360)]:
        draw.text((x + px, y + 31), name, fill="#18283B", font=small)
        canvas.paste(frame.crop(panels[name]), (x + px, y + 56))
        if by_frame[i]["apparent_identity"] == "supported":
            box = (x + px + 62, y + 56 + 24, x + px + 158, y + 56 + 120)
            draw.rectangle(box, outline="#EAB308", width=3)
        draw.text((x + dx, y + 389), f"{name}: fixed detail", fill="#334155", font=small)
        canvas.paste(frame.crop(details[name]).resize((192, 192), Image.Resampling.NEAREST), (x + dx, y + 416))
    sources.append({"encoded_frame_index": i, "simulation_time": i * 2.5, "decoded_frame_sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
draw.text((20, 1435), "Sampled visual persistence; material continuity, confinement and active maintenance remain untested.", fill="#334155", font=body)
target = BASE / "p7-persistence-overview.png"
canvas.save(target)
manifest = {"method": "Six evenly spaced, already-reviewed observations. Fixed full-domain panels, fixed detail crops enlarged 2x by nearest-neighbor, yellow fixed-window rectangles only where visual identity is supported. No field decoding or numerical feature calculation.", "sources": sources, "panel_boxes_xyxy": panels, "detail_boxes_xyxy": details, "output": {"path": str(target), "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}, "presentation_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(BASE / "overview-provenance.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(manifest["output"]["sha256"])
