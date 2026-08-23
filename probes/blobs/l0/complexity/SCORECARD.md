# SCORECARD — l0-metrics (phase 5 complexity assay battery)

## Deliverables (all in probes/blobs/l0/complexity/)
- soup_sim.py      S1 soup simulator (locked protocol; genome.py numerics verbatim;
                   f32+scipy-fft, 1.4x faster; blob_list parity 1e-14)
- soup_assay.py    driver CLI (world -> run -> battery -> results.json row)
- worlds.py        7 ground-truth builders (M0/M4/XV/BFIELD refs, stage-3
                   encounter genomes s2_101_58 + s2_116_46, machinev3 mimic-0.6)
- metrics_v1.py    LOCKED battery: d1-d6 + C1-C7 + interest scalar
- metrics_dev.py   dev copy (edit HERE for v2; v1 is frozen)
- recompute.py     uniform re-scoring from saved runs
- aggregate.py     table/rank printer
- VALIDATION.md    ground-truth table (21 runs), rank, disagreements, limits
- results.json     append-only log (smoke, parity, all assay rows, final row)
- v1_scores_all.json / v1_scores_T2500.json, runs/*.npz (21 raw runs), strips/

## Validation verdict
Required ordering a << b,c < d,e,g: SATISFIED on 3 seeds (seed 3 out-of-sample
after metric lock). Means: m0 3.1 << coex 23.2 < m4 28.2 < xv 35.4 < bf 39.7
~ pred 40.7 < mv3 42.9. No seed overlap between {b,c} and {d,e,g} groups.
T=2500 truncation preserves ordering -> cheap screening mode available.
f32/f64 parity: rank-stable (max component delta 0.15 at T=800).

## Key design decisions (for the search phase)
1. Interest scalar = weighted sum of 7 graded components; alive-gate n_end>=2.
   Lexicographic alternative rejected: graded C4 (log-tent churn) was needed
   anyway to kill a frozen/liquid knife-edge; after that the weighted sum is
   stable.
2. Winding scan (d5) is THE rotor detector: max angular range over sustained
   bonds + parked-COM condition. ACF alone missed rotors that flip direction.
3. Amplitude gates before ACF: without them, frozen worlds win C2 via
   numerically-tiny fluctuations (m0 scored 0.52 C2 from bond-count flicker
   at the cutoff radius; hysteresis + floors fixed it).
4. d6 memory measures REALIZED structure (cover/elong/persistence of the
   slow field), not genome architecture — pred's tanh channel qualifies, and
   that is correct: it builds real 7x-persistent spatial structure.
5. coex < m4 is a finding, not a bug: static 3-species coexistence has no
   dynamics; if the search wants coexistence, gate on n_species_alive.

## Costs (M1 Max, solo run)
T=5000 soup: 3-11 min/world (3-9 fields); T=2500: 1.5-5.6 min. Battery ~20s.
7 worlds x 1 seed parallel (7 procs): ~35 min wall for the heaviest batch.

## What is NOT certified
- No new physics claimed; ground truths are prior certified/screened worlds.
- Battery tested on 12-blob soups at L=128; different densities may need
  re-calibrated churn/turnover normalizations.
- Search launch is gated on parent review of VALIDATION.md.
