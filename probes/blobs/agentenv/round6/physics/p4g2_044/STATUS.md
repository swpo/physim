# p4g2_044 / seed 928 physics reconnaissance

Status: COMPLETE — bounded first pass, private evaluator evidence.

Delivered:
- PHYSICS.md: three per-world phenomena, evidence labels, compact tests, gaps,
  and private predictor coverage aligned with the fixed opaque-t0 R6 interface.
- evidence.json: structured claims, source hashes, measured values, caveats.
- Four figures actually viewed: activators_time.png, all_fields_t1700.png,
  native_segments.png, paired_source_fields.png.
- cache_layout.json, first_look.json, measurements.json.
- inspect_cache.py, cache_access.py, first_look.py, measure_fields.py.

Core findings:
1. Existing same-state/RNG u0 source branches have a nonmonotone long-lag
   spot outcome at one anchor; amp2 leaves no extra spot but changes u1 stripes.
2. Duplicated u2/u3 have unequal negative-defect geometry and spatial
   compensation, with shared signed feedback channels of different scales.
3. Gated x7 has local halos missed by home probes; weak cross-group response
   is not globally zero.

All claims distinguish OBSERVED / HYPOTHESIS / NOT YET TESTED.
No new simulations, seeds, ensembles, model calls, or evaluations.
No E1 trace observations were used as measurement inputs. R5 truth is
identified as sensor-only. Legacy branch pairing is not confused with the
current R6 policyA sham/treatment reseeding rule (a root design gate).

Processes: first_look.py completed; it was not rerun. measure_fields.py
completed successfully in 1.45 s. No process is pending; no wakeup needed.
Native thread limit: 1. Cache access: read-only member memmaps, not extraction.
No changes outside this directory and no commits.
Durable scratch reserved: ~/v3work/round6/physics/p4g2_044/ (not needed).
