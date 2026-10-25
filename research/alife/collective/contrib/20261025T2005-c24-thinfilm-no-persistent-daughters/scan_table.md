labkit packs (seed 0, 128^2, t=4000, 80 frames) of the sighting's world.py, with WORLD_P overrides on top of its defaults
(csp 0.05, cp 0.5, pnoise 0.1, h0 1.6):

| run | overrides | bodies mean/max/final | persistent splits | merges/splits | max body lengths |
|---|---|---|---|---|---|
| sighting pack s0 | defaults (chpa 0.1, ca 0.1, mu0 0.002) | 9.6/18/5 | 1 | 18/11 | 1.1 |
| sighting pack s1 | defaults | 9.2/18/5 | 1 | 14/15 | 1.4 |
| sighting pack_ext s0 | chpa 0.2, ca 0.3, h0 2 | 1.8/5/3 | 0 | 11/19 | 2.3 |
| sighting pack_ext s1 | chpa 0.2, ca 0.3, h0 2 | 1.8/6/1 | 0 | 9/16 | 2.5 |
| scan/g1 | mu0 0, chpa 0.2, ca 0.1 | 5.4/20/2 | 0 | 28/19 | 3.5 |
| scan/g2 | mu0 0, chpa 0.2, ca 0.2 | 3.4/17/1 | 0 | 25/21 | 4.6 |
| scan/g3 | mu0 0.004, chpa 0.2, ca 0 | 5.2/14/3 | 0 | 28/20 | 3.4 |
| scan/g4 | mu0 0.004, chpa 0, ca 0 | 4.4/13/1 | 0 | 21/20 | 2.2 |

256^2, h0 3, mu0 0, chpa 0.2 (strip.py, seed 0, 16000 steps, dt 0.25; big_256_view.png): film components (h - ha > 1) every 125 t:
- ca 0.2: 1,1,1,1,6,7,7,8,8,7,12,9,11,7,6,9,11,10,9,9,7,6,9,7,7,4,5,5,5,7,5,6
- ca 0.3: 1,1,1,3,10,10,9,6,11,10,12,10,8,7,6,7,9,7,10,6,8,7,7,9,8,8,5,7,6,5,3,7
