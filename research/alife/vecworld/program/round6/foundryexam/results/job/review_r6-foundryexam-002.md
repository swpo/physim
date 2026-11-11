# Review of r6-foundryexam-002 (study `foundryexam`)

Reviewed by the runner Mac while the job was being provisioned. The code is the four request paths at 0b7e392c.

Method:
- four reviewers, one each for GPU memory, time and deadlines, outputs and hygiene, and correctness;
- each minor-or-worse finding re-checked by independent skeptics: two for a major, one for a minor;
- estimates are from the code's shapes plus measured rates in r5-foundry-001 (H100), r5-foundry-002 (H200) and r5-ladder-002 (A100 40GB);
- the job's code was not executed on the Mac.

**Verdict: fine to run. 0 blocker, 0 major, 4 minor.** The minor findings are for the next request. Two would help the summary of this run offline.

## Checked

- **Memory on an A100 40GB.** The largest peak is the 16-net lockstep training step of arm P's C and Cft groups.
  - Temporaries are about 9.1 GiB: input copy buffer 1.83, six hidden copy buffers 5.06, saved activations 1.13, backward buffer 0.84 GiB.
  - Stacked data adds about 1.4 GiB, for about 10.4 GiB in all, roughly a quarter of the card. The notes' "nets 4-6 GiB" is about 2x low, but there is ample room.
  - Cross-check: r5-ladder-002's 8-net step, scaled to 16 nets and this layer mix, gives 9.4 GB.
  - Simulation chunks of 2048 float64 members take 3.0-4.6 GiB, so "about 6 GiB" is a safe upper bound.
  - Largest array: 0.23 of 2^31. No int32 overflow.
  - Data sets are uploaded once per train() call and passed by reference, not duplicated on the device.
  - The presmoke runs the Runner at chunk 2048, and the shape_test runs the exact C-group shape, so a GPU-only blowup would show within minutes.
- **Time.** Setup took 10-35 s in earlier jobs and counts inside max_hours. The kill comes about 194 min after job.sh starts; job.sh's own end (T_END) is at 180 min.
  - Per family on the A100: simulation 41-43M member-ticks at 21-30k/s, 23-34 min; per-world nets 1.11M net-steps at 2.7-3.4 ms, 50-63 min; big nets 22-27 min; presmoke with compiles 10-17 min; CPU work per hidden world 4-10 min.
  - Modelled totals on job.sh's clock: optimistic 2.0 h, central 2.5 h, pessimistic 3.0 h. The notes expect 1.8-2.2 h, which is the optimistic end.
  - In every scenario modelled, the run ends before the kill. In the central case nothing is skipped, with 10-11 min of slack in arms P and N30.
- **Deadlines.** The arms run P, N30, N10 (run_fx.py:80, 544), as DESIGN.md says.
  - The notes' "N10 goes first" is a wording slip; N10 runs last.
  - The 45/27/27 split is recomputed at each arm's start from the time left. P gets 45% of the time left, N30 50% of what is left after P, N10 the rest.
- **Outputs.** About 34 files, at most about 33 MB uncompressed. The largest is full/P/items.npz at at most 10.9 MB. All are inside 50 MB, 20 MB per file and 2000 files.
  - Every JSON and npz file carries PILOT_NEVER_REUSE_AS_EXAM.
  - Each arm's files are written atomically when the arm ends.
- **Hygiene.**
  - The os.urandom secret is never written or logged; only its SHA-256 commitment goes to info.json.
  - No network or subprocess use, and writes stay under OUT.
  - Exit codes are as the notes say: presmoke failure gives 2, any full-pass failure gives 1, and outputs are collected after failure or timeout.
- **Science.**
  - Hidden weights reach only the policies allowed to use them: O, K, C and Cft, and the plug-ins.
  - Lab and exam draw from separate secret namespaces, so no exam future enters a Lab.
  - Arm-P hidden worlds are excluded from training by (seed, index).
  - Neighbour training worlds (j < 1000) and hidden neighbours (j >= 1000) are distinct draws at exactly the stated eps.
  - Scores are averaged with equal weight per item and world.
  - Code paths only the full size takes (n_centres > 1, P0[64], 12- and 16-net D/FT groups, arm-N big nets) were traced; no crash was found. The multi-group N-arm path has still never been executed.

