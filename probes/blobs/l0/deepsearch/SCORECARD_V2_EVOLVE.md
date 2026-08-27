# SCORECARD — l0-evolve-v2 (phase 6: operator/search side, LOCAL VALIDATION DONE)

MISSION: v2 operator alphabet (T1) + assay_v2 handshake (T2/T3) validated locally.
5 gens x 24 run on this laptop: 3 under metrics_v1 (v1-epoch, operator shakedown)
+ bootstrap re-eval + 2 breeding gens under LOCKED assay_v2 (v2 epoch).
THE research question is ANSWERED EARLY: evolution USES minted bilinear vertices.

## T1 headline: minted-vertex uptake (creation rate was structurally ZERO in v1)
- mint_bilin: 15/15 evaluable children ok (no funnel kill, no blowup);
  9 minted vertices FIXED in archive cells across both epochs.
- v2-epoch archive (34 cells): 8 carry minted vertices, ALL 2-seed confirmed.
- g12 GLOBAL BEST among bred children is a mint: ds2g12_005 I2=70.1
  (parent ds2g1_017 64.7, +5.4) — vertex (act2, chan3*chan2) coef -0.23,
  "rand"-bias pick, i.e. a coupling the biased-own heuristic would NOT propose.
- ds2g11_007 (mint on ds3_014, I2=69.5): a SECOND bilinear alongside the
  fossil vertex in the succession world — fossil+minted coexist.
- delete_bilin ablations reproduce the fossil-vertex story in-search:
  g0_jit_11 minus its inherited vertex: 66.5 -> 9.5 (the load-bearing check,
  now an operator, cf. PROGRAM.md ds3_014 deep-dive).
- Vertex census machinery: vtags[] lineage uids on every genome; per-gen
  birth/fixation stats in state_v2.json gen_stats[].census.

## Operator economics (5 local gens, 120 bred screens; both epochs pooled)
| op               | n  | ok | archive events | best I | note |
|------------------|----|----|----------------|--------|------|
| mint_bilin       | 15 | 15 | 8              | 73.7*  | *v1-epoch best rode ds5_003; v2-epoch best 70.1 |
| mutate           | 25 | 21 | 8              | 64.0   | climbs within cells (v1 law holds) |
| merge_cross_edge | 17 | 17 | 12             | 72.3   | still the cell-opener |
| merge_slow_tanh  |  8 |  8 | 3              | 73.8   | low-n, high-ceiling (v1 law holds) |
| add_chan         | 10 |  8 | 4              | 67.9   | 2 archive cells incl. 3|grow|rotor 67.9 |
| dup_act          | 10 |  3 | 1              | 39.5   | WEAK: high funnel-kill (see negatives) |
| delete_bilin     |  6 |  6 | 1              | 65.2   | cheap ablation probe + occasional win |
| merge_share_chan |  6 |  1 | 0              | 52.7   | fragile as ever (same-vacuum law) |
| immigrate        | 25 | 16 | 3              | 32.0   | 3 archive cells = plateau-breaker works; alive-rate 64% after g1 fix |
Gate suite ds2_gates.py 16/16 PASS (vacuum-exactness per op; fossil delete/
restore bit-exact; mint reaches the BFIELD fossil class; dup_act(split,sigma=0)
== share_chan self-merge EXACTLY; merges preserve bilin multiset + vtags;
v1 V1/V2 reconstruction gates still pass).

## Assay_v2 handshake (locked contract, ASSAY_V2_API.md)
- Adapter ds2_lib.evaluate_v2: genome-in run_assay(...), lean horizon logging,
  cell key from pinned fields: sppInt|growth|motion|phase|stages|memgrade.
- Reproduced their numbers through my adapter: m0 2.8, coex 15.6, mv3 52.4
  (their 51.3 s1 at earlier snapshot; traj matches), ds3_014 74.2@T5000-s1.
- Metric-mixing guard: v1-scored and v2-scored rows can never share an archive
  (RuntimeError on insert; archive_v2_v1epoch.json preserved separately).
- SEED2 HORIZON-FAIRNESS FIX (found live): seed2 at default t0=2500 can
  undershoot a seed1 that extended (ds3_014: 74.2 vs 37.1 "fail"). Fix:
  seed2 jobs inherit seed1's T_used as t0 floor -> both false fails flipped
  to confirms (49.5, 45.2). POD RULE: confirm seeds always start at the
  incumbent's T_used.

## v2-epoch trajectory (fresh archive; scores NOT comparable to v1)
| gen | evals | new/imp cells | meanI | maxI | notes |
|-----|-------|---------------|-------|------|-------|
| 10* | 24    | 18/2 (18 cells)| 51.5 | 74.2 | *bootstrap: 7 GT + 17 elites re-scored |
| 11  | 24    | 10/3 (28 cells)| 31.8 | 69.5 | mint takes 3 archive events |
| 12  | 24    | 6/2 (34 cells) | 40.9 | 70.1 | mint = gen-best; 2 immigrant cells |
Descriptor space works as designed: 34 occupied cells span constant/switch/
grow/oscillator x still/drift/mobile/rotor x frozen/liquid/flicker/gas x
s1/s2 x g0/g2. The s2 (2-stage succession) axis has TWO occupants
(ds3_014-class + ds2g11_006 minted-vertex world) — succession is now VISIBLE
and selectable (T2 payoff).

