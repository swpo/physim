# VW-1 fresh runs of the gliders world (6 Nov 2026)

Every number, chart and video on the "VW-1 Glider World" page comes from these runs of the VW-1 JAX world
(`../vw` library and `../port`: `aworld.build()`, `aworld.MapWorld`, `flowlenia_jax`, `phi`). The VW-0 simulator
(`level0/flowlenia.py`, `integrate/lenia_world.py`) produced no result. The VW-0 analysis and drawing helpers
(`integrate/analyze.py` estimators and `objects_stats`, `render_l1.py`, `make_videos.Pipe`) and the VW-0 checker's
blind rules were used read-only on the new outputs. Each set was re-run in part by an independent checker
(bit-identical); its corrections are in each `results/summary.json` under `checker.edits`, and its review is
`results/check.md`.

| folder | what | CPU |
|---|---|---|
| `closure/` | closure ceilings at 1-32 ticks for both views; 36 trajectories x 300 ticks, 144 test states x 6 futures x 32 ticks (47,160 member-ticks); learned level-1 predictors in JAX (`patchnet`, `slotnet`); learning curve; tau = 1 objects-gap decomposition; chaos curve to 96 ticks | about 3.2 h |
| `inputs/` | blind input visibility (32 states, 6 noise keys, twins in one rollout call, null = 0); designer-aimed steering (64 runs, 46 usable); autodiff input sensitivity of the coarse view (192 VJPs per horizon, checked against finite differences); late differences; steer video | about 3.0 h |
| `media/` | hero videos of the objects and coarse views from one agent episode (`World.reset(0)`, `World.step`); fusion/fission strip; legibility statistics (24 trajectories x 300 ticks); blind structure recovery on agent observations | about 0.5 h |
| `page/` | the page's simplified sensitivity figure and cropped fusion strip | - |

Not committed (regenerate with the scripts): the `.npz` arrays (level-1 records, test states, hero level-0 episodes)
and the `.mp4` videos. Scripts use absolute paths under `/home/user/evalwork/vecworld/vw1/` from the build session.

Headline results (with the checkers' corrections):

- Closure ceiling, best level-1-only predictor (learned networks included) against the true simulator:
  coarse 0.991, 0.967, 0.849, 0.495, 0.136, 0.078 and objects 0.833, 0.781, 0.632, 0.434, 0.210, 0.048 at
  1, 2, 4, 8, 16, 32 ticks. Lower bounds: the networks still improve with data at 1-8 ticks (coarse) and 1-16 (objects).
- tau = 1 objects gap: fusion/fission slot-ticks are 11.8% of slot-ticks and carry 69% of AR(1)'s error (every
  tick); for the best network 53% +- 14% (144 test states).
- Chaos: the spread between copies of one state doubles every 2.3 ticks (coarse); half the natural spread at
  42 ticks (coarse) and 27 (objects).
- Blind random admissible inputs: median signal-to-noise <= 0.013 at every horizon, worst state 0.80; 87% of
  touched cells are empty. Designer-placed within budget: median <= 0.092. Aimed steering: 35/46 runs (76% +- 8%)
  turned the expected way, 22/23 without fusion or fission.
- Autodiff sensitivity agrees with finite differences at 1 tick (median relative error <= 2.2e-4), at 2 ticks for
  typical cells only, not from 4 ticks; sensitivity sits on and within 4 px of matter.
- Level 1: mean 7.4 bodies, 12.8 px long, one body length in 7.8 ticks; 22.5 fusions and 22.3 fissions per 100
  ticks; mass conserved to 2e-14.
- Anonymisation: blind rules recover the slot of all 132 coordinates of the 11 occupied slots and pair every coarse
  coordinate with its own block from one agent episode.
