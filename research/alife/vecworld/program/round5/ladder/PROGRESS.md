# ladder study: progress (kept current; a container restart may kill the agent at any time)

- 2026-11-10 01:14 UTC. Third instance of this study (container restarts at 00:12, 00:53, 01:12).
  Code by the earlier instance committed as work in progress (34c3f221d). No GPU job submitted yet.
- 01:22 UTC. CPU smoke of run_ladder.py (old sizes) got through stages A-G for n=4 without error.
  Edits since: sizes cut to fit about 2 h on an H200 (r4-sbi-002 stage timings: 1,080-1,290 member-ticks/s,
  exams 520/s): 8 truths, 36 items, N_theta {1: 256, 4: 448, 8: 512}, N_v {1: 128, 4: 512, 8: 512}, 32 class-e
  Lab episodes; net steps adapt to a time share per view (ladder_net.train_nets time_budget); the time left is
  shared by the remaining sets; PM and the state-given plug-in at the prior mean under p_v; pilot marker in
  every output file.
- Next step: run `run_ladder.py --smoke --cpu-ok` and `make_summary.py --smoke` from a git archive of the
  request's paths at the committed revision; update the request file (max_hours 2.65, script --max-hours
  2.35, cap 6.69 x 2.9 = $19.40); commit + push the request r5-ladder-001.json; start a watcher.
