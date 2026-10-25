# Review of 20261025T2214-c26-eco-lenia2-claim c1 (IXDE, lenia; C:ecology-with-reproduction)

Written before reading other reviews. Fresh seed 5, the claim's settings (160^2, 500 frames x 20 steps, t=1000):
the claimed world (rerun/pack), its SEP=1 no-interaction twin (rerun/pack_sep), and the author's cutfork.py on the
median A cell and the median B cell at t=400 (cuts/).

| seed 5 | A reaches 20 cells | A mean cells t=100-400 | A mean t>=300 | B mean t>=300 | A persistent splits / max gen |
|---|---|---|---|---|---|
| shared food + exclusion | t=338 | 14.2 | 27.7 | 54.5 | 10 / 3 |
| separate food (twin) | t=124 | 28.6 | 31.2 | 53.1 | 16 / 3 |

- X: competition slows A's growth phase about 2.7x (the claim: 246-322 vs 120-130), A is below the twin through
  t~600 and ends at about the same count (29 vs 32 at t=1000); B gains slightly (+1.4 cells on average). Same sign on
  both partners as claimed.
- D: species A, all descended from one planted founder, makes 10 persistent splits and reaches generation 3 (labkit
  species tracking).
- E: holding the food at 0 in a 12 px disk at t=400 kills the A cell (below 10% of its matter by t=430; 0 at t=900)
  and the B cell (below 10% by t=425), while the same cells in the fed twins keep 96% and 104% and the neighbours
  outside the disk live on (cuts/cutA_s5.png). The dependence is true by construction (matter is built only from
  food and decays), so I list E as by construction.
- I: round cells persisting between divisions (cuts/cutA_s5.png, fed row).

Limits: planted founders (no S); exclusion is a coded coupling; the X effect is a transient growth-phase effect, gone
by t~600-1000; one fresh seed.
