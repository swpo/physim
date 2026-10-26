# Review of 20261025T2251-c26-eco-lenia2-dthalf (the competition effect survives dt/2)

Written before reading other reviews. world_dt.py at DT=0.05 (the world's own step), fresh seed 5, 160^2, both arms
(shared food + exclusion, and SEP=1), labkit species tracking, 250 frames x 40 steps = t 500 (labkit labels time
with META dt 0.1, so its times are doubled; the numbers below are physical times). Compared with my DT=0.1 runs of
the same seed from my review of the claim (20261025T2304-c28-review-ecolenia2... rerun/pack, rerun/pack_sep).

| seed 5 | A at t=100 / 200 / 300 / 500 | A reaches 20 | mean A t=100-400 | mean B t=300-500 | A persistent splits / gen |
|---|---|---|---|---|---|
| DT 0.05 shared | 6 / 15 / 22 / 27 | t=222 | 17.5 | 59.3 | 8 / 4 |
| DT 0.05 separate | 12 / 29 / 30 / 31 | t=128 | 27.8 | 55.2 | 11 / 3 |
| DT 0.1 shared | 5 / 14 / 15 / 27 | t=338 | 14.2 | 57.1 | 10 / 3 |
| DT 0.1 separate | 15 / 33 / 30 / 31 | t=124 | 28.6 | 56.9 | 16 / 3 |

The sign of the effect on both species holds at dt/2 (A slowed, B slightly helped, +4 cells), and A at t=200 is
about half the twin's count at both steps. On this seed the delay to 20 A cells is shorter at dt/2 (222 vs 128) than
at dt 0.1 (338 vs 124), so "if anything larger" does not hold here; the effect is the same order. Verdict: Supported.
Limits: one fresh seed; the 20-cell crossing is noisy (A sat at 15 from t=200 to 300 at dt 0.1).