## Cost model (measured, M1 Max under shared load; per candidate incl. battery)
- v1-epoch local screens (fixed T2500 + trend-extend rule): median 927s,
  mean 1178s, 8% extended.
- v2-epoch assay_v2 screens: median 961s, mean 1767s among evaluable
  (mean 1399s per bred candidate incl. funnel rejects at ~0s); T_used dist
  over bred gens: 2500: 74%, 5000: 11%, 10000: 13%, 20000: 3%.
- Extension multiplier vs v1 fixed-screen mean: ~1.5-1.9x (brief guessed ~2x).
- Statics stay cheap (m0 156s, m4 124s, bf 306s, coex 417s).
- seed2 confirms: mean 1508s (horizon-floored).
- Local total spent: ~76 core-h over 217 evals (5 gens + bootstrap + smokes
  + handshakes; excludes gate suite).

## Pod-run spec (controller rents; budget-upgraded per user 2026-02-25)
- pop 96/gen x 25 gens, 20% immigration (config ds2_config.json: mix scales
  4x: mutate 20 | mint 12 | del 4 | add_chan 8 | dup 8 | merge 24 | imm 20).
- 3-seed elite confirmation before block library (seed2+seed3 at t0 floor).
- L192 lane: box_limit-flagged elites get one L=192 confirm/gen (cap 2).
- Long-horizon lane: top-3/gen confirm at cap T=40000.
- Volume: 2400 screens + ~1050 seed2 + ~840 seed3 + 50 L192 + 75 longH
  = ~1985 core-h (M1-core equivalent) — matches controller's ~2000 estimate.
- Fleet 10x16 vCPU nebius @ ~$4/h: 19-25h wall at 0.5-0.65 vCPU efficiency,
  $76-99 (headroom to $250 covers stragglers/reruns; cap chains at 20000
  keep single-candidate worst case ~2.5h).
- Sharding: ds2_gen.py write_shards cost-proxy balancing; workers idempotent
  (skip done cands), results/archive under fcntl locks — pods can share an
  NFS/synced dir or run island-model per pod with archive merge (RECOMMEND
  islands: 10 pods x 2 gens/merge-round, merge = archive union by cell max,
  avoids cross-pod lock traffic).
- Per-gen cost logging: gen_stats[].wall_sim_total (now includes wall_assay).

## Honest negatives / open items
- dup_act is weak so far: 3/10 evaluable (funnel kills: duplicated species
  destabilizes the joint vacuum), 1 low cell. It IS the vvw-topology move
  (G4 proves exactness) — but as a random move it needs either a stability
  pre-check (funnel-in-operator retry) or acceptance that speciation events
  are rare. Kept in mix at reduced weight for the pod run.
- merge_share_chan stays fragile (1/6). Kept at weight 1 as the only
  channel-fusion move; its wins (v1: ds4_023 54.5) justify a lottery ticket.
- g11 mean-I dip (31.8) vs g10 bootstrap (51.5) is composition, not decline:
  bootstrap re-scored PROVEN elites; g11-12 are fresh children incl. dead
  immigrants. Non-immigrant bred means: g11 35.2, g12 42.4 (rising).
- Interest concentration: 8 of top 10 v2-epoch holders are switch|mobile or
  grow|rotor liquid classes; the new axes (stages, memgrade, sppInt) hold
  diversity but a Goodhart watch stays warranted at pod scale.
- 2 gens under assay_v2 is a smoke-scale sample for op-vs-op comparisons;
  pod run is the real experiment (statistical power was never the local goal).
- v1-epoch minted-carrier walls hit 5934s locally (T-extend + 12 fields);
  MAX_FIELDS=14 at pod scale will produce ~2x that worst case per candidate.

## Files (probes/blobs/l0/deepsearch/)
ds2_ops.py (v2 alphabet + vtags), ds2_lib.py (eval/adapter/archive/census),
ds2_gen.py (driver: seed_import|init_full|breed|ingest|ingest2|status),
ds2_worker.py, ds2_gates.py (16 gates), driver2.sh, mon_g10.sh,
ds2_config.json (metrics=v2 live), results_v2.json (187 rows),
archive_v2.json (34 cells, v2 epoch), archive_v2_v1epoch.json (46 cells),
data/state_v2.json (gen stats + census), runs2/ (69 npz, interest>=15 only),
jobs2/ (all shards), init_v2local.py, ds2_handshake*.py, ds2_s2fix.py.
