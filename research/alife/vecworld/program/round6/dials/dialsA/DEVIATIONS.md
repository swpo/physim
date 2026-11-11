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
