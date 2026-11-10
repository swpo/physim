# PROGRESS (study slots, round 5) -- kept for restarts

Updated 09:25 UTC 10 Nov (instance 4). STATUS: FINISHED. Nothing is running; nothing is queued.

## Done
- r5-slots-001 cancelled, r5-slots-002 infra_error ($0), r5-slots-003 pilot done ($3.13, H200, ref e5d146ef3).
- Review fixes e139c34f3; post-pilot changes and the pilot's outputs 7099a0ded (the code ref of every later job).
- Tiny end-to-end run of job.sh on CPU from a git archive of 7099a0ded: 14 configs, 124 halves, EXIT 0, FAIL=0.
- r5-slots-004 (full size, 80 GB cards only): no card for over two hours, cancelled before start ($0).
  r5-slots-005 / 006 (48 trajectories per half, 40 GB card allowed): cancelled before start ($0; memory fraction,
  then a cap 7 cents short of the only rentable offer).
- r5-slots-007 (A100_40GB): failed, $1.04: references and sam_sup, then 13 configs out of GPU memory (BFC pool
  could not supply a second 17-19 GiB block at 17% use).
- r5-slots-008 (A100_40GB, same ref, XLA_PYTHON_CLIENT_ALLOCATOR=platform, 3000 steps): 13 of 14 configs trained
  in full, 116 halves certified, $5.36. Its exit code is 1 only because the table printer met null objective values
  (collapsed code readouts); combined.json is complete, table.txt was rendered locally.
- Analysis: results/interpretation.json (9 claims), results/summary.json (ssummary.py results r5-slots-008
  r5-slots-003 r5-slots-007 r5-slots-001 r5-slots-002 r5-slots-004 r5-slots-005 r5-slots-006), results/figs/,
  README.md. Billed in total $9.52 of $25.
- Local fixes after the job (not in any job's ref): scombine.py (null-safe table, --table mode), ssummary.py
  (null-safe means, claim refs into other job files, pod hours and totals), sfigs.py (null-safe), stable.py (new).

## Next step
None for this study. If someone continues: the proposed follow-ups and their cost are in the report (a parsimony
term on the number of present slots; the same grid on the membrane world). On a 40 GB card keep
XLA_PYTHON_CLIENT_ALLOCATOR=platform; validation needs about 18 GiB at this size.
