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
