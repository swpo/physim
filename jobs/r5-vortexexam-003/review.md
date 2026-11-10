# Review of r5-vortexexam-003 (study `vortexexam`, job 2)

Reviewed by the runner Mac before the job started. Code: `round5/vortexexam` and
`round5/agentenv/evaluator` at 84550bc04. Method: three reviewers (gate, secrecy and
safety; resources and time; correctness), each finding checked by a second, skeptical
reviewer. Local CPU runs passed: `job2.py --smoke` and `job1.py --scan-only --smoke`
(exit 0). Without `--smoke`, job2 stops at the GPU assert on CPU.

**Verdict: the gate is met and the job is fine to run. One major issue: the closing scan
always shrinks to its smallest design (3 members, one anchor).**

## Gate (met)

- GPU backend: `job2.py:241-242` asserts it before any GPU-scale work; only imports,
  argument parsing and INFO run before it. `--smoke` is the only bypass.
  `job1.py:125-126` does the same for `--scan-only`.
- Output size: every write is atomic. At the largest preset (xl) no file can approach
  19 MiB: the largest are the `design_S_*` parts at about 5.8 MB raw each. job2 totals
  about 30 MB raw at most, and the scan adds about 1.5 MB at J=3 (6.2 MB at J=12). The
  audit cap of 40 MiB plus the scan stays under the 50 MB per-job limit.

## Exam secrecy (clean)

- The 256-bit secret comes from `os.urandom`. `__repr__` prints only part of the
  commitment, and `hex()` is never called.
- A run with the secret patched to a known value found it in no output, stdout or
  stderr, including on a forced failure path that writes a traceback.
- Only the commitment is written, to `info.json` and `truths.json`.
- Truths, exam classes, and the Lab and exam keys come from separate secret-rng
  namespaces, and no derived key is stored.
- Of `agentenv/evaluator`, only `__init__.py` (a docstring) and `acceptance.py` (numpy)
  are imported. `lab_service`, `sandbox`, `grader`, `instance`, `build_workspace` and
  `submission` never are.
- Nothing reads secret material from the bundle, the environment or files.

## Major

1. **The `--scan-only` run always falls back to J=3 and one anchor.** In scan-only mode the
   rate table is a single row at B=bmax=1024 (`job1.py:399`). `rate_at` (`job1.py:216-228`)
   scales the rate linearly for every batch below that row, so `est()` (`job1.py:303-306`)
   prices the main run at about 409600/rate seconds for every J.
   - At job 2's own rate (about 444 member-ticks/s on the H200) the estimate is
     1107-1229 s against a budget of about 800 s. Nothing fits, and the code keeps the
     fallback J=3, anchors [200] (`job1.py:307-315`). It logs 'est ~1107s of ~805s' and
     runs anyway.
   - J=4 needs a rate of at least about 611, J=12 with both anchors about 800.
   - With job 1's real bench rows (374/425/444 at B=64/256/1024) the same logic picks
     J=12 with anchors [200, 320] at an estimated 676 s, and job 1's actual scan took 708 s.
   - Consequence: the headroom scan covers 3 members per setting at anchor 200 only,
     instead of job 1's J=12 with 2 anchors. The level-1 scores are much noisier: es_k1
     has 2 other members. Time and cost are not at risk; the scan just finishes early.
   - Fix: pass job 1's bench rows (or a flat-rate row at B=64) in scan-only mode, or pass
     J and the anchors explicitly. A later scan-only job (about 15 min) can redo it.

## Info

2. The pilot marker sits only in `info.json` and `truths.json`. `exam.npz`, `items.npz`,
   `lab.npz`, `lab.json`, `identification.json`, `posterior_draws.npz`, `scores.npz` and
   `prediction.json` hold truths, Lab episodes or exam answers without it. Add a
   `PILOT_NEVER_REUSE_AS_EXAM` entry so a copied file cannot be mistaken for a real exam.
3. The 20 MB limit holds by construction (array shapes), not by a check at write time.
   `audit_outputs` runs only at the end of a normal run, and it deletes oversized files
   rather than refusing them, then still exits 0.
4. An out-of-memory error in the episode or exam stage ends job 2 instead of degrading it.
   This is not expected here: the peak is about 10 GB at BMAX=1024 on any card, so A100
   40GB is enough.
5. If the final report (stage H) fails, job2 still exits 0. Too few viable truths abort
   the job before any design output is saved.
6. `track1/vortex_world/_paths.py:10` puts the fixed path `/home/user/evalwork/vecworld/vw1`
   at `sys.path[0]`. That is harmless while that directory doesn't exist on the pod, and
   `vw` itself is protected by `vxlib.py:51`.

## Resources and time (checked)

- Largest device array: about 168 million elements. Largest array in CPU memory: about
  90 million. All are at most 8% of 2^31.
- Peak device memory is about 10 GB at the largest preset.
- No large device array is captured as a jit constant: the 8.4 MB stirring basis is
  passed as an argument.
- Presets by measured rate: xl at 383 member-ticks/s or more (1,735,168 member-ticks,
  about 1.1 h of simulation at 444/s).
- Estimated xl timeline: about 1.5 h. Deadlines end at about 8880 s, against the
  9720 s kill.
- The turnover fix (carried across chunk borders) is correct.
