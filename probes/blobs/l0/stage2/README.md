# L0 stage-2 pod bundle (V3 metrics lock)

Ship this whole directory (worker.py, lib/, requirements.txt) to each pod.

Per pod (4 vCPU -> run 4 workers, distinct shard seeds):
  pip install -r requirements.txt          # numpy+scipy only
  python worker.py --shard-seed 42 --n 10 --smoke   # ~2-5 min sanity
  nohup python worker.py --shard-seed 42 --n 100 --out shard_42.json &

- Deterministic per shard seed; SAVE-AS-YOU-GO (shard file rewritten atomically
  after every candidate — a killed pod loses nothing done so far).
- Mix: 60% jitter (5 refs + 2 stage-1 elites builtin; add evolver elites via
  --elites elites.json = [{"name":..., "genome":...}]), 40% uniform.
- Budget (measured, V3.1): jitter-heavy shard 98 s/cand (6-cand full-battery
  smoke); 60/40 mix ~ 100-110 s/cand => 100-cand shard ~ 3 h/core.
  25 shards over 8x4vCPU (32 workers) ~ 3-4 h wall.
- Collect shard_*.json back to controller; merge:
  python merge_shards.py 'shard_*.json'
  -> merged_results.json / merged_archive.json (+dedup by genome hash).
