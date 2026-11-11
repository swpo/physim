# PROGRESS crit_cost (cost and feasibility reviewer, round 6 dials)

- 11 Nov: worktree created, folder made. Next: read program README, DECISIONS, ROADMAP 1+3, round-5 cost numbers, the three designs.
- Read README, DECISIONS, ROADMAP 1+3, gpu/LEDGER.md, crit_stats. Measured rates collected (sources):
  - gliders, A100 40GB: 1,312 member-ticks/s in the ladder harness (r5-ladder-002 progress.txt: n=4 design
    629,760 member-ticks in 480 s; Lab 424,960 in 323 s); 617-734 in bias2 gliders_w and r6-cards (card.md sec. 9: 687).
    Ladder all-in: 3,650,912 member-ticks in 1.2146 h of script, $2.5555 billed = $0.70 per million.
  - membrane 128 px, 20 substeps/tick, tracker on, A100 40GB: 7,091 member-ticks/s (round6/cards/results/cards/membrane/card.md sec. 9);
    bias2 membrane_w 598-2,717 is batch 64 with host transfer of float64 fields.
  - fed vortices 128 px: 169.4 (A100 40GB, r5-vortexexam-006), 444 (H200); 64 px: 1,388-1,577 on the H200; on the A100 40GB only
    r6-cards vortex64: 209. 32 px: not measured anywhere.
  - pilot B stored: design.npz holds no series; the design series are design_S_00/01.npz (512 x 405 x 14 float16 each).
- Next: recompute the three designs' member-ticks, caps, budgets; what must be built; write CRITIQUE.md (< 900 words).
- net_cpu_cost.py run (one thread, about 1 CPU-minute): the ladder's block-view training step costs 0.98 CPU-s; a 6,000-step conditioned net
  = 1.63 CPU-hours = 476 gliders episode equivalents (results/net_cpu_cost.json).
- recompute.py run: member-ticks, hours, dollars, caps, budgets of the three designs (results/recompute.json). Designers' member-tick
  arithmetic holds in all three; differences are in rates (membrane much cheaper than the designer's bracket; vortex 64/32 px unmeasured on the A100),
  in budgets that the reference policies do not fit (defect_gliders H; compute_limit pooled designs) and in what the port can meter.
- Next: CRITIQUE.md (< 900 words), commit, push, remove worktree and scratch.
- DONE: CRITIQUE.md written (897 words by wc -w). Files: CRITIQUE.md, recompute.py -> results/recompute.json, net_cpu_cost.py -> results/net_cpu_cost.json.
  Worktree and scratch removed after the push.
