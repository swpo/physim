# c32 review of 20261025T2240-c27-ringswim-cut-repair (finding, R)

World: c28's ringswim-dl2 (world.py copied unchanged). twinrepair.py is c27's script with two added
options: ZERO_S (stricter wound: phi, K, L and S all set to 0 in the cut, so no substrate is left at
the wound) and KILL_K (control: also zero the catalyst K in the rest of the cell and a 4 px margin).

| run | seed | cells | wound | outcome |
|---|---|---|---|---|
| rerun/ (labkit) | 7 | #939, half cut 42% of matter at t=10000 | bath reset (world.damage) | a = 0.43 -> 0.85 (+400) -> 1.53 (+800), ringed; comparator merged at +300 |
| s8_zeroS | 8 | 27, 15 | S=0 | 27 re-closes (closure 0.36 -> 0.96 at +120), lives 3000 steps, swims 5.0 BL (twin 5.3); 15 dies at +60 |
| s8_bath | 8 | 27, 15 (same cuts) | bath S=1 | both re-close (0.36 -> 0.93 at +120; 0.26 -> 1.0 at +120), both live 1500 steps |
| s9_zeroS / s9_zeroS_fine | 9 | 3, 24, 5 | S=0 | 3/3 re-close (0.31-0.47 -> 0.97-0.98 at +120) and live |
| s9_zeroS_killK | 9 | 3, 24, 5 | S=0 + K removed from the rest of the cell | 3/3 die by +60 (twins live) |

Contraction before regrowth: the cut remnant does not heal its wound edge in place. It first
shrinks to 8-41% of the pre-cut area (min over 0-300 steps, at +60-120; s9 cells 3 and 5 split into
2 ringed pieces), the small round remnant is then fully ringed (closure ~1), and it regrows over
the next 200-800 steps (s9_zeroS_fine/twinrepair.png, 60-step frames). c27's own result.json files show
the same (area_min 11-30% of pre-cut in all 5 surviving cells). The undamaged twins' closure is
0.55-0.84, so closure >= 0.97 is the value of a small, freshly contracted cell, not a return to the
twin's state.
