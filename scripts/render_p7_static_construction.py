"""Reproduce the P7 static contact sheets from saved PNGs, without field analysis.

Run with Pillow 11.3.0 and the recorded Arial font for byte-identical output.
Only existing images are decoded; there is no simulation or NPZ input.
"""

import argparse
import base64
import hashlib
import io
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--out", type=Path, required=True)
parser.add_argument("--font", type=Path, default=Path("/System/Library/Fonts/Supplemental/Arial.ttf"))
parser.add_argument(
    "--review-html", type=Path, default=root / "research/evidence/2026-10-23-p7-static-construction/review.html"
)
parser.add_argument(
    "--provenance", type=Path, default=root / "docs/assets/research/2026-10-23-p7-static-construction/provenance.json"
)
args = parser.parse_args()
provenance = json.loads(args.provenance.read_text())
raw = args.review_html.read_bytes()
assert hashlib.sha256(raw).hexdigest() == provenance["saved_png_extraction"]["source_html_sha256"]
pngs = [base64.b64decode(x, validate=True) for x in re.findall(rb"data:image/png;base64,([^'\"]+)", raw)]
rows = provenance["saved_png_extraction"]["images"]
assert len(pngs) == len(rows) == 38
for i, r in enumerate(rows):
    assert r["figure_index"] == i
    assert len(pngs[i]) == r["bytes"]
    assert hashlib.sha256(pngs[i]).hexdigest() == r["sha256"]
if not args.font.is_file():
    parser.error("Pass --font with the recorded Arial.ttf; see the evidence README.")
assert (
    hashlib.sha256(args.font.read_bytes()).hexdigest()
    == provenance["presentation_renderer"]["environment"]["font_sha256"]
), "Font differs from the recorded renderer"
font = ImageFont.truetype(str(args.font), 24)
small = ImageFont.truetype(str(args.font), 18)
out = args.out
out.mkdir(parents=True, exist_ok=True)
labels = {
    "S": "S: no pulse",
    "B": "B: boundary-region pulse",
    "C": "C: exterior-control pulse",
    "D": "D: interior pulse",
    "DB": "DB: interior + boundary",
    "DC": "DC: interior + exterior",
}
outputs = []
for kind, predicate, scale, cellw, cellh, columns in [
    ("interior", lambda r: "interior readout" in r["caption"], 4, 680, 390, 3),
    ("native-context", lambda r: "full-domain static context" in r["caption"], 1, 1054, 572, 2),
    ("coarse-context", lambda r: "future context representation" in r["caption"], 3, 800, 444, 2),
]:
    groups = [[r for r in rows if r["arm"] == a and predicate(r)] for a in labels]
    assert all(len(g) == 2 for g in groups)
    height = 80 + ((len(groups) + columns - 1) // columns) * cellh
    im = Image.new("RGB", (columns * cellw, height), "white")
    d = ImageDraw.Draw(im)
    title = {
        "interior": "Fixed interior readout: existing 8-bit PNG pixels enlarged 4× by nearest neighbor",
        "native-context": "Existing native context: 512 × 512 pixels per activator",
        "coarse-context": "Existing prospective context: 128 × 128, 4-bit block means, enlarged 3×",
    }[kind]
    d.text((16, 12), title, fill="#152334", font=font)
    d.text(
        (16, 44),
        "Static states only. All saved pixels retained; no new crop, field scaling or numerical analysis.",
        fill="#334155",
        font=small,
    )
    sources = []
    for j, g in enumerate(groups):
        x = (j % columns) * cellw + 10
        y = 80 + (j // columns) * cellh
        d.text((x, y), labels[g[0]["arm"]], fill="#152334", font=font)
        for k, r in enumerate(g):
            src = Image.open(io.BytesIO(pngs[r["figure_index"]])).convert("RGB")
            if scale != 1:
                src = src.resize((src.width * scale, src.height * scale), Image.Resampling.NEAREST)
            px = x + k * (cellw // 2)
            d.text((px, y + 30), "A0" if k == 0 else "A1", fill="#334155", font=small)
            im.paste(src, (px, y + 54))
            sources.append({"figure_index": r["figure_index"], "source_png_sha256": r["sha256"]})
    p = out / (kind + "-contact.png")
    im.save(p)
    outputs.append(
        {
            "file": p.name,
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "scale": scale,
            "method": "Whole existing PNG pixel enlargement by nearest neighbor and labeled composition only. No scientific array decoding, field recoloring, crop, numerical metric or alternate view.",
            "sources": sources,
        }
    )
expected = {r["file"]: r["sha256"] for r in provenance["presentation"]["outputs"]}
for result in outputs:
    assert result["sha256"] == expected[result["file"]], "Output differs: " + result["file"]
print(
    json.dumps(
        {"verified_embedded_images": len(pngs), "byte_identical_outputs": [r["file"] for r in outputs]}, indent=2
    )
)
