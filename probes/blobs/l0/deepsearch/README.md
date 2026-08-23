# deepsearch — phase 5b: complexity-driven MAP-Elites (l0-deepsearch)

MISSION: does sustained selection FOR the audited interest scalar (metrics_v1)
discover emergent behavior that random/jitter sampling did not?

## Design
- FITNESS: metrics_v1 interest. T=2500 f32 soup screen (truncation-parity
  verified: recompute of gt_m4_s1 truncated -> 24.34 vs certified 24.3).
  T=5000 confirms for cell-winners only.
- ARCHIVE (archive.json): MAP-Elites keyed spp|motion|phase|mem
  (spp = n_species_alive capped 4; motion in {still,drift,mobile,rotor}
  [rotor = winding>=1.5 & parked COM, mirrors C3]; phase = d5 bond phase
  {gas,frozen,liquid,flicker}; mem = realized d6 cover > 1%).
  Cell quality = screen interest; every eval logged in results.json.
- POPULATION g0: 7 ground truths (free battery recomputes of the saved
  complexity/runs/*.npz, truncated to 2500) + 8 elite seeds (engine_10748,
  s2_118_41, uni_3034, s2_128_26, rail_111_17, e1_9508, e1_9513, rh1_7000;
  pred/coex are already GTs) + 20 operators_lib.mutate jitters around all 15.
- OPERATORS: evolve/operators_lib.py mutate + merge (share_chan/cross_edge/
  slow_tanh, post-mut p=.35). Block library GROWS: any elite holding a cell
  for >=2 generations becomes a merge block (gen.py cmd_breed).
- BUDGET: G0 funnel before any soup; size caps n_act<=4, fields<=12.

## Files
ds_lib.py   eval pipeline (funnel->soup->battery), cell key, locked archive
gen.py      init / breed <g> / ingest <g> / confirm [n] / status
worker.py   shard runner (idempotent by (cand, phase))
seeds/      8 elite genomes (json, lib format)
jobs/       g<g>_w{0..3}.json shards
runs/       npz raw runs (screen: *_s.npz, confirm: *_c.npz)
results.json / archive.json / data/state.json

## Loop protocol (per generation)
1. gen.py breed <g>   (24 children: 10 mutate + 14 merge, elites-biased)
2. 4x worker.py jobs/g<g>_w*.json   (parallel, nohup)
3. gen.py ingest <g>  (archive insert + gen stats)
4. every 2-3 gens: gen.py confirm -> run cf shards -> archive_confirm
GATES: loop-validation = archive grows AND >=1 evolved candidate beats its
seeds' interest. Honest null = publishable.
