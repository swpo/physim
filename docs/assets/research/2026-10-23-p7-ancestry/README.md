# P7 early history: evidence and display conventions

This is a presentation of an existing fresh CPU P7 movie, not a new simulation.
The standing evaluator inspected all 101 saved observations from simulation time
0 to 250, using full A0/A1 context and fixed detail views. The selected structure
forms from an initialized A1 spot. No qualifying parent-to-multiple-continuing-
individuals event appears on this exact track. The [independent account](../../../../research/evaluation/2026-10-23-p7-ancestry.md)
explains the result and limitations.

- [Complete 12.625-second early-history movie](early-history.mp4)
- [Six-frame overview](overview.png) and [full-context poster](poster.png)
- [Original 301-frame movie, time 0 through 750](../2026-10-23-p7-persistence/native-context.mp4)
- [Original display settings](../2026-10-23-p7-persistence/native-display.json)
- [Source-run metadata](../2026-10-23-p7-persistence/source-run-metadata.json)
- [Frozen scientific scope excerpt](review-scope.json)
- [Evaluator decision](evidence/decision.json), [all 101 observations](evidence/visual-observations.json),
  [direct human report](evidence/human-report.txt) and [publication account](evidence/publication-ready-account.txt)
- [Presentation hashes and every-frame encoding checks](presentation-provenance.json)
- [Public file manifest](publication-manifest.json)

The four evaluator files above and six original keyframe PNGs are exact copies.
Their internal references preserve the original evidence identities. Provider
and account records referenced by hash in the original decision are not published.
The scientific-scope excerpt omits operating checks and local selection-file
paths; it records the hash of the complete original frozen protocol. The original
review sheets are display derivatives; every underlying observation is retained
in the linked source movie and identified by its decoded PNG hash in the observation
record. The new video reproduces the same full A0/A1 panels and fixed neighborhood.

## Original illustrative frames

| Source frame | Simulation time | Evaluator caption |
| --- | --- | --- |
| [0](keyframes/source-000000.png) | 0 | Localized A1 spot present at initialization; the mature enclosure and curled interior are absent. No earlier parent is visible. |
| [12](keyframes/source-000012.png) | 30 | At t30, a distinct outer A1 ring surrounds the central spot, with an intervening A0 annulus. |
| [60](keyframes/source-000060.png) | 150 | At t150, one enclosure contains a rounded triangular central A1 island. |
| [72](keyframes/source-000072.png) | 180 | At t180, the internal A1 island is becoming lobed and indented within the continuing enclosure. |
| [84](keyframes/source-000084.png) | 210 | At t210, the curled A1 stripe, low-A1 bay and adjacent A0 band are recognizable. |
| [100](keyframes/source-000100.png) | 250 | At t250, the accepted selection anchor shows the nested organization used in the later persistence assessment. |

These six observations illustrate the complete review; they do not define exact
feature-onset thresholds. No new scientific measurements are inferred from pixels.

## Reading the movie

A0 is cyan and A1 is cream. They are two interacting numerical fields, not two
cell types. Full-domain panels are shown above the fixed detail views. Red boxes
mark the same detail neighborhood throughout; they are annotations, not detected
boundaries. Color limits remain those of the original movie: approximately
−0.681 to 1.385 for A0 and −0.722 to 1.414 for A1.

Each encoded frame corresponds to exactly one retained source observation:
source indices 0–100, with simulation time = 2.5 × index. At eight video frames per
second, each observation lasts 0.125 seconds. There are no interpolated states,
extra opening/end holds, adaptive crops, field recoloring or inferred motion.
Full panels are enlarged 2× and detail panels 3× with nearest-neighbor sampling.
The source itself is an encoded display, so these are not raw concentration values.

The source movie has SHA-256
`b23e458f986f05e50c7df259b8b9e01d9634e872bf88e4eb2d8b7f94fbc99d3d`.
The full frozen review protocol has SHA-256
`054c4edc55ff4a0eea8f9bda90fee3bae96b99b0a429e6eeade92ba1757cd7d5`.
The original evaluator decision has SHA-256
`65045d0b7dbdba1dc76be7c601c0b42966792829b845cc4197cda0544a328757`.

## Reproduce the presentation

The [renderer](../../../../scripts/render_p7_ancestry.py) reads only the existing
encoded movie. It does not import the model or read field/checkpoint arrays.
Use Pillow 12.1.0 and FFmpeg/ffprobe 8.0.1 to match the recorded toolchain. Pillow's
embedded scalable font supplies the labels. From the repository root:

```sh
python3 scripts/render_p7_ancestry.py
```

The renderer verifies the source hash, generates the movie and static images,
then decodes and compares every one of the 101 encoded frames to its presentation
PNG. The provenance lists those errors, source-frame hashes, output hashes and
fixed crop coordinates. The average RGB pixel-error checks are only encoding
validation; they are not biological metrics or evidence of material ancestry.
