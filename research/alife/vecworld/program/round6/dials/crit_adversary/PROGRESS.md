# PROGRESS (crit_adversary, round 6 dials)

Role: adversary critic of the three dial designs (defect_gliders, sublevel_second, compute_limit).
Deliverable: CRITIQUE.md (under 900 words) in this folder.

- 11 Nov, start: worktree /home/user/wt/crit_adversary made; program README, DECISIONS, ROADMAP 1 and 3 read.
- next: read the three designs' code; build the cheapest generic policy on sublevel_second (gvh.py, the only
  design that claims generic recipes fail); small CPU checks only.
- 13:58 UTC: three designs read (DESIGN.md, sublevel.py, gvh.py, screen.py, surrogate.py, compute_limit summary).
  Plan: defect_gliders and compute_limit already forecast their own failure with generic recipes they built; the
  one design that claims to resist is sublevel_second (generic 0.10-0.34 of the state-given gap, told-form 0.77-1.02).
  `adv_sim.py` repeats gvh.py's set-up call for call (so the designer's numbers are reproduced and its H is paired)
  and adds public-law runs under a filter bank on the command (delay x blur); `adv_fit.py` fits form-free repairs
  on the Lab (lagged gain; filter bank; both) and scores as gvh.py does. Seed 5 is the development seed; seed 6 and
  a new seed are run once with the recipe frozen. Scratch: s5.npz (running).
- 14:08: seed 5 (development seed), chosen carrier (lam 1, cat 1, rho 0.02, DX 0.5, a0 0.03): adv_sim reproduces the
  designer's L(pub), L(pub0), L(O), L(G2) exactly (max difference 0.0), so its H column is paired. First recipes
  (lagged gain, filter bank on the command, response mixing) close 0.17-0.31 of the gap pooled: no better than the
  designer's generic recipes. BUT by horizon: 55% of the public-to-oracle gap is the 32-tick horizon and 55% is one
  test member (8); at 4, 8, 16 ticks the designer's own per-horizon gain G2 closes 0.91, 0.87, 0.66 and the filter
  bank 0.90, 0.86, 0.55; at 32 ticks every linear recipe is negative. A perfect mean with the public spread would
  close 1.03, so the gap is all conditional mean. Next recipe (`adv_act.py`): the public law run under a linearly
  filtered command (4 numbers on a 39-point grid), so that the public law's own nonlinear growth carries the
  correction to 32 ticks. Running on seed 5.
- 14:27: `adv_act.py` on seed 5 (development) and seed 6 (recipe frozen before it ran). Results in
  `results/adv_s5.json`, `results/adv_s6.json` (`adv_fit.py`). Both seeds reproduce the designer's L(pub), L(pub0),
  L(O), L(G2) exactly; on seed 6 the designer's H is re-run here and reproduces its share (0.773).
  Share of the public-to-oracle gap closed at 4 / 8 / 16 / 32 ticks:
    seed 5: G2 (designer's gain) 0.91 0.87 0.66 -0.45; A_act 0.88 0.82 0.69 0.06; pooled 0.10 and 0.38 (se 0.17, 0.20)
    seed 6: G2 0.81 0.94 0.77 -0.05; A_act 0.92 0.90 0.84 0.06; H (told form) 0.56 0.62 0.60 0.91; pooled 0.34, 0.42, 0.77
  The gap is 55-56% at 32 ticks in both seeds; on seed 5 one test member of eight carries 55% of it (its focus cell
  dies without input, holds under the public law, grows explosively under the hidden law). The fitted filter is
  the same grid point in both seeds (direct gain 0.25, lagged gain 1, 3 ticks, 5 x 5 bumps).
  Reading: generic repair closes about 0.8 up to 16 ticks (as well as or better than the told form); the design's
  resistance is the 32-tick horizon alone. Seeds 7 and 8 running with `bank=0` (the designer's runs only, for G2
  by horizon on four seeds). Then CRITIQUE.md.
