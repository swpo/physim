# Review of 20261025T1915-c22-wavepin-front-cut-no-repair (negative finding: no front re-nucleation)

Written before reading other reviews of this finding.

Runs (fresh seeds 5 and 6; the world is deterministic after the planted start, so seeds change the heading
and the initial noise only):
- labkit pack of the claimed world with the front cut inside the world (`WORLD_P={"cut_t":8,"cut_mode":"front","cut_frac":0.3}`,
  80 frames, t=16): rerun/seed5, rerun/seed6. The sheet shows the half-moon crawler, the dumbbell after the cut,
  and a static round disk from t~12 to 16 (plus a small fragment that also rounds up).
- The author's branch script (cutrun.py, cut at t=8, undamaged twin, to t=16) on seeds 5 and 6:

| arm | area cut | protein lost | cut cell at t=16 | twin speed |
|---|---|---|---|---|
| front 30% s5 / s6 | 0.21 | 0.23 / 0.24 | static uniform-high disk, area 2.15, speed 0.000 | 0.301 |
| front 15% s5 / s6 | 0.09 | 0.10 | static uniform-high disk 2.33 + a tiny static fragment | 0.301 |
| chem (polarity erased) s5 / s6 | 0 | 0.22 | extinct at t=8.96 | 0.301 |
| rear 30% s5 / s6 | 0.17 | 0.13-0.14 | crawls at 0.258-0.260, area 2.09-2.10 | 0.301 |
| dt/2 (dt=5e-4) front 30% s5 | 0.21 | 0.23 | static disk 2.16, speed 0.000 | 0.322 |
| dt/2 chem s5 | 0 | 0.22 | extinct at t=8.87 | 0.322 |

All of these reproduce the finding's numbers to two digits. dt/2 changes the twin's speed by 7% and nothing else.

New control of the proposed mechanism (world_keepC.py: the claimed world plus one line that returns the erased
protein to the remaining cell's cytosol, `lose=0`):
- front 30% s5 with the protein kept: the cell goes through the same dumbbell and rounds up at t~12, then
  re-polarizes and crawls again as a half-moon at 0.27 (twin 0.30), polarized area 1.51
  (cuts/keepC_front0.3_s5/cut.png). So the static uniform-high disk is reached because the cut removes
  protein, as the finding argues (allowed-area window), not because the polarized state is unreachable.
- chem erase with the protein kept: still extinct at t=8.96: once rho < rho* everywhere the whole boundary
  retracts faster than the bound state can re-form.
This protein-kept recovery is not repair under the rubric (erased matter returned to the individual at the
wound); it confirms the mechanism and says which knob would matter.

Verdict: Supported (negative finding). Limits: planted crawler, single cut time, deterministic dynamics so the
two seeds are close to one experiment; I did not repeat the noise sweep.
