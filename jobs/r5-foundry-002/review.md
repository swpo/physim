# Review of r5-foundry-002 (study `foundry`, job 2)

Reviewed by the runner Mac before the job started. Code: `round5/foundry` at ee9648d4e.
Compared with r5-foundry-001 (22134cfd9), which was reviewed in full and ran cleanly in
556 s on an H100. Method: one reviewer, with findings checked by a skeptical second
reviewer, and compile-level checks at full shapes. Local CPU run of `job2.sh` at
`FOUNDRY_SIZE=tiny` with this request's arms: exit 0, FAIL=0.

**Verdict: fine to run. No blocker, major or minor findings.**

## Checked

- **World code unchanged:** `tnca.py`, `screen.py`, `criteria.py` and `vw1` are identical
  to job 1's. `job2.py` imports only `screen`, `tnca` and `vw`, so the changes in `job.py`
  do not run.
- **Memory (compiled at full shapes):**
  - late (2000-tick burn-in, 128 draws): 9.105 GiB, the same as the screen at burn 50. The
    burn scan returns None per tick, and the only 2000-long array is the tick iota (16 KB),
    so nothing accumulates.
  - sigma100: 9.105 GiB.
  - cert (24, no frames): 8.869 GiB.
  - Largest array: 301,989,888 elements (0.14 of 2^31).
  - Peak: about 9.2 GiB, against about 30 GiB on an A100 40GB.
- **Time on an H100:** enrich about 179 s, late at most 411 s, cert about 21 s, sigma010
  and sigma100 about 90 s each. With compiles that is about 14.5 min. Every arm finishes
  before the 3600 s rule unless the GPU is more than about 4.3x slower. The deadline is
  checked before every chunk and every arm, so after 3600 s the longest unit is one late
  chunk plus compile, about 120 s, against the kill at about 4440 s.
- **Halving:** 128 -> 64 -> 32 -> 16 -> 8, then the arm is given up (cert 24 -> 12 -> 6). It
  cannot loop, and the failed arm is recorded.
- **Inputs:** `make_job2_inputs.py` rebuilds `job2_inputs.json` byte for byte from the
  bundled files.
  - late: 2000 unique draws, seed 2026.
  - enrich: 4096 unique draws, seed 2027, 96 enriched per 128 in every chunk; enriched and
    control are disjoint.
  - sigma: draws 0-2047.
  - cert: the 88 candidates.
- **Safety:** no network, subprocess, pickle, eval or credential reads, and writes stay in
  OUT. `FOUNDRY_REQUIRE_GPU` is checked before the inputs are read or anything compiles.
- **Outputs:** about 84 chunk files of about 160 KB each (enrich chunks with thumbnails
  about 1.2 MB), about 13-16 MB in total. `job2_state.json` is written atomically.

## Info

1. The halving fallback catches every exception, not only out-of-memory errors, and each
   arm starts again at the full chunk size. In this run that only costs time.
2. The exit code is 1 after a recovered halving, although `job2.sh` says 0 means every
   arm finished. Read `job2_state.json` (`n_done == n_planned` per arm) rather than the
   exit code.
3. Chunk npz files are written straight to their final names; only `job2_state.json` is
   atomic. Take the chunk list from `job2_state.json`, not from a directory glob.
4. The cert arm re-measures 23 of job 1's 24 certified worlds. Draw 189 is not a
   'candidate', so for the paired check against job 1's eps010 certification, 23 worlds
   overlap.
