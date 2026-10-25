# Fission screen on one r-two56 cog (c18)

One mature cog (from the claim's seed 2 at t=600, matter 300) planted in a 96^2 food-filled box (F=1, W=0) of the
claim's world (`world.py` with `"N":96`), run 400 t, once unperturbed and once per single-kernel perturbation
(`scripts/fscreen.sh`: m x0.95/1.05, h x0.75/1.25; `scripts/fscreen2.sh`: m x0.9/1.1, s x0.85/1.15; 6 kernels each).
Counted: A0 cores (blur 1, >0.3) every 50 t; fscreen.txt, fscreen2.txt.

- unperturbed: 1 cog throughout, matter 1.00.
- 40/48 perturbations: 1 cog throughout, matter 0.95-1.02 (it neither grows nor elongates).
- 7/48 die (k1 m 1.05, 1.1; k1 s 0.85; k4 m 0.9; k5 m 0.9; and k1 m 0.9 after the ring below).
- 1/48 (k1 m 0.9) grows as an expanding closed ring that meets itself across the periodic box at t~235 and
  annihilates (scr_k1m09.png), the same growth mode as the lcn worms and rings (lcn_rings_colD.png; 20261025T1518).
- 0/48 fission.

So r-two56's cog is a robust non-growing fixed point; the only growth mode reachable by single-kernel changes is an
unbounded front, and the question's "weaken the size limiter under scarcity" route has no fissioning state to switch to
(k0 x0.6-1.25 all stay one cog; k0 x0.6-0.7 from noise gives worms, 20261025T1437 and 20261025T1518).
