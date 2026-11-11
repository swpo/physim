# Study A: deviations from the plan, written at the time

Each entry: when, what the plan says, what was done instead, why. `DECLARED.md` is not edited.

1. **11 Nov 2026, 15:35 UTC, at declaration, before any run. The training rule has a cap.** The plan's rule
   ("otherwise the schedule doubles") has no end. With a cosine schedule on 520,000 examples the best
   validation step is usually the last one (round 5: 9 of 9 cells), so the rule may never be met. Done instead:
   at most two doublings of the base nets (6,000 to 24,000 steps), the longest schedule whose cost fits the
   research budget the exam tells the agent (DECLARED R16). If the rule is still unmet there, the nets are
   reported as "not converged by the rule" and every rung is scored, so the reader sees what a doubling moves.
2. **Same time. The training rule for cross-validated fine-tunes is read per group.** A fine-tune whose
   cross-validation curve is flat has its minimum anywhere, so with 96 fine-tunes per budget some would always
   fall in the last 20% and the schedule would double without end. Done instead: the rule is applied to the
   mean curve of each group (DECLARED R16).
3. **Same time. Fewer member-ticks than the plan counts.** The plan's 1.80 million include 17,696 for scales
   and for drawing truths. The block view's scales are public constants and the 8 truths are read from round
   5's file, so those simulations are not run. The 96 items of a world are two exams of 48, each with a
   climatology pool of 48 (DECLARED R2), which leaves the count unchanged.
4. **11 Nov 2026, 15:50 UTC, before any run (the code was not yet complete). Folds and the clock.** Two points
   that DECLARED R8 and R16 leave open were fixed while the job was written. (a) The cross-validation folds
   are stratified by the Lab program class the experimenter chose: episodes are ordered by class and dealt
   round-robin, so that at N = 8 every held-out pair holds two different classes and every training set holds
   every class. Unstratified folds would, one time in four, hold out both episodes of a class. (b) "Only if
   the job's clock allows": a doubling of the fine-tune schedule is made only if, by the presmoke's estimates,
   the stages the plan declares (D at round 5's column, the budgets not yet run) still fit afterwards.
5. **11 Nov 2026, 17:05 UTC. Job ids and one setting, before any run.** The plan allows one GPU job for A; one job
   runs, under its fourth name. `r6-dialsA-001` (16:11 UTC) has a capital letter, which the protocol's id
   pattern forbids: the runner dropped it without a status. `r6-dialsa-001` was rejected at 16:26 before any pod
   ($0): its notes passed 4,000 characters. `r6-dialsa-002` (16:35, notes shortened) was held by the runner's
   review and cancelled by the coordinator before any pod ($0): both trainers dispatch one compiled step per
   Python iteration, and the platform allocator I had set makes such loops about 3.5 times slower on this card
   (r6-foundryexam-002), which by the reviewer's model would have cut N = 32, N = 2, the control and probably
   the 24,000-step rung. `r6-dialsa-003`, pushed by the coordinator at 17:01, is the job that runs: the same
   pinned commit (f38f88ac0), paths, run line, hours and cap, without that allocator setting. No code, size,
   seed or criterion differs between the four requests.
6. **11 Nov 2026, 18:25 UTC, after the job. The base nets are not converged by the plan's rule.** As entry 1
   foresaw, the rule was unmet at every rung and at the cap: best validation steps 22,750 to 24,000 of 24,000.
   Done as declared (R16): the 24,000-step nets are the scored ones, they are reported as "not converged by the
   rule", and all three rungs are scored (s with the true-form net alone 0.247, 0.267, 0.279; sigma at the zero
   point 0.013, 0.015, 0.017). Fine-tunes and D nets met the rule at their first schedule; no doubling of theirs
   was needed and the clock cut nothing. After the results were seen, reported-only numbers were added to
   `make_summary.py` (the science share by budget and by horizon, the cross-validation gain, the counts of chosen
   ridges); no criterion, threshold or pick was touched.
