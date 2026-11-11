# PROGRESS: round 6, dials, designer "defect_gliders"

Design study (b) on the gliders wind world: an incomplete public law with a hidden extra term of strength eta.
Design phase only: no GPU, no model calls, small CPU checks.

- 11 Nov 02:40 UTC. Worktree made; program README, DECISIONS, ROADMAP 1 and 3, round-5 ladder README and its
  checker block read. CPU speed measured: 9.1 gliders ticks/s on one thread of the shared container
  (scratch `probe0.py`, 4 members x 50 ticks in 22.1 s).
- Plan: `dlaw.py` (gliders wind tick with five optional hidden terms, all off = the public law), `screen.py`
  (the round-5 screen at tiny size: oracle against the public-law simulator from the hidden state, per input
  program, passive against designed), `results/*.json`, then `DESIGN.md`.
- Candidates: G gust (flow gain above a wind threshold), XW stress conversion (c0 -> c1 above a wind threshold),
  M scar (slow field charged by strong wind that weakens growth), X dense conversion (c0 -> c1 above a density
  threshold), T terrain (static smooth field shifting the growth centres).
- 11 Nov 10:30 UTC. Container had restarted (nothing but this note survived; the note was not yet committed).
  Resumed: `dlaw.py` (five hidden terms, traced strengths), `probe.py` (results/probe.json: background wind
  magnitude max 0.119 over 400 ticks, mix aimed push peak 0.228, regional 0.153; wind trigger set to
  0.12-0.17), `screen.py` (state-given screen with common random numbers; smoke run: wind-triggered terms
  give bit-identical passive futures). Speed about 7 ticks/s on CPU.
- Next: screens G, XW, M, X, T at 6 states x 5 replicates x 8 ticks, calibration arm PAR (lR + 0.06),
  zero-point check, dial and horizon 16 for the chosen candidate, DESIGN.md.
- 11 Nov 11:03 UTC. Screens done at eta = 1 (6 states x 5 replicates x 8 ticks; results/screen_*.json):
  XW passive 0.000, aimed 0.150, regional 0.223, designed 0.264; M passive 0.000, aimed 0.126, regional 0.168,
  designed 0.248; G aimed 0.040, regional 0.032 (weak). Running in the background: X, T, PAR (calibration).
  Added to screen.py: a history-only surrogate (own level-1 start + other states' increments under each law)
  and a per-state cache of public futures; `check_zero.py` and `dose.py` written, not yet run.
- Next: check_zero, XW and M reruns with the surrogate, XW at eta = 4, dose-response, horizon 16, DESIGN.md.
- 11 Nov 11:20 UTC. First chain done (results/screen_{G,M,X,T,PAR}_1.json): G weak (0.03-0.06), X inert at
  every program (0.000; the density trigger is not reached, also not by a converging wind), T 0.20 in passive
  episodes (visible without inputs; history-only surrogate 0.01-0.02), PAR (lR + 0.06, calibration) 0.07 with
  surrogate 0.013. Second chain running: check_zero, XW at eta 1 and 4 with the surrogate, dose-response,
  M with the surrogate, XW eta 4 to horizon 16.
- 11 Nov 11:48 UTC. All CPU checks done (results/summary.json collects them). check_zero: traced zeros are
  bitwise equal to gworld.tick. XW at eta 4: state-given 0.29 / 0.42 (aimed / regional, 8 ticks), 0.32 / 0.50
  to 16 ticks; dose-response clean. New: `surrogate.py`, a simulation-trained history-only family (LLR) and a
  GENERIC residual on it (RES): XW eta 4 keeps a share of 0.11 / 0.30 without the state (hidden-parameter
  calibration 0.003), but RES fitted on ONE true-world episode of the class closes 0.94 / 0.70 of it, on two
  0.93 or more. Forecast: the design beats P0 where it acts and is repaired by a generic residual.
  `views.py` (block + population view to 16 ticks), `baseline_by_class.py` (zero point by item class from the
  ladder's saved scores: sigma 0.013-0.020 in every class).
- Next: DESIGN.md, scratch deleted, worktree removed.
