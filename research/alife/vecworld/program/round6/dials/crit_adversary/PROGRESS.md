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