## Minor (for the next request)

1. **If the run is slow, the declared null goes first, and the summary changes sigma's null without saying so.**
   - The D and FT budgets train in ascending order, with D(512) and FT(512) last in every arm (run_fx.py:393-407). They are about 30% of arm P's per-world net-steps.
   - If nets run about 1.3x or more slower than the central estimate, the deadline skips them first. make_summary.py:175 then takes Nmax = 128 and measures sigma against a weaker null than DESIGN.md:93 declares. That biases sigma upward, toward the 0.15 bar.
   - Fix: train D(512) and FT(512) (at least seed 0) right after C, and the P0[16]/P0[64] curve nets last. In make_summary, fix Nmax at 512 and add a null_incomplete flag instead of lowering it.
2. **The platform allocator's cost per training step is unmeasured.** fx_net.py:429-434 dispatches one jitted step per Python iteration: about 215,000 dispatches, 27,700 of them with about 9 GiB of temporaries allocated and freed through CUDA each time.
   - The 2.3-2.8 ms per net-step basis (r5-ladder-002) was measured with the default allocator, and r5-slots-008's "platform costs nothing" ran 100 steps per call.
   - Fix: have the presmoke log steady ms per step for the 16-net and big-net shapes. Run 25-50 steps per dispatch (a scan or fori_loop inside vstep), or use the default allocator: the peak is about 35% of its 0.75 x 40 GiB cap.
   - For this run: compare the first full-pass "step 1000" line with 2.3-2.8 ms per net-step.
3. **A kill or crash late in the run loses more than it needs to.** info.json is written only after the last arm (run_fx.py:556-563), and make_summary needs it (make_summary.py:313).
   - A kill during N10 leaves P and N30 complete on disk, but no info.json, so failed, skipped, clock and config are lost.
   - N10's reference scores, computed long before, are also lost: scores are saved only at the arm's end.
   - Fix: rewrite info.json after the gate and after each arm. Save reference scores per arm right after the hidden-world loop. Add a SIGTERM handler that writes info.json with a killed flag. Let make_summary read arms from their folders when info.json is missing.
4. **Failures are contained per arm, not per world or policy as the notes say.** There is no try around each hidden world (run_fx.py:314-328, 338-341), so one data-dependent error in one of arm P's 16 worlds loses the whole primary arm. Examples: a LinAlgError in ridge_fit's Cholesky (fx_lib.py:392), or an input violation in a Lab.
   - Also, if P0 training fails, scores.npz is written but meta.json is not, and make_summary.load_arm crashes for that arm.
   - The chance is low, because the presmoke runs these stages at full per-world size on 3 worlds.
   - Fix: wrap each hidden world (drop it, record it in FAILED) and each lock group. Write meta.json before quick_report.

## Notes

- Code standardisation (st_norm) is computed from the first 64 gate-passing pool worlds. By the CPU gate pass rate, about 3 of those are arm-P hidden worlds, each contributing 8 windows to the mean and SD of the 33 statistics. Better: compute the norm after arm_groups, without arm-P hidden worlds.
- In training mode "random" (fx_net.py:241-247), an amortised net's context can include the example's own target window. The chance is 1/128 per drawn window, about 0.6% of the context weight. The Lab never does this at test. Masking that episode removes it.
- S(N) at N >= 128 is scored with context means cleaner than any it was trained on: about 111 distinct windows at most. A flattening S(N) lowers rho. Report rho at N = 32 next to the N = 512 value, and state the training range.
- In arm P, the P0[16]/P0[64] curve nets train before C, Cft and the D/FT groups. Unlike the lockstep groups, they have no deadline check before starting. Also, fx_net.convergence clamps its index, so a net cut short can still be marked converged. It should return None when the history ends before 0.8 x steps.
- The presmoke runs with STRICT, so a gate skip in it (not a code bug) aborts the whole job with exit 2. By the CPU gate check the presmoke's N30 group should pass. Next time, treat presmoke gate skips as warnings.
- The heartbeat shows only job.sh's few lines from progress.txt; live progress is in run.log.
