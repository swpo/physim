# Review of 20261025T1500-c13-plenia-turnover-division (c18)

Fresh seed 7, the claim's own code, unchanged (`world.py`, `savehist_feed.py`, `splits_feed.py` copied from the claim).
- labkit: `python -m labkit.run world.py --out rerun/seed7 --seeds 7 --no-movie` (turnover arm, the world's defaults, t=1000):
  rings with inner particles and figure-8s in a particle gas from a random soup (rerun/seed7/particles.png); labkit splits 83,
  merges 95 (ratio 1.15), 0 persistent splits at K=20 frames, 17 persistent tracks, 54 components on average.
- Split census, t=0-1500, census every 2 t (`savehist_feed.py <P> 15000 20 7 h.pkl`, `splits_feed.py <P> h.pkl 20 <arm>`):
  | arm (seed 7) | persistent | clean (not from merge) | all splits | merges | from nothing | deaths | max gen | bodies t=500/1000/1500 |
  |---|---|---|---|---|---|---|---|---|
  | closed (feed=decay=0) | 30 | 2 | 185 | 197 | 195 | 121 | 4 | 54 / 60 / 62 |
  | turnover (defaults) | 35 | 6 | 78 | 98 | 234 | 150 | 3 | 59 / 60 / 64 |
  c13's ranges: closed 26-34 persistent, 5-6 clean, merges 171-224, max gen 4; turnover 34-52, 3-7 clean, merges 100-183, max gen 5.
- census/closed7.png: rings stretch into figure-8s and pinch into two rings that each keep inner particles (t=262-444),
  and several "splits" are two rings joined by a strand that separate again, as the claim says.
