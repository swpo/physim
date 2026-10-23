# P7 persistence evidence

The [full-context movie](native-context.mp4) is a byte-identical copy of the saved
11 October 2026 visualization. It has 301 frames at 16 frames per second,
covering simulation time 0–750 with 2.5 units between saved observations.
The reviewed interval is frame 100 through 300, simulation time 250–750.
[Source-run metadata](source-run-metadata.json) and [fixed display settings](native-display.json)
describe the original realization. No new simulation was run for this review.

The [overview](p7-persistence-overview.png) shows six evenly spaced observations.
It uses fixed full-domain activator panels and fixed detail crops. Yellow boxes
mark the viewing window, not a physical boundary or an automated track.
The [per-sample judgments](visual-observations.json) are the standing evaluator's
manual visual observations; they are not automated measurements.

## Reproduce the overview

The source movie, the observation JSON and [the original presentation script](render_overview.py)
are sufficient. Install FFmpeg and Pillow, then run the commands below from this
directory. They only decode movie pixels and compose the figure.

```python
from pathlib import Path
import subprocess

Path("frames").mkdir(exist_ok=True)
for frame in [100, 140, 180, 220, 260, 300]:
    subprocess.run([
        "ffmpeg", "-v", "error", "-i", "native-context.mp4",
        "-vf", f"select=eq(n\\,{frame})", "-frames:v", "1",
        "-fps_mode", "passthrough", "-y", f"frames/native-{frame:06d}.png",
    ], check=True)
subprocess.run(["python3", "render_overview.py"], check=True)
```

The retained presentation script uses macOS Arial at its explicit system-font
path. On another system, choose an available font in `font_path`; caption pixels
will then differ. Different video-decoder versions can also change decoded pixels
slightly. The published overview and source movie have fixed hashes in
[the provenance record](provenance.json). No intermediate scientific motion is generated.
