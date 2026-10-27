# Screen (quick.py, seed 0, 128^2, t=3000; rows: density rho on top, food below; GS-type growth k c rho^2, d = F + kill)
Defaults differ by stage; each line gives the WORLD_P overrides of the screen-time world (base: Dr 0.08, Dc 0.16, kf 0.037, d 0.097, rc 0.15, w 0.5, lam 0.8).

| image | overrides | v0=0 twin | with motility |
|---|---|---|---|
| b0s / b0 | (labyrinth GS point) | static labyrinth | travelling straight bands |
| c_all rows 1-3 | kf 0.0367, d 0.1016; v0 0 / 1 / 0.4 | splitting spots (row 1) | bands (row 2), wavy fronts (row 3) |
| e_all rows 1-4 | Dc 1.0, v0 0; Dc 0.5 v0 0.25; Dc 1 v0 0.25; Dc 1 v0 0.4 | dense static spot lattice (row 1) | finite worms early, aligned bands by t~2000 |
| f_all rows 1-4 | Dc 0.5 v0 0.25 with d 0.1036 / 0.1056; d 0.1036 v0 0.4 lam 2; alpha 0.2 | | fronts -> bands; lam 2 gives chaotic crescent fronts; alpha 0.2 dies |
| g_all rows 1-4 | speed rises with density v = v0 rho^nv/(rho^nv + rs^nv): v0 0.5 rs 0.5; v0 0.8 rs 0.6 nv 4; v0 0.5 rs 0.5 lam 2; v0 1 rs 0.7 nv 4 | | bands; bands; chaotic fronts; bands |
| (not kept) | v0 0.1 / rc 0.3 v0 0.5 / w 2 v0 0.3 (spot point) | | everything dies: the splay of p spreads small spots below the growth threshold |
