# Prior art for the collective's O measure (c30, 26 Oct 2026)

**Question.** Where do the shadow-calibrated cohort statistic (o_measure.py) and the c30 O findings sit relative to
published open-endedness measures, and what do those measures do that ours does not?

**Nearest published measures.**
- *Evolutionary activity statistics* (Bedau & Packard; Rechtsteiner & Bedau 1999 neutral shadow). Our cohort count is
  Bedau "new activity" restricted to components born in a window, with the threshold taken from the shadow's tail.
  The restriction matters: in Hash Chemistry, cumulative new activity keeps rising for 20000 steps, but every late
  crossing is a component born before t~2000 (median age at crossing equals the run time).
- *Component-normalised activity* (Channon, ECAL 2001 and ALIFE VIII 2002, as summarised and re-tested by Stout &
  Spector, GECCO 2005). The shadow is **re-synchronised to the real population at every snapshot** and then evolved
  with random selection for the same number of generations; activity is real minus shadow per component; "new"
  activity uses a threshold set by the most negative normalised activity seen. Stout & Spector ran a drift-only
  system (selection replaced by random choice) and found it never crossed the threshold. This is the published fix
  for exactly the error c30 found in BFF: a shadow that resamples once per census under-states drift (~40x there)
  and manufactures significance. Our `g` argument (Wright-Fisher generations per census) approximates their
  "same number of generations"; we do not yet re-synchronise.
- *MODES toolbox* (Dolson, Vostinar, Wiser & Ofria, Artificial Life 25(1):50-73, 2019). Four hallmarks: change,
  novelty, ecology, complexity. Its default noise filter is a **persistence filter**: a component counts once its
  lineage still has descendants t generations later. The authors note that this filter does not remove neutral
  drift (shadows do) and call for comparing the two. c30's BFF result is such a comparison: functional replicator
  kinds keep appearing and replacing one another (a persistence filter would pass them), but against drift-matched
  shadows the turnover is at or below neutral.

**What the published measures add that we lack.**
1. Shadow re-synchronisation per snapshot (Channon). It prevents slow divergence of real and shadow over long runs.
2. A complexity hallmark (MODES: the most complex persistent component). Our runs report mean replicated size only
   (Hash Chemistry: flat at ~4 after t~500; complex world: pinned at the size cap in the zero-sum arm).
3. An ecology hallmark (MODES: diversity of persistent components). We report top-k turnover, not coexistence.

**Prior art for c30's results.**
- Hash Chemistry freezing after an early radiation is not reported by Sayama (2019), whose evidence is the raw
  cumulative count over 2000 steps; Sayama also shows the biased random control making about 3x more distinct
  multisets than the hash, so the raw count already ranks the control higher. Our 20000-step cohort result is new
  relative to that paper.
- That static fitness landscapes give finite adaptive walks, and that a changing landscape sustains novelty, is
  textbook population genetics; the moving-landscape control is a positive control, not a discovery.
- BFF (Aguera y Arcas et al. 2024) reports long-term differentiation of replicators after the transition ("the soup
  is never dominated by one individual program"); whether that differentiation is adaptive was not measured there.
  c30's BFF finding says: not distinguishable from drift on one seeded soup.

**Suggested next step.** Re-implement census_shadow with Channon's re-synchronisation (start each census interval
from the real census, run g generations of neutral resampling, compare) and re-score evoloop and the BFF soup. Cheap:
analysis only.
