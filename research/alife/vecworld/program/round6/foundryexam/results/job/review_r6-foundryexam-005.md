# Review of r6-foundryexam-005 (study `foundryexam`, last job)

Reviewed by the runner Mac as the job started. The code is the four request paths at 94451e27.

Method:
- two reviewers: one checked the run risk at 16,384 episodes per world, the other the correctness of the changes since r6-foundryexam-004 (1e9acab5);
- each minor-or-worse finding re-checked by an independent skeptic;
- timings from 003's finished run and 004's live log on this card;
- the job's code was not executed on the Mac.

**Verdict: fine to run. 0 blocker, 0 major, 3 minor.** All three minor findings are about reporting and can be fixed offline after the run.

## Checked

- **Device memory.**
  - The Cbig stack: X (8, 16384, 33, 8, 8, 3) is 8.30e8 elements (3.09 GiB), CU and CtU 4.13 GiB together, tr 76 MB, 7.2 GiB in all. Every array is asserted below 2^31.
  - C's and Cbig's stacks never coexist on the device: each training call builds and drops its own.
  - The 8-net batch-128 step is 1.13e8 elements under check_elems, half of C's 16-net step that already ran in 004. Peak is about 12.5 GiB of about 39.5 GiB.
  - No index passes 8.3e8.
  - shape_test trains the exact Cbig shape about 3 min in, so an out-of-memory error would cost about $0.15.
- **CPU-side memory.** Simulation buffers 6.64 GB plus 4.29 GB (the notes' "GiB" are GB), per-world data sets 20.6 GB; peak about 35 GB against about 216 GB of RAM on the machine.
- **Time.** 128 simulation chunks at 16.25 s (35 min); Cbig 2 x 24,000 steps at about 20 ms (16 min); C about 10 min. Arm P about 89-93 min, the job about 1.65-1.8 h against job.sh's 2.5 h and the 2.75 h kill; about $4.
  - Cbig comes right after C, so a slow run keeps it. It is cut only at a uniform slowdown of about 1.66x.
- **Changes.**
  - The data are nested: C takes the first 4,096 rows of each world's 16,384, Csm the first 1,024, Cbig all of them, with classes shuffled before slicing.
  - Cbig runs 24,000 steps at batch 128 in two lock groups of 8, with one seed per world, none shared with another net.
  - FX_SEED_OFFSET = 2000 applies at every training call, and the noise secret is fresh.
  - The arm-P-only wiring is correct in job.sh and run_fx.py, and every downstream script iterates only the arms present.
  - Cbig is in the speed projection and is scored as Cbig|s0. C, Csm and Cbig are scored on the same 512 items with the same sample seed, so the curve is paired item by item.
- **Outputs.** About 9-10 MB. Exit codes are as in 004.

## Minor (fix offline before the write-up)

1. **Cbig gets fewer passes over its data than C, and its convergence is not shown where the curve is read.**
   - Passes: C 8,000 x 128 / 199,044 rows = 5.14, Cbig 24,000 x 128 / 796,284 = 3.86, Csm 20.6. In 003, at 3.43 passes, only 4 of 32 C nets converged by criterion 6.
   - make_summary renames the score keys but not the train_info families (make_summary.py:143-153 versus 283-299). tables.py:94 has no "Cbig" or "Cmid" kind, so the convergence table can show a converged "C" that is really the 4,096-episode net.
   - Before quoting the curve, read analysis convergence["P Cbig"] (ok / nets, late_share_max, best_step_median against 24,000). If Cbig fails criterion 6 or its best step falls in the last fifth, keep C a lower bound whatever the last step is.
2. **The declared C(1,024) / C(4,096) / C(16,384) curve and its 0.01 verdict are computed nowhere.**
   - DESIGN.md 5d (lines 167-169) promises the curve and a verdict on whether the last step is above 0.01.
   - make_summary only adds gap pairs (lines 229-232), and which pair carries the last step depends on which net won the ceiling.
     - If Cbig wins, the last step is C - Cmid.
     - If the 4,096 scratch net wins, it is C - Cbig with the sign reversed.
     - If Cft wins, no pair compares Cbig with the scratch net.
   - tables.py:69 labels C - Csm "convergence of C in data", which is two steps when Cbig wins.
   - Add an explicit c_curve block keyed by the original net names, with each net's OES, the two step gaps from the same world bootstrap, and the verdict. The underlying curve is sound.
3. **"Three independent repeats" of arm P share the same training simulations and plug-in weights.**
   - The agent's training simulations use the fixed seed 1000 + 100 x ai + gi (run_fx.py:349), and the plug-in perturbations use fixed seeds (run_fx.py:278).
   - So P0, P0s, A and the P0[n] curve train on bit-identical data in 003, 004 and 005. Only net seeds, items, Labs and the noise secret change.
   - The spread across the three understates between-run variability. Word it as "repeats with new items, Labs and net seeds on fixed training simulations".

## Notes

- **If the run is slow, Csm (the curve's 1,024 point) is cut before Cbig.** The plan order is C, Cbig, D(512), FT(512), Cft, Csm, then the rest. At expected speed nothing is cut; the P0[n] curve goes at about 1.37x, Csm at about 1.45x, Cbig at about 1.66x.
  - The speed guard stops the job only when nets are about 2.6x slower.
  - If Csm was cut, take the 1,024 point from 004 and say so. A skipped Cbig group removes Cbig from scores.npz entirely.
- **The validation splits of C, Csm and Cbig are drawn independently.** Read the curve from the exam-scored gaps, not from validation losses.
- **The job's own quick report ignores Cbig as a ceiling candidate.** Quote make_summary's numbers.
