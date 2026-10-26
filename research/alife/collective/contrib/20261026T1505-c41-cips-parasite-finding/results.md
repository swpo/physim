# Parasitic autocatalyst on c40's dividing CIPS condensates (c41)

World: world_base.py = c40's world (c41 copy with a DRIFT option, default unchanged). pred.py adds a predator species c:
dc/dt = Dc Lsc^2 lap c - div(chic Lsc^2 c(1-c) grad p) + eat - kd c, and e loses eat, with
eat = kp e c^2 (order 2, Froese-Ikegami-Virgo's parasitic autocatalyst) or kp e c (1-c) (order 1).
All arms branch from c40's world at t=8000 (seed 0: 12 bodies; seed 1: 18 bodies), c seeded as weak uniform noise
(c0 |N(0,1)|, unstructured) or as 4-6 random Gaussian patches.

| screen | kinetics | outcome |
|---|---|---|
| screen1 (A-D) | order 2, kp 0.5-2, kd 0.02-0.05, no drift | c dies within 200-400 t; prey unaffected |
| screen2 (E-H) | order 2, kp 5-10, kd 0.1-0.3 | c grows in the bath too and eats every body within 200 t (12 -> 0), then dies (G, patches: 4 bodies eaten, 12 -> 8, prey recover to 13) |
| screen3 (I-L) | order 2 + drift up the prey's product (chic 3-6) | same all-or-nothing: 0 prey (I), 2 prey (L), or c dies (J) |
| screen4 (M-P) | order 1, kd just above 0.12 kp, drift | c finds every body (14 spots at t=8100) and eats all within 150-250 t, then starves |
| screen5 (Q-T) and the paired runs | order 1, rates 100x slower (kp 0.005-0.02, kd/kp 0.14-0.2), drift chic 1-3 | coexistence: one c condensate inside every body, prey divisions slow |

Paired runs (kp 0.02, kd 0.003, Dc 0.05, chic 3, order 1, noise c0 0.02; 8000 t), prey bodies at t = 8000 / 12000 / 15500:
- seed 0: predator arm 12 / 14 / 15, c-free twin 12 / 18 / 18
- seed 1: predator arm 18 / 18 / 17, c-free twin 18 / 19 / 19
At t=15500 c sits inside 15/16 (seed 0) and 18/18 (seed 1) bodies at median 0.65, outside 0.0004; body median area 114 px
(seed 0) vs 174 px in the twin (crops_s0_pred.png, crops_s1_pred.png). c never forms a free-living spot.
