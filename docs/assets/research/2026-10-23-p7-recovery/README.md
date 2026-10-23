# P7 recovery comparison: saved evidence and presentation

These are the retained outputs of one six-case comparison, not six independent
replicates. Read the [dated explanation](../../../../research/updates/2026-10-23-p7-recovery.md)
and [standing evaluator's assessment](../../../../research/evaluation/2026-10-23-p7-recovery.md)
for the scientific outcome and limitations.

[Watch the interior comparison](interior.mp4) · [Watch the wider context](context.mp4)

![All six cases at fixed relative times 0, 200 and 250](overview.png)

## What the images show

Each case starts from the same saved P7 checkpoint at model time 250, with its
registered pulse and a newly initialized, paired future noise stream. Relative
time runs from 0 to 250. Labels 250–500 in the metadata are source-clock labels;
this is not a continuation of the original historical random stream.

The two displayed activator fields are A0 (cyan) and A1 (cream). Display values
are clipped to the same [0,1] range in every case and frame. This affects the
display only; the simulated fields were not clipped. The interior view preserves
all 4,748 cells of the prebound readout, with eight-bit display codes. Gray marks
cells outside that readout, not zero concentration. Positions, orientation,
palettes and view bounds are fixed; the images are not recentered.

The wider context uses 4×4 block means from the original 512×512 grid, retained
as a 128×128 image with four bits per displayed field. It is deliberately coarser
than the interior view and is not a second recovery endpoint. Both views use an
origin at the lower left, matching the previously accepted static construction.

All 101 saved observations appear once in each 20.2-second movie, at five frames
per second. Each observation is held for 0.2 seconds. No intermediate scientific
motion is synthesized. The final scoring interval is relative time 200–250,
including all 21 saved observations; the three-time overview does not replace
inspection of that full interval.

## Exact records and all saved interior observations

| Case | Intervention | Exact result | Interior contact sheets |
| --- | --- | --- | --- |
| S | No pulse | [Summary](evidence/s/summary.json), [trajectory](evidence/s/trajectory.npz), [observation metadata](evidence/s/observations.jsonl) | [1](atlases/s-1.png), [2](atlases/s-2.png), [3](atlases/s-3.png) |
| B | Boundary-region pulse | [Summary](evidence/b/summary.json), [trajectory](evidence/b/trajectory.npz), [observation metadata](evidence/b/observations.jsonl) | [1](atlases/b-1.png), [2](atlases/b-2.png), [3](atlases/b-3.png) |
| C | Exterior-control pulse | [Summary](evidence/c/summary.json), [trajectory](evidence/c/trajectory.npz), [observation metadata](evidence/c/observations.jsonl) | [1](atlases/c-1.png), [2](atlases/c-2.png), [3](atlases/c-3.png) |
| D | Interior pulse | [Summary](evidence/d/summary.json), [trajectory](evidence/d/trajectory.npz), [observation metadata](evidence/d/observations.jsonl) | [1](atlases/d-1.png), [2](atlases/d-2.png), [3](atlases/d-3.png) |
| DB | Interior and boundary pulses | [Summary](evidence/db/summary.json), [trajectory](evidence/db/trajectory.npz), [observation metadata](evidence/db/observations.jsonl) | [1](atlases/db-1.png), [2](atlases/db-2.png), [3](atlases/db-3.png) |
| DC | Interior and exterior pulses | [Summary](evidence/dc/summary.json), [trajectory](evidence/dc/trajectory.npz), [observation metadata](evidence/dc/observations.jsonl) | [1](atlases/dc-1.png), [2](atlases/dc-2.png), [3](atlases/dc-3.png) |

The [protocol](evidence/protocol.txt), [fixed configuration](evidence/comparison-config.json)
and [exact experiment source](evidence/recovery_arm.py.txt) describe the registered
comparison. The public configuration replaces only the absolute controller home
path with `<REPOSITORY_ROOT>`; its original frozen hash and public-copy hash are
recorded separately in the provenance. Scientific values are unchanged. Each
pulse replaces the two activator fields in its mask with their
registered vacuum values while retaining the other six fields. The boundary and
exterior masks have equal area but different field state, dose and distance.

The evaluator's [machine-readable assessment](assessment.json),
[joint metadata checks](joint-metadata-checks.json) and
[concise reader-facing report](human-chat-report.txt) are published without
changes to their sealed source bytes. The provenance maps original scientific
source paths to the public files where those inputs are included in this package.

## Reproduce and verify the presentation

From the repository root, with Python and Pillow installed:

```sh
python3 scripts/render_p7_recovery.py --out /tmp/p7-recovery-render --font /path/to/Arial.ttf
```

The [renderer](../../../../scripts/render_p7_recovery.py) maps the already quantized
display codes, checks all 24 initial field/view pixel matches against the accepted
static evidence, and verifies all 220 frame/contact-sheet PNGs and the overview
against their published hashes. It performs no simulation or scientific field
analysis. The [provenance](provenance.json) records the exact font hash, software
versions, source/output hashes, video encoding commands and presentation choices.
The recorded Pillow version and font are needed for byte-identical text rendering.

H.264 movies are lossy viewing copies. All 202 encoded frames were decoded and
compared with their corresponding rendered PNGs; the [frame verification record](video-frame-verification.json)
contains those comparisons. Exact saved quantized records and reproducible PNGs
remain authoritative. The original full-field checkpoint and native execution
dependencies are hash-identified in the scientific records but are not all
bundled here; this package reproduces the retained evidence and its presentation.

Provider, account and credential records are excluded from this publication.
