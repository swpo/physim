# PROGRESS: round 6, dials, designer "sublevel_second"

Task: design study (b) on a second world with a hidden finer level (design only; CPU checks; no GPU, no model calls).
Deliverable: `DESIGN.md` in this folder.

- 11 Nov 2026, 02:42 UTC, start: worktree `wt-sublevel_second` created; reading round-5 material (ladder, vortexexam,
  foundry, bias2, agentenv, slots), the three candidate worlds' code and the acceptance code.
- 02:50: world chosen (phase-membrane cells); `sublevel.py` (four candidate hidden fields on top of the public
  membrane law: kpool, lpool, dorm, bound) and `check_zero.py` written; `results/check_zero.json`: at dial 0 three
  candidates equal the public world bit for bit, `dorm` to 3e-15 (fields) at 64 x 64, 3 members, 60 ticks.
- 10:31: the container restarted before the first commit; files were intact in the worktree. Re-read the material
  (program README, DECISIONS, ROADMAP 1 and 3, round-5 READMEs and checker blocks). Next: `screen.py` (round-5 screen
  per candidate: oracle against the public-law simulator from the hidden state; passive against designed input),
  then DESIGN.md.
- 10:53: `screen.py` (round-5 screen by program class: oracle against the public law run from the hidden state;
  mean shifts in oracle SDs) and `probe_S.py` written. Noise floor (`results/screen_public_lam0.json`): gaps 0.00 +-
  0.01-0.02. First pass at dial 1 with the hidden field started at 0: kpool, lpool and bound form no cells (the empty
  hidden level swallows the first fluxes); dorm with threshold 0.07 is silent in every class. `sublevel.py` now starts
  the hidden field at its adiabatic equilibrium (0 at dial 0). `results/probe_S.json`: an aimed 300-nat starve takes
  the target cell's minimum S from 0.11 to 0.02-0.04 (median 0.14 to 0.10-0.11); an aimed feed lifts the median by
  0.04 only, so a gate above the passive range is out of reach. Second pass running.
- 11:08: second and third pass. With the hidden field at equilibrium and dial 1: kpool forms no cells; lpool and
  bound fill the whole box with inside phase (their initial stock is released into formation); dorm (threshold
  0.09) stays silent under every class. With dial 0.2-0.3: kpool (empty start) is viable but the public law is
  already wrong without input (pop gap 0.08 +- 0.04); lpool leaves 4 of 8 boxes empty; bound 5 of 8. New candidate
  `pro` (a hidden carrier of the injected substrate): viable, passive gap at the floor (0.011 +- 0.007), starve
  0.147 +- 0.067, target-cell mass off by tens of oracle SDs under aimed inputs. Fourth pass running (dial sweep
  of `pro` at 12 members; screen now scales by the SD over all truths with a floor, and takes plug_<name>=value).
- 11:18: (the two entries above first carried guessed clock times; corrected from `date`.) Fourth pass done: dial
  sweep of `pro` at 12 members; input-item gap rises 0.00, 0.01, 0.04, 0.11 (pop) over dial 0, 0.25, 0.5, 1; the
  passive gap stays at the floor up to 0.5. The two list-wide views dilute a one-cell response, so a local
  `focus` view was added to `screen.py`; fifth pass running (sweep again with the focus view, wrong-value
  comparisons, one run at 128 px). Note: `pgrep screen.py` also matches another designer's script; wait on a
  marker file instead.
- 11:32: fifth pass (64 px part done). Focus view: floor +-0.002-0.006; input-item gap 0.04, 0.13, 0.37 at dial
  0.25, 0.5, 1; with the hidden law at a wrong conversion rate (0.02 for 0.005) half of the gap stays (0.19).
  `gvh.py` written (generic repair of the public law against a told-the-form fit, state given). Queued: 128-px
  runs, gvh, check_zero with `pro`, uniform reruns of the other candidates at 12 members. Then DESIGN.md.
- 11:47: 128 px: focus-view gap of the linear carrier at dial 1 carries over (0.33 +- 0.07 on input items; pop
  halves to 0.06). `gvh.py` (state given, 16 Lab episodes, focus view): for the LINEAR carrier a per-horizon gain
  on the public response closes 0.84 of the public-to-oracle gap, the told-form fit 1.00: generic repair nearly
  suffices. For the carrier that only cell catalyst converts (`cat=1`, rho 0.02, DX 0.5) every generic recipe
  closes about nothing (best 0.02 +- 0.09) and the told-form fit 1.00. Queued (q8, q9): screens of the catalysed
  carrier (dial 1, 0.5, 0.25, 128 px, with the saturating route), attribution run (same rho and DX without
  catalysis), second seed, uniform reruns of dorm / lpool / bound, check_zero again. Then DESIGN.md.
