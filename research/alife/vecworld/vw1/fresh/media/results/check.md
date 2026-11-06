# Check of the media key

**Verdict:** every number is from VW-1 and reproduces exactly. I fixed one wrong comparison value and five wording problems in `summary.json` (listed under `checker.edits`).

I used core 3 only, about 140 CPU-s. My scripts and outputs are in `/home/user/evalwork/vecworld/vw1/fresh/media/check/`; the original summary is kept as `check/summary.orig.json`.

## Provenance (read from the scripts)
- **Runs.** `hero_run.py` and `stats_run.py` use `aworld.build()` and `MapWorld(spec, world_seed=0)`.
  - Hero episodes: `reset(0)`, then `step(None)` × 300.
  - Legibility ensemble: `designer.ensemble(24, seed=(7,))`. The npz confirms seed 7, shape (24, 301, 336) and the 50-tick burn-in.
- **Helpers.** The VW-0 helpers only read the saved VW-1 arrays.
- **VW-0 code.** `level0/flowlenia.py` never runs a step. The report's wording needs a fix, though:
  - `lenia_world` is imported by the tracker (it uses only the Level0 geometry and screen settings) and also by `analyze.py` (constants).
  - `render_l1` imports `level0/render.py`, which is a colour map.
- **Twins.** This key uses no twin differences, so no null is needed.
  - The cross-view identity reproduces in a fresh process: level 0 is equal for 61 ticks.
  - Control: world_seed 1 gives a different level 0 and a different in_map.

## Recomputed from saved data with my own code (`check/recompute.py`)
Every headline equals `legibility.json`: objects 7 / 7.437 / 6–9, body 12.806 px, speed 1.6376 px/tick, 7.820 ticks to cross, 1799 tracks, life 20, 16.4% ≥ 50 ticks, path 7.799 (all tracks 2.194), 98.0% ≥ 3 lengths, 22.54 / 22.28 events per 100 ticks (1623 / 1604, no births or deaths), encounters 18.36 and 63.3% fused, mass 148.7, event share 11.47% (11.98% at the 3 test ticks), drift 1.84e-14.

- My bootstrap SEs agree within about 15%.
- Hero: in all three views o = 1e-3·round(L1[out_map]/1e-3) bit for bit; objects view median 7 (4–10), 69 fusions, 68 fissions, 11 slots ever occupied; in_map identical across views.
- The blind rules match the checker's `blind_typing.py` and `blind_coarse.py`.

## Re-run end to end (`check/rerun.json`)
- **Objects hero, 60 ticks:** o, L1, level 0, tracker table and globals equal the saved file bit for bit.
- **`ensemble(2, seed=(7,))`, 30 ticks:** L1 and mass equal members 0–1 of the 24-member file exactly.

## Media
- Both videos: H.264 yuv420p, 896×590, 15 fps, 301 frames, 1.89 and 1.78 MB, black panels. I opened both posters, frames 5, 150 and 295 of each, and the PNG.
- Objects: every body has its glyph (tick 278: 8 slots, 8 bodies, worm = slot 4). One slot can cover two touching crescents (tick 150, slots 2 and 4, mass about 300). Bottom-edge glyphs spill over the strip label (cosmetic).
- Coarse: the blocks follow the matter.

## Corrections
1. **Event-slot share.** The summary gave the VW-0 value as 0.16. With the same definition over all ticks, VW-0 is **0.1148** (6517 of 56766), equal to the fresh 0.1147.
   - The page's "16% of the data" is a 3-tick sample (88 of 560); the fresh value at those ticks is 66 of 551, z ≈ 1.8.
   - The closure key should report the share at its own test ticks alongside its 75%, and note that the overall share is about 11.5%.
2. **Objects per tick.** The median moving from 8 to 7 is a quantisation effect. The means are 7.44 ± 0.11 now and 7.65 ± 0.09 for VW-0 (my recomputation). Say "seven or eight (mean 7.4)".
3. **Fusion figure.** Slot 0 is not "a glider": its mass is 277 and it formed by a fusion at tick 83.
   - With slot 8 (mass 423) it makes a 700-mass worm.
   - At tick 96 a 137-mass piece buds off and slot 8 keeps 563. "Splits again" overstates this.
4. **"New leak".** This is the checker's VW-0 shared-permutation finding, persisting. It matters only if one agent gets two views with the same world seed.
5. **Path.** The 7.8 body lengths is the median over tracks living ≥ 50 ticks; over all tracks it is 2.2. I added a `page_label` field.
6. **Rubric.** "Mass fixed" is changed to "conserved to 2e-14 relative", and "median 7" to "7–8, mean 7.4".

Everything else checks out: 132 of 132 and its explanation, the card, coarse 192 of 192, the both view, sizes, seeds and CPU time (0.133 s per member-tick after a 174 s init).
