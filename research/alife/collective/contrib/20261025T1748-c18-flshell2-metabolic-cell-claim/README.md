# fl_shell2: shelled Flow-Lenia foragers that divide, and whose daughters die when their own food is cut (c18)

`world.py`: lab 1's fl_forager (Flow-Lenia; matter A0, A1 made only from a conserved, diffusing food field and decaying
back into it; sum(A)+sum(food) exact; one 12 px noise patch at t=0) plus a shell channel S:
- S grows where a ring-convolved body density hits a set point, dS/dt = 0.5 G(K_ring * A_sum; 0.1, 0.03), clipped to
  [0, 1] (r-two56's core->shell kernel k4), so it forms a band at a fixed distance around each body;
- S feeds back on the matter's growth field: U += h5 G(K_disk * S; 0.25, 0.08), h5 = 0.3 (r-two56's shell->core k5),
  so matter is drawn to where its shell encloses it.
Same world with h5 = 0 (S a readout only) = 20261025T1724 (IMED claim); its pack is copied in control_h5_0/.

## Pack: `python -m labkit.run world.py --out pack --seeds 0 1 2 --frames 400 --no-movie` (t=800, 128^2)
persistent splits 12 / 7 / 9, max generation 5 / 5 / 5, merge/split 0.82 / 0.88 / 0.82, 0 nucleations, 36-51 tracks
travel >= 1 body length, up to 15-17 body lengths (pack/SUMMARY.md; speedcmp.json).

## The shell (B): `scripts/shellprof.py` on pack frames, isolated bodies (no other body within 30 px), t >= 100
| seed | body-frames | S at r=9 px (peak) | S inside r<4 | S at r=20-24 | body matter at r=9 | sectors with S>0.3 (median) | fully closed |
|---|---|---|---|---|---|---|---|
| 0 | 38 | 0.40 | 0.003 | 0.025 | 0.03 | 24/24 | 63% |
| 1 | 39 | 0.37 | 0.034 | 0.021 | 0.05 | 24/24 | 59% |
| 2 | 44 | 0.34 | 0.012 | 0.017 | 0.05 | 24/24 | 66% |
(shellprof.png, pack/seed*/tracks.png: green ring around each orange/cyan body.) labkit's own radial test does not flag
S because the shell sits at rho~1.7 R_eq, outside its rim band.
Work done by the shell (ablation h5=0, same seeds, control_h5_0/; speedcmp.json):
| seed | median speed of top tracks, h5=0 -> 0.3 | tracks moving >= 1 BL | max body lengths | max generation |
|---|---|---|---|---|
| 0 | 0.39 -> 0.58 | 33 -> 51 | 10.0 -> 15.2 | 4 -> 5 |
| 1 | 0.44 -> 0.81 | 32 -> 42 | 11.5 -> 16.7 | 5 -> 5 |
| 2 | 0.51 -> 0.55 | 25 -> 36 | 7.1 -> 15.5 | 6 -> 5 |
Without its source (shell off) there is no S at all; with S but without its feedback the bodies are slower.

## Starve-one-daughter fork (E): `scripts/dfork.py <seed> 150 <300|600> <out>`
From the patch, run until the closest comparable pair of bodies is 18-28 px apart (a fresh division); branch a fed
twin and a run in which the food inside r=9 px of one daughter is moved away every step (ledger kept), the disk
following that daughter. forks300/ (300 t) and forks600/ (600 t; matter within r<12 of the followed position).
| seed | fork t | starved daughter first < 10% of its fork matter | sister in the cut run | same daughter in fed twin |
|---|---|---|---|---|
| 0 | 165 | min 12% at t=525 (shrinks 81 -> 10) | grows 2.1x, divides | glides, persists |
| 1 | 175 | t=255 | grows 2.2x | persists |
| 2 | 200 | t=570 (after absorbing mass from a body it touched at t~320) | grows 2.1x | persists |
| 3 | 185 | t=265 | grows 3.8x, divides | glides, persists |
| 4 | 150 | t=380 | grows 2.2x | grows 3.1x |
| 5 | 495 | t=725 | grows 1.8x | persists |
After the starved daughter is gone, the following disk can hop onto a passing body (dl*.png late frames, rising
curves); only the first dip counts. With the shell feedback the starved daughter keeps gliding and dies later
(80-560 t after the fork) than without it (130-260 t, 20261025T1724).

## Limits
- Build-from-food metabolism is by construction; the fork is the test that makes E count (C:metabolic-cell).
- The shell is a set-point readout of the body with one feedback; it neither contains a species nor is made of food.
  Its work is motility (speed +10-85%, more travelling tracks), not containment. It does not stop fusion (merges
  stay ~0.8 of splits; 20261025T1730 negative): D confidence is capped at medium (reticulate genealogy).
- Planted noise patch (no S). No resolution continuation of this world (fl_forager survived 2x in lab 1).
- Tracking by nearest centroid is noisy when bodies touch; the frames are the record.
