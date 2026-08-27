# deploy/ — deepsearch-v2 island bundle (pod run)

One pod = one island. Each island runs independent generations on the SAME
seed pool; the controller unions archives every ~2 gens and pushes the union
back (breeding pool refresh). Locked assay: metrics_v2/assay_v2/soup_sim_v2
(SHA256 in lib_hashes.txt; verify with `shasum -a 256 -c lib_hashes.txt`).

## Contents
lib/            genome/funnel/sampler/operators_lib/ds2_ops (search stack)
                + metrics_v1/v2, soup_sim/_v2, assay_v2, hier_metrics (assay)
seeds/          40 genomes: v2-epoch archive elites + 7 GTs + champions
                + blk_engine_10748 (block library primitive)
pod_lib.py      eval pipeline (funnel -> assay_v2), archive, ghash dedup
pod_gen.py      init | breed | ingest | ingest2 | ingest3 | status
pod_worker.py   shard runner (idempotent; skips done cands)
pod_run.sh      main loop: ./pod_run.sh <first_gen> <last_gen>
pod_smoke.py    3-candidate smoke (exit 0 = ready)
merge_islands.py  controller: union by cell-max + results concat + push
island_config.template.json

## Per-pod setup (16 vCPU)
    cd deploy
    python3 -m pip install -r requirements.txt   # numpy+scipy only
    shasum -a 256 -c lib_hashes.txt              # verify snapshot (incl. assay lock trio)
    cp island_config.template.json island_config.json
    # EDIT island_config.json: "island": <0..9>  (UNIQUE per pod)
    python3 pod_smoke.py                         # ~10-15 min; must PASS

## Launch (25 gens; gen 0 = seed re-eval bootstrap)
    nohup ./pod_run.sh 0 25 > pod_run.log 2>&1 & disown
Watch:
    tail -f out/driver.log
    python3 pod_gen.py status

## Config notes
- n_workers 14 on a 16-vCPU pod (2 spare for OS+battery spikes);
  assay_workers=1 (FFT threads OFF; parallelism = process-level).
- mix sums to 96 candidates/gen (pop as specced): mutate 20 | mint 12 |
  del 4 | add_chan 8 | dup 8 | merge 24 (12/8/4) | immigrate 20 (~21%).
- rng streams: rng_base + 1000*island + gen -> islands never share streams.
- minted-vertex uids are island-scoped (v<island>_<gen>_<k>): collision-free
  across the fleet by construction.
- seed2/seed3 confirms + lanes inherit t0 = incumbent T_used (the confirm-t0
  rule; see ASSAY_V2_API.md "Multi-seed / confirm runs").
- L192 lane: box_limit-flagged elites, cap 2/gen. LongH lane: top-3 that hit
  T=20000 cap get one cap-40000 confirm.
- Elites enter the BLOCK LIBRARY only with seed2_ok AND seed3_ok (3-seed rule).

## Island merge (controller, every ~2 gens)
Pull each pod's out/archive.json to merged/i<K>_archive.json, then:
    python3 merge_islands.py union merged/i*_archive.json \
        --out merged/union_archive.json \
        --results merged/i*_results.json          # optional concat
    # push back (after copying union to each pod):
    python3 merge_islands.py push merged/union_archive.json <podN_out_dir>...
Union = cell-max winner; losing lineages retained in history (ghash-tagged);
vtags/provenance ride winners verbatim; counts summed; first_gen = min.

## Cost expectations (from local validation, M1-core equiv)
mean bred candidate ~1400s incl. funnel rejects; T_used dist 74% @2500,
11% @5000, 13% @10000, 3% @20000; statics 2-7 min; seed2 ~1500s.
Fleet 10x16 vCPU: ~19-25h wall for 25 gens + confirms + lanes (~2000 core-h).
Single-candidate worst case ~2.5h (cap 20000); LH-lane confirm up to ~5h.

## Output (per pod)
out/results.json   every eval row (lineage, vtags, minted, horizon, ghash)
out/archive.json   MAP-Elites island archive
out/state.json     per-gen stats incl. minted-vertex census
out/runs/*.npz     saved runs for interest >= 25 elites
