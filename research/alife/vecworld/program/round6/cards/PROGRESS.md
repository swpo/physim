# Study cards (round 6): progress

Worktree /home/user/wt/cards (branch wt-cards), study folder `research/alife/vecworld/program/round6/cards`.
Scratch: /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/cards (delete when done).
Coordinator channel: scratchpad/cards_COORD.txt (read at start and after waits).

## State (updated 11 Nov 2026, 10:55 UTC; this session is a RESTART, the first self left nothing committed)

Done
- Read: DECISIONS.md "Direction", program README (rounds 1-5 and the checkers' corrections), gpu-jobs PROTOCOL.md,
  LEDGER lessons, foundry (tnca.py, screen.py, criteria.py, job.py, checker findings), gliders wind world
  (wind.py, gworld.py), fed vortices (vortex_jax.py, vortex_world.py, vxlib.py), membrane (membrane_jax.py,
  membrane_world.py), vw.objects.

Design decided (not yet coded)
- One tool `cardlib.py`: a thin `Adapter` per world (init, tick with params as arguments, input channel, views:
  grid / fine grid / tracker), a generic GPU simulation (main run + branches from held-out test states: fresh-noise
  replicas, hidden-law neighbours at 3%, 10%, 100% of the prior, aimed / blind input arms), and a numpy analysis
  that builds the card offline from the small records. The job computes cards on the pod; raw records come back
  for a few worlds only (50 MB limit).
- Level kinds and their fixed cheap predictor family: grid (local 3x3 x 2-lag ridge), bodies (per-body ridge on
  wrapped displacements), vector (global ridge; quadratic variant; the vortex kind-share law).
- Controls: uniform / frozen / diffusion foundry draws, pure-noise field, non-interacting bodies.

Running: nothing. No GPU job submitted yet (ids will be r6-cards-001, ...).

Exact next step
1. Write `cardlib.py` (adapter type, simulate, analyse) and `adapters.py`; test on CPU at tiny size with the
   foundry adapter first, then gliders, vortex, membrane, controls.
2. Write and commit HYPOTHESES.md + criteria (thresholds) BEFORE the GPU request.
3. job.py / job.sh, CPU tiny run from a git archive of the requested paths, then request r6-cards-001.
