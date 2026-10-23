# P7 static construction evidence · 23 October 2026

These are saved starting states, before any integration step or random draw.
[Read the comparison](../../../../research/updates/2026-10-23-p7-static-construction.md)
and the [standing evaluator's report](../../../../research/evaluation/2026-10-23-p7-static-construction.md).

The three contact sheets preserve every source PNG pixel. The interior images
use eight-bit native-resolution data, enlarged four times with nearest-neighbor
display. Native context is shown at its saved resolution. The prospective context
uses saved four-bit block means and is enlarged three times. A0 is cyan, A1 pale
yellow, and gray marks excluded readout pixels. Context does not replace a
readable interior feature. The source display mappings, masks and exact hashes
are recorded in [provenance.json](provenance.json).

The [original self-contained review HTML](../../../../research/evidence/2026-10-23-p7-static-construction/review.html)
contains all 38 unchanged embedded PNGs, including the intervention masks. Download
it and open it locally to inspect the complete saved presentation. Its bytes are
unchanged; it is kept outside the generated documentation pages.
[summary.json](summary.json) and [checks.json](checks.json) contain the collected
worker findings. [assessment.json](assessment.json) is the evaluator's scientific
assessment with only provider job metadata omitted. Its report hash identifies
the sealed source report; provenance records the public report's link relocation.

To reproduce the contact sheets from the repository root, use Python with
Pillow 11.3.0 and the recorded Arial.ttf (SHA-256 in provenance):

```sh
python3 scripts/render_p7_static_construction.py --out /tmp/p7-static-contact-sheets --font /path/to/Arial.ttf
```

The [renderer](../../../../scripts/render_p7_static_construction.py) validates the
HTML and every embedded PNG hash, retains the evaluator's layout and pixel
operations, and checks all three resulting PNG hashes. It reads saved images
only. It does not load scientific arrays or run the simulation. Font licensing
is separate; the font is not distributed here.
