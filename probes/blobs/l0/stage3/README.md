# L0 stage-3 pod bundle (V4 metrics lock)

Ship this directory (worker.py, lib/, requirements.txt, jobs_*.json) to pods.

17 job shards (priority order):
  jobs_census_00..11.json  P1 kicked-A1 travel census (996 genomes: all alive
                           cell exemplars + onsets + alive candidates; ~83/shard,
                           ~40-120 s/genome -> ~1-2.5 h/shard)
  jobs_island.json         P2 s2_107_48 speed island (33 jobs, ~25 min)
  jobs_plateau_0..2.json   P3 plateau design rule + stacks + mech (11 jobs
                           each, ~40 min/shard)
  jobs_encounter.json      P4 3-flavor encounter tables (6 genomes, ~50 min)

Per pod (4 vCPU -> 4 workers):
  pip install -r requirements.txt
  python worker.py --jobs jobs_census_00.json --out out_census_00.json --smoke  # 2 min check
  nohup python worker.py --jobs jobs_census_00.json --out out_census_00.json &

Fits comfortably in 4x4vCPU x 6h (measured smoke rates). SAVE-AS-YOU-GO:
out files rewritten atomically per job; partial shards usable.
Collect out_*.json back to stage3/ for analysis (analyze.py, controller-side).
