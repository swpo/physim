# Q:marangoni-turnover-persistence, loop 1: tuning a trait-blind dilution for the Marangoni rods (c45, interim)

world.py = c34's Marangoni rods (20261026T0505-c34-nematic-marangoni, CARGO=0) plus a dilution every 10 frames: bodies
(phi > 0, merged across periodic edges) sorted by raster order of their first pixel; 256 uniforms from an RNG seeded only by
(run seed, event index); body i removed if u_i < p (inside the body dilated by 2 px: phi = mean bath phi, Q = s = 0).
REDIST=1 also puts the removed matter back at once, spread uniformly (the event conserves mean phi). Nothing reads a body's
kind, speed, size or age. Tuning on seed 80, 150 frames (T=750), labkit + c00's extract.py; turnover_stats.py per 20 frames
(tune/*/stats.txt), occupancy per 10 frames (tune/*/occupancy.txt).

| setting | removed | persistent splits (all / after frame 60) | splits per 20 frames after frame 60 | bodies at dilution, last 40 frames | occupancy t=750 (plateau without dilution ~0.08) | dividing tracks, median D |
|---|---|---|---|---|---|---|
| p 0.05 | 20 | 20 / 7 | 0-3 | 21-26 | 0.082 | 10, 1.57 |
| p 0.10 | 33 | 17 / 6 | 1-2 | 14-20 | (declining) | 8, 0.99 |
| p 0.20 | 42 | 10 / 4 | 0-2 | 8-11 | 0.024 | 5, - |
| p 0.10, kr 0.024 | 0 | 0 | - | 0 (nothing forms) | 0 | 0 |
| p 0.10, phi_b -0.58 | 35 | 18 / 9 | 0-4 | 15-20 | 0.065 | 7, 1.52 |
| p 0.10, phi_b -0.56 | 40 | 16 / 6 | 0-2 | 24-26 (refilled by nucleation: 157 tracks) | 0.081 | 6, 0.89 |
| p 0.10, REDIST | 35 | 21 / 11 | 0-5 | 21-27 | 0.077 | 12, 1.37 |
| p 0.20, REDIST | 52 | 11 / 5 | 0-2 | 11 | 0.027 | 6, 1.41 |

None reaches the question's target (12-20 bodies with >= 5 persistent splits per 20 frames). In every setting splits are
0 in frames 120-150. The dilution removes bodies, but the chemostat returns matter at its own rate kr (phi_b - phi), into
the bath, so survivors do not grow faster: mean phi stays at -0.62 to -0.64 (below phi_b = -0.6) and occupancy falls
from 0.08 to 0.02-0.03 at p = 0.2. Births are capped by supply, not by space. Putting the removed matter back at once
(REDIST) holds the body count and gives the most divisions (11 after frame 60, up to 5 per 20 frames), but still no steady
division. A stronger chemostat (kr 0.024) stops nucleation altogether; a higher bath (phi_b -0.56) refills the box by
nucleation rather than division. Rods in these runs swim no further than without dilution (0 of 54 dividing tracks reach
D >= 3 rod lengths).

Next (loop 2, running): the question's T=2000 design with p 0.10 + REDIST on seed 81, and the mar=0 floor, to see whether
divisions stop for good after the first plateau or continue at a low steady rate.

Limits: one seed per setting, 150 frames (about 1.5 of the early cycles). The per-window counts are small.
