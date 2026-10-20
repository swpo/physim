# Research media · 20 October 2026

These videos present two completed experiments. They do not run a simulator or
reconstruct missing dynamics. See the [research note](../../../../research/updates/2026-10-20.md).

| Movie | Recorded evidence | Display |
| --- | --- | --- |
| `initial-x1.mp4` | Raw signed A, 29 times × four arms | Same fixed 32 × 32 crop of a 64 × 64 periodic domain; fixed clipped scale [−1.5, 1.5] |
| `protective-action.mp4` | Primary saved binary masks, 31 times × two arms | Full 144 × 144 domains; normalized U₀ > 0.45 |

No temporal interpolation is used. Each frame is held until the next recorded
time at five simulation units per video second; the final frame is held for two
seconds. Both movies are 1920 × 1080 H.264, 20 fps, with no audio and fast-start
metadata. Browser controls allow pausing or scrubbing.

The geometry crop uses array rows `[-6,58)` modulo 128 and columns `[8,72)`.
Array rows increase downward; columns increase rightward. The fixed outline is
the boundary of the initial retained region, not a live tracker. The
original-identity and Q-phase captions come directly from saved readouts. The
video does not assign identity or phase after the original splits.

The protection masks use threshold index 1 (0.45), unpacked in big-bit order
along the last axis. Every raw above-threshold pixel is displayed. The saved
eligible-component counts use area ≥ 2, while area labels report raw active area.
Normalization is `(U0-u0)/(sqrt(2)-u0)` with `u0 = -0.5897545123014584`.
Intermediate raw U₀ fields at times 5–120 were not retained; this is explicitly a
mask movie. An absent mask is not a claim that all fields equal zero.

## Re-render

With Python, NumPy, Pillow, FFmpeg and ffprobe installed:

```sh
python scripts/render_research_update.py
```

This reads the six committed files in `evidence/`, verifying every SHA-256 against
the renderer's fixed source pins. It does not need the original research cache.
`--capture-from /path/to/original/checkout` is an optional explicit acquisition
step; it copies only those exact six hash-verified outputs.

Fonts default to Arial on macOS or DejaVu Sans on Linux. Supply `--font` and
`--font-bold` to select exact fonts. `provenance.json` records font names and
hashes, library versions, source paths/hashes, pixel conventions, timing,
encoded hashes and video-stream metadata. Layout can differ with another font.
The encoder compares decoded first, turning-point and final frames against the
source images; mean absolute RGB error must be ≤ 5. Locally generated
`*-encoded-check.jpg` contact sheets are for review and are not published evidence.

The original NPZ and JSON files are byte-for-byte copies. They include recorded
experiment identities, configuration and diagnostics, but no provider credentials
or private account records. The summaries' original research-relative paths
identify acquisition provenance; only the six listed files are in this publication.

The native simulations used their historical pinned runtime and physics locks.
The rendering runtime recorded here is separate and performs presentation only.
