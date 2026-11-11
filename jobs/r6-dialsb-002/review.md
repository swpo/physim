# Review of r6-dialsb-001 (study `dialsB`, stage 0; applies to r6-dialsb-002)

Reviewed by the runner Mac. The code is the five request paths at 52ae6e40. r6-dialsb-002 runs the same commit, with S0_NPROC=16 added, so this review covers it too.

Method:
- two reviewers: one checked the run risk on a 16-vCPU, 64 GB VM, the other the correctness against DECLARED.md;
- each minor-or-worse finding re-checked by an independent skeptic;
- the job's code was not executed on the Mac.

**What actually stopped 001, which this review missed.** job.sh:11 exports OMP_NUM_THREADS=1, and job.sh:14 then sets NPROC="${S0_NPROC:-$(nproc)}". GNU nproc honours OMP_NUM_THREADS, so it answered 1 on the 16-vCPU machine. The speed guard then projected one process (20,762 s against 9,000 s) and stopped the job at exit 3, for $0.04. The reviewers read nproc as 16. 002 sets S0_NPROC=16, which fixes it; next time compute NPROC before the export, or use nproc --all.

**Verdict for 002: fine to run. 0 blocker, 0 major, 3 minor.** One minor finding (item 3) is about the runner Mac itself, and is fixed there.

## Checked

- **Work and time.**
  - Planned 5,822,544 member-ticks: gate 16 x 324,448, scan C 350,688, scan V 280,688. The alignment check adds 80,736.
  - At 430/s that is 3.76 CPU-hours; 002's presmoke measured 672/s per process once compiled.
  - The guard's projection matches the critical path (alignment plus one gate process, about 405k ticks per process). At half efficiency the job takes about 52 min, against job.sh's 10,800 s and the runner's 3.5 h.
- **Memory.** lax.map over 48-member chunks, one member at a time. The largest arrays (A_act inputs 164 MB, level-1 output 65 MB) put each process near 1 GB, so 16 processes need about 16-20 GB of 64 GB.
- **Outputs.** About 150 small files, far under 5 MB.
- **Exit codes as stated:** presmoke 2, speed guard 3, a failed phase 4, deadline before a phase 5.
- **Hygiene.** No network or subprocess use in s0.py or its imports, and BLAS is held to one thread.
- **Correctness against DECLARED.md.**
  - The ranges rule is as declared: the longest admissible run containing the centre, with the declared admissibility thresholds, scan V's viability tests, and ranges.json fixed with its SHA-256 printed before the gate and checked by every gate process.
  - Truths are drawn with default_rng([20261111, seed]).
  - The main and control arms differ only in cat.
  - G2/G3 match gvh.py; A_act uses the 39-point grid with common random numbers.
  - G* is chosen by leave-one-episode-out on the Lab.
  - H uses Sobol plus the refined box (72 points).
  - The stand-in and the verdict contrast are as declared.

## Minor

1. **One core per process is not enforced, and the speed guard cannot see contention.**
   - XLA_FLAGS at job.sh:12 has a second token, intra_op_parallelism_threads=1, without "--". XLA's parser stops at it, so it is silently dropped.
   - The first flag makes Eigen single-threaded, but nothing caps JAX's CPU thread pool (sized to all 16 CPUs in every process) or the 16 concurrent compiles. Nothing pins processes to cores either.
   - The guard times one process running alone. The margin is wide (about 52 min expected against 3 h), so this run is fine.
   - Next time: pin each worker with taskset through xargs --process-slot-var, drop the dead token, and log CPU time next to wall time in the presmoke.
2. **The gate saves nothing until each process ends, and one failed gate process prevents the analysis.**
   - Each gate process writes its npz and json only at the end (s0.py:593-598).
   - One non-zero exit makes xargs return 123, so job.sh dies with code 4 and never runs analyse. analyse() also loads every (arm, seed) file unconditionally (s0.py:885-888).
   - Next time: save partial results after A_act and H (atomically), run analyse even when the gate phase fails, and declare a rule for missing seeds.
3. **Scan V file names differ only by case, and the runner Mac's file system ignores case.**
   - V_PARAMS has both "DK"/"dK" and "DL"/"dL" (s0.py:62), and files are written to scan/V_{name}_x{factor}.json (s0.py:681, 717). That makes 8 of the 53 scan files pairs that differ only by case.
   - On the pod they are distinct, so ranges.json, its hash and the gate are correct. But when the Mac unpacked the outputs, the second file of each pair overwrote the first.
   - **Fixed on the runner:** a collected file whose name collides that way is now stored separately (manifest: stored_as), and each published path gets its own bytes. 002's outputs are re-extracted from the kept archive with the fix before publishing.
   - Next time: use case-distinct names anyway, for example a numeric index prefix.

## Notes

- The noise keys are the same in every seed and arm. DECLARED.md says the random numbers live inside the seed, so this is worth a sentence in the write-up.
- In the control arm, C3 also tests whether A_act's fixed grid covers the drawn truth.
- Per-horizon reporting is narrower than DECLARED 2.4 lists.
- scipy==1.18.1 is a new pin (earlier jobs used 1.18.0). 001's setup installed it without error.
- On a runner cancel, timeout's process group keeps the Python workers out of the runner's group kill until the pod is terminated. A collect taken at that moment could catch a half-written npz. Write npz atomically next time.
