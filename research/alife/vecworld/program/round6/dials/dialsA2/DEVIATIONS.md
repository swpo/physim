# Study dialsA2: deviations from the task and the plan, written at the time

Each entry: when, what the task or plan says, what was done instead, why. `DECLARED.md` is not edited.

1. **11 Nov 2026, 19:26 UTC (commit 3fd4076c5), at declaration, before any run. The whole exam is not re-sat.** The task asks to
   report "the whole-exam numbers beside the triggered ones". The exam of this study is built from the triggered
   items only (the lead's choice), so its nets are trained on the triggered mix at horizons 8, 12 and 16 and cannot
   be scored on none or blind items or at 1, 2 and 4 ticks without a second set of base nets. Done instead (nearest
   thing, DECLARED R19): study A's whole-exam numbers (all four classes, horizons 1 to 16, 8 truths, job
   r6-dialsa-003) are quoted beside this study's with their source, and this study reports its own numbers per
   class and per horizon.
2. **11 Nov 2026, 19:40 UTC, before any run. A wrong clock time in DECLARED.md's header.** The header says "about
   19:50 UTC"; the file was committed at 19:26:12 UTC (commit 3fd4076c5), before any code of this study existed (the
   first code commit is 0b5617736 at 19:33 UTC). The commit time is the record; DECLARED.md is not edited.
3. **11 Nov 2026, 20:50 UTC, job r6-dialsa2-001 running, no result seen. The runner's review (3 minor) and what follows
   from it.** (a) DECLARED R11 says each kind of widening of the fine-tune grid (doubled steps, a smaller rate) may
   happen at most twice; the code caps the widening rounds of a group at two in all (`cfg["ft_widen"]`), so a group
   that doubles its steps and then needs a smaller rate, or the reverse, can be left short of R11's grid. Any group so
   left is reported "not interior" in the job's notes and in `results/summary.json` [training.ft]; it is not rerun.
   (b) The speed guard's projection of D(N) is 5 to 12 times too large (compile time scaled by the world count), so
   the clock checks before a base-net doubling, N = 32 and the eta 1/2 arm reserve too much; if one of them is cut,
   that cut is the guard's error, not the declared priority, and is listed here after the job. (c) If a D(N) group
   is stopped by the deadline, the doubling can retrain it briefly and overwrite Dnet(N); `stopped_early` of every
   D group is read before Dnet is quoted. The code is not changed while the job runs.
4. **12 Nov 2026, 00:05 UTC, after the job. What the clock and the review's points did.** Nothing was cut: every stage
   ran, including N = 32 and the eta 1/2 arm (the guard's oversized D estimate, entry 3b, did not bind). No fine-tune
   group needed both kinds of widening (entry 3a): CFT at N = 8 and at eta 2 added one rate, FT at N = 32, eta 0
   doubled its steps once, and every group's pick is interior. No D group was stopped by the deadline (entry 3c).
   The base nets met the rule at 192,000 steps, the declared maximum. The zero point missed (README); its diagnosis
   (`make_summary.py` [diagnosis_after_results]) was written after the results were seen and is reported only; no
   criterion, threshold or reading was changed, and no second job was requested (DECLARED R20 allows one only for a
   failure or the clock).
