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
