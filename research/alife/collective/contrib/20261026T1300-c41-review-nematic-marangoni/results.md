# c41 review of 20261026T0505-c34-nematic-marangoni (SIBWMD), fresh seed 31

All runs: c34's world.py unchanged except the named WORLD_P key; labkit, 128^2, T=1000, 200 frames. Measures with
c34's own tools (swimdivide.py, sd_individuals.py channels 2,3, inherit.py).

| run | persistent splits / gen | swim >= 3 labkit BL then divide (best) | ring body-frames pass | cargo in/out (>=2) | daughters >= 2x |
|---|---|---|---|---|---|
| rerun (mar=40) | 26 / 4 | 7 (5.7 BL, track 16; by rod length best 2.84) | 1.00 (rim/core 2.59, rim/out 11.2) | 10.1 (1.00) | 36/36 at birth+5, 43/43 mid-life |
| ctl_mar0 (no Marangoni) | 24 / 4 | 0 (best 2.39) | 1.00 | 13.1 (1.00) | 0.97 |
| ctl_kappa0 (cargo not coupled) | 26 / 4 (same bodies) | 7 | 1.00 | 1.33 (0.05) | 0.00 |
| ctl_chis0 (no adsorption: wall-off) | 34 / 7 | - | 0.00 (rim/core 0.73) | 0.24 (0.00): s fills the body and expels the cargo | 0.00 |
| twin_passive (zeta=0, mar=0) | 0 / 0 | 0 (0 tracks move 1 BL) | ring and cargo membrane-like (FACTS) | - | - |

Track for the claim's life on my seed: seed 31 track 16 (strip_ring_seed31_track16.png): born by fission at frame 32,
ringed throughout, net 41 px (5.7 labkit body lengths, 2.84 rod lengths), pinches at frame 79 into ringed daughters 42 and 43.
Caveat: by rod (major-axis) length no track on seed 31 reaches 3 (c34's seeds: 2, 0, 0); M passes on labkit's sqrt(area) body length.