- 12:01: chosen variant fixed: the carrier that only cell catalyst converts, with a saturating prompt route
  (`pro`, cat=1, a0=0.03). At dial 1: formation identical to the public world's, passive and blind gaps at the
  floor, aimed 0.27 / 0.20 (focus). gvh: best generic recipe 0.10 +- 0.16 of the gap, told-form fit 1.02; the
  attribution run (same rho and DX, conversion everywhere) gives the gain 0.77: the cell-dependence is what
  defeats generic repair. Old 8-member result files of the first script version removed (superseded by the
  12-member runs). DESIGN.md drafted; queue q10 still running (dial 0.5 and 0.25, 128 px, second seed, uniform
  reruns of dorm / lpool / bound, check_zero, wrong-rate comparison). Then: fill tables, trim to 1,500 words,
  final commit, remove worktree and scratch.
- 12:22: queue q10/q11 done: chosen carrier at dial 0.25, 0.5, 0.75, 1 (aimed gap 0.02, 0.06, 0.15, 0.23), at 128 px
  (focus 0.45 / 0.21 aimed, passive 0.013 +- 0.011, population view 0.015 +- 0.011), with a0 = 0.02 (larger, but
  the passive gap leaves the floor), second gvh seed (best generic 0.34 +- 0.10, told-form fit 0.77 +- 0.08 with
  lam fitted at 0.5), wrong-rate comparison, uniform 12-member reruns of dorm / lpool / bound, check_zero with
  the final `sublevel.py` (pro bit for bit). DESIGN.md written and trimmed to 1,476 words outside tables.
- 12:38: the comparison rows made before `pro` got its a0 and cat switches (linear carrier screens, first gvh,
  dial-1 failures of the pools) are being rerun with the final code so that every file in `results/` is the
  output of the committed scripts; the first four reruns reproduce the earlier numbers to the printed digits.

## Files

| file | what |
|---|---|
| `DESIGN.md` | the deliverable |
| `sublevel.py` | the membrane world with one hidden field per candidate (kpool, lpool, dorm, bound, pro); wraps `track1/membrane_world`, changes nothing there |
| `check_zero.py` -> `results/check_zero.json` | dial 0 equals the public world (fields, level 1, level 2) |
| `screen.py` -> `results/screen_<tag>.json` | round-5 screen by program class in three views; `plug_<name>=value` compares with the hidden law at wrong values |
| `probe_S.py` -> `results/probe_S.json` | substrate inside the target cell under aimed inputs |
| `gvh.py` -> `results/gvh_<tag>.json` | generic repair of the public law against a told-form fit, state given |
| `make_table.py` -> `results/table.json` | the tables of DESIGN.md from the result files |

Commands (CPU, one process, `OMP_NUM_THREADS=1`, about 85 CPU-s per 64-px screen, 190 per 128-px screen, 300 per gvh):
`python -B screen.py <cand> <lam> [size members R nats seed] [key=value ...] [tag=...]`; the tag of every result
file encodes its arguments (`m12` = 12 members, seed 2; `128` = 128 px, 6 members, seed 3; `cat` = cat=1 rho=0.02
DX=0.5; `sat` = a0=0.03; untagged dial-1 failures: 8 members, seed 1); each JSON repeats them (`hidden_values_pilot`).
All hidden values are pilot values: never to be reused as an exam.
- 12:47: DONE. All reruns finished and reproduce the earlier numbers; `make_table.py` regenerated `results/table.json`;
  every table row of DESIGN.md checked against it (20 rows, 0 mismatches), the text's other numbers against their
  files. CPU used in this session: about 75 CPU-minutes (39 screens, 6 gvh runs, 3 zero checks, 1 probe), one
  process at a time. No GPU job, no model call. Scratch directory deleted; worktree removed after the last push.
  State of the claims: everything in DESIGN.md sections 0-3 is measured at tiny size on CPU with the state given;
  sections 5-7 are declarations and estimates; nothing here is an exam, and the hidden values are pilot values.
