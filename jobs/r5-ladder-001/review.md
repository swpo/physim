# Review of r5-ladder-001 (study `ladder`, exam side)

Reviewed by the runner Mac before the job started. Code: `round5/ladder` plus the bundled
`track2/gliders_exam`, `track2/actuation`, `round4/sbi`, `agentenv/evaluator` and `vw1` at
a92093604. Method: three reviewers (secrecy and safety; resources and time; correctness),
each finding checked by a second, skeptical reviewer, with compile-level size checks.
The local CPU presmoke (`--smoke --sets 8 --cpu-ok`) passed. Without `--cpu-ok` it stops
with "no GPU backend".

**Verdict: NOT STARTED. The job is rejected until the validation pass is chunked
(finding 1, the same class as the r5-bias2-001 cancel). Secrecy is clean.**

## Major (must fix before running)

1. **The full-size block-view D(N) validation builds arrays past 2^31 elements.**
   - Where: `eval_one` (`ladder_net.py:314-320`) runs every validation row
     (`Cfg.N_VAL` = 1024, `:50`) with 8 noise draws, so 8192 samples per net, vmapped
     over all nets of the group in lockstep (`:321-323`). For the block view's D group 1
     (`run_ladder.py:451-462`: budgets 128 and 512 x 8 truths, so 16 nets), the im2col of
     `_conv` (`:186-191`, nine rolled copies) gives:
     - hidden conv: `f32[16,8192,8,8,432]` = 3,623.9M elements (1.69 x 2^31, 13.5 GiB)
     - input conv: `f32[16,8192,8,8,333]` = 2,793.4M elements (1.30 x 2^31, 10.4 GiB)
   - Size and memory: confirmed by two reviewers with make_jaxpr and a CPU compile at full
     shapes. CPU `memory_analysis` gives 34.5 GiB of eval temp. A single-gather rewrite (a
     stand-in for GPU fusion) still gives 22.5 GiB. The A100 40GB, which this request
     allows, has about 30 GiB usable at the default 75% fraction.
   - Not caught: the requester's "largest tensor about 1.4 GB" counts only the group-0
     training step. The guard at `ladder_net.py:137-138` checks only the dataset
     arguments, and neither smoke nor presmoke reaches full-size validation.
   - When: the first `veval` runs at step 250 of the block view's D group-1 training
     (`ladder_net.py:365-366`). Block is the first view of every set.
   - If it fails (OOM, or a 32-bit index past 2^31): the exception leaves `stage_predict`,
     which has no per-view guard (finding 2). The set then loses all three views: no
     `scores.npz` and no `prediction.json`. The same shapes recur in sets 8 and 1, so the
     whole K / D(N) / P0 / S(N) / C / O ladder would be lost. Only prior, truths, Lab and
     identification outputs would survive.
   - Fix: evaluate validation in chunks (e.g. `lax.map` over row blocks of 512-1024
     samples, or one net at a time instead of vmapping the whole group), or compute the
     3x3 conv without materialising the 9xC im2col (`lax.conv_general_dilated`). Then extend
     the size guard to the eval shapes (net count x N_VAL x draws x 8 x 8 x 9C), or check
     the lowered program's result types.

## Minor

2. **No failure isolation in the prediction stage.** One exception in a view's net
   training or eval (OOM included) loses the set's remaining views and its report:
   `run_ladder.py:427-497`, `run_set` `:558-560`. `report()` is all-or-nothing
   (`:519`). Catch per view and per group, write what was scored, and record the failure.
3. **`progress.txt` has no PILOT_NEVER_REUSE_AS_EXAM marker but lists the truths.**
   `log()` (`run_ladder.py:101-105`) appends raw lines, and line 248 logs
   `n={n} truths [...]`. The other 12 output files carry the marker. Write the marker as
   the first line of `progress.txt` (OUT and OUT/presmoke).

## Info

4. `gworld.py:35-39`, `wind.py:35-37` and `viab_joint.py:22` put fixed `/home/user/evalwork`
   paths ahead of the bundle on `sys.path`. Harmless on a Prime pod (user ubuntu, those
   directories do not exist), but better derived from `__file__`.
5. A hard kill during a write can leave a partial `*.tmp` / `*.tmp.npz` in OUT (writes
   are tmp + `os.replace`), which would then be published.
6. The presmoke cannot fail on its deadline: it exits 0 even when every net and scoring
   view was skipped.
7. The blind arm (class e) only reaches N=32, while the docstring and the arm comparison
   assume 128 class-e Lab episodes.
8. The member-tick figures in the code comment and the request are about 2x the code's
   own count.

## Secrecy and safety (clean)

- **Secrecy test:** an audited presmoke run with `os.urandom` patched to a known value
  wrote the secret to none of the 13 outputs. The search covered raw bytes, both hex
  cases, base64, 12 child secrets and 20 key words or item labels. Only the commitment is
  written, in `info.json` and `truths.json`.
- **Hidden material:** `pilot.secret()`, which reads `hidden/secret.hex`, is defined but
  never called. The audit saw no `hidden/` or `*.hex` read, and the bundle holds no
  hidden material: the truths it holds are published pilots with the marker, as
  `HIDDEN_NOT_COMMITTED.md` says.
- **Evaluator modules:** `lab_service` (socket), `sandbox` (subprocess) and `instance`
  are bundled but never imported. Only `acceptance.py` runs, and it uses numpy.
- **Processes and network:** none (audit hook).
- **Writes:** only to OUT, all atomic except the log.
- **Size:** about 12-13 MB in total, largest file about 1.8 MB.
