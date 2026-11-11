# vfport: PROGRESS

## INTEGRATION, round 4 (integrator; worktree wt-port4i, run label physim2-port4i) -- 11 Nov 2026, IN PROGRESS
- Merged `wt-port4a` (9dafd57df) and `wt-port4b` (150b38d38) into a branch from origin f96477e6c: no conflict
  (B's branch held A's final commit; the merged tree under round6/vfport equals B's). Nothing outside
  round6/vfport changed.
- Changed before the pin: `tools/pin.py` (lists `physim2_verifier/` and the whole `docker/` folder),
  `tools/check_round3.py` (crashed at the merged code; its command-form part follows round 4; 48 of 48),
  `tests/prove_round4.py` (container named after the caller's run label), `RUNBOOK_MAC.md` step 3f (EXIT 137, 143),
  new `rehearsal/issue4.py` and `rehearsal/fetch4.py` (outside the pin).
- **Pin: `PIN.sha256` 135 files, sha256 9f1511add96b527d0ef208f81f5195162c4159740e898fefbb7dde6396d896e4**
  (round 3: 109; 83 unchanged, 26 changed, 26 new). `tools/check_runbook.py` 51 of 51.
- Every check at the pinned code (`results/round4_integration.json`): safety 36/36, units 59/59, round3 48/48,
  round4 125/125, runbook 51/51 (host, tripwires or text); driver 31/31, interrupt 8/8, exam_units 91/91, harness
  set-up replay without network (throwaway containers); check_step3 44/44 and prove_round4 48/48 with the round-5
  cross-check (vf-eval, stand-in endpoint or scripted; no model).
- Image `physim2-ring:2` (fixer A's build) not rebuilt: not a cache hit behind this proxy, 2.3 GB free for
  everyone. Its `uv` stand-in and its 41 packages match the pinned files (checked in a throwaway container).
- NEXT (this role): push; rehearse `RUNBOOK_MAC.md` from a fresh clone of the pushed head (steps 0 to 2 with one
  interruption and one watchdog trip; step 3 with a real model: one rollout killed between two model calls and
  cleaned up by the runbook, one to its natural end); publication folder to `../rollouts/qwen_ring_002/`; record in
  `results/rehearsal_round4.json`. This note is completed when that is done.

## VERDICT, round 3 pass 1 (of branch head db3ff5a6e) -- 10 Nov 2026, finished: GO for steps 0 to 2
- This note was written just before the verdict commit. The verdict is the commit right after it: the last
  commit that touched `HOST_SAFETY_AUDIT.md` and `RUNBOOK_MAC.md` (it holds those two files and nothing else).
  If no commit after this note touched them, the verdict was NOT committed: redo the last step below.
- **Verdict: GO for the scripted smoke test on the lead's Mac (runbook steps 0 to 2, "If a run was interrupted",
  step 4 on the lead's word), from that ONE commit; the coordinator's message names its hash.** It replaces the
  suspended round-2 GO (af767adb is not to be run). The one-model rollout stays NO-GO. Judged: code and commands
  of db3ff5a6eacc6a4ccc66374df5ac3fc0051c75e3; sha256 of `PIN.sha256` cd67eb4b...03e4 (109 of 109 from a clean
  archive; 91 files identical to the round-2 pin, 14 changed, 4 added).
- What the verdict wrote: the first line of `HOST_SAFETY_AUDIT.md` (the fixer's suspension note went with it),
  the section "Re-audit, round 3", and the notice between HOLD-BEGIN and HOLD-END of `RUNBOOK_MAC.md` (37 lines
  longer than the hold notice; the rest of the runbook is byte for byte the judged text, 33 fenced commands
  equal). No command changed.
- Status of the Mac's findings: M1, M3, m1 to m6, m8 to m11, D1 closed; M2 closed by the notice (the one missing
  row: Python kills verifiers' `docker rm --force <box>` client after 30 s); m7 as a rule, widened by the notice,
  bearer deferred to before step 3. The six text items of the runbook re-audit are the notice's two rules and
  four corrections. Its item 10 (PYTHONEXECUTABLE, __PYVENV_LAUNCHER__) is residual G1: not macOS-only, run
  here; such a session fails step 1's import check (a stop); by hand for the lead.
- Evidence of my own: read (vfrun.py, _nokey.py, vfeval.py, build_reference.py, the diff of the other pinned
  files, the verifiers kill sites and credential readers, CPython 3.12.13 getpath and subprocess); run (pin;
  the commands against the rehearsal record: 65 of 65 match, 26 of 33 blocks issued; PYTHONEXECUTABLE with a
  one-line program); container (mine: allow-list, floor, one SIGTERM, nothing removed, 97 and 98); tripwire
  (mine: 0 opens and 0 stats of a made-up credential file with the package first, the stock control opens it).
  No rollout by me; nothing on macOS.
- Left on the machine by this role: nothing (no container, no process). Scratch `vfr3verdict1` is deleted and
  the worktree `wt-vfr3verdict1` removed after the push. The Docker daemon was running before and was not touched.
- Next step (exact), for the coordinator: the GO message to the lead with the 40-character hash of the verdict
  commit and the by-hand list of "Re-audit, round 3" (G1 in the starting terminal; 11 GiB free; nothing else in
  Docker; the pilot folders after a stop). Later pass, not gating: the notice's six points into the runbook
  body, G1 into step 0 and `ENV_REFUSE` (new pin), the minor items of the code re-audit; before step 3: the
  lead's disk decision, the bearer, a rehearsal of the free dry run in the cloud container. Stale: `README.md`
  lines 14 and 99-100 and `results/summary.json` still say ON HOLD.

## RE-AUDIT of the runbook, round 3 pass 1 (independent; of branch head 33173af09) -- 10 Nov 2026, finished
- Role: re-audit of `RUNBOOK_MAC.md` only, read as the Mac session reads it. The report went back to the coordinator
  as text. **My verdict on the runbook: NO-GO as written, narrowly** (prose, and one line of one command; no pinned
  file). The hold notice was not touched. No file but this note was changed.
- Evidence labels: read / run (my own scripts and stand-ins in scratch; no file of the port executed, nothing
  signalled) / tripwire (mine: the package imported from a clean archive with every kill, delete and process start
  replaced, a made-up credential file in a scratch home) / inferred (everything about macOS).
- Closed: M1 (the session's own step-0 command, all name classes), M3 (six listeners match the source; tripwire:
  package first -> `stand-in`, 0 opens, key EMPTY; stock import -> 4 opens, key loaded), m1 to m6, m8 to m11, D1,
  the three removals (literal, label or `test ! -L` guarded), step 3 (file gate on both commands; `tools/vfrun.py`
  refuses a model config without `--model-credentials`).
- Open, with replacement text in the report: (1) M2, one row missing in the signal table: Python kills verifiers'
  `docker rm --force <box>` client after 30 s (verifiers `runtimes/docker/__init__.py:553-567`); (2) m7, the
  "nothing else runs in Docker" check stands before 2a only; (3) section C says 8 GiB is enough while steps 1 and 2
  write about 3; (4) `~/.docker/buildx/` is not among the writes; (5) the opening lines claim point 4 was rehearsed;
  (6) nobody is named for the pilot folders after a stop without point 6; (7) new, macOS, inferred: PYTHONEXECUTABLE
  or __PYVENV_LAUNCHER__ in the session moves `sys.executable`, so the tools' children would not be listed by the
  status command; step 1's interpreter check should also compare `sys.executable` (one command changes).
- Rehearsal record: all 65 recorded commands equal one of the 33 fenced blocks of the head after undoing the
  recorded substitutions (my script); 26 blocks issued, 7 never (image build and its status, the five of step 3).
- Left on the machine by this role: nothing. Scratch `vfr3book1` deleted; worktree `wt-vfr3book1` removed after the
  push. The Docker daemon was not used.
- Next step (exact), for the coordinator: a prose pass on the items above, one Linux rehearsal of the changed
  interpreter-check line, then pass 2 of this re-audit.

## RE-AUDIT of the code, round 3 pass 1 (independent; of branch head 33173af09) -- 10 Nov 2026, finished
- Role: re-audit of the CODE only (M1, M3, m1, m5, D1; the whole diff since 40c697e54; the tests; the pin). The
  report went back to the coordinator as text. **My verdict on the code: GO** (for the scripted steps 0 to 2; the
  runbook text has its own re-audit; the hold notice was not touched by me). No file but this note was changed.
- Evidence labels: read / tripwire (run by me on the cloud host in a child process under `tools/tripwires.py`, a
  made-up credential file in a scratch home) / container (mine: one `docker run --rm -i --network none
  python:3.12-slim`, named, no mount, gone afterwards) / inferred (everything about macOS). No rollout was made
  by me; nothing ran on macOS.
- Pin: clean `git archive` of the head, `sha256sum -c PIN.sha256` 109 of 109; sha256 of `PIN.sha256`
  cd67eb4b8d706acf44c23dce72efd087532b422a5b66179c1cdc92561ffd03e4 = the runbook's pin block. 14 changed, 4 added,
  91 identical to the round-2 pin (the driver, grading, taskset, access, the box scripts among them).
- M1 closed (container): of 56 made-up session names only HOME, LANG, TMPDIR, TZ, VF_RUN_ID (and PATH) reach a
  child; the refuse-list names 17 of them (every DOCKER_*, BUILDX_*, MCP_HOST/PORT, PHYSIM2_*, UV_*, VF_*,
  PYTHONPATH/HOME), and a real tool process started with DOCKER_CONTEXT ends before anything starts. Residual, minor: the refuse-list is a deny-list for the tool's own process;
  PYTHONEXECUTABLE (macOS: it sets sys.executable, hence the interpreter of vf-eval; inferred), other PYTHON*,
  DYLD_*, proxies are not on it (they do not reach a child).
- M3 closed (tripwire): stock import opens the made-up file and loads its key (control); through the package 0
  opens, 0 stats, nothing under the home folder touched in 26 module imports, the default and the stand-in
  client, `EvalClient`, `prime_runs.init(mode="disabled")`; a laboratory-like process stays closed even with
  PHYSIM2_MODEL_CREDENTIALS=prime. The two unpatched readers (prime_sandboxes, prime_tunnel) open the file only
  if instantiated; verifiers reaches them behind `ensure_prime_auth` only (`runtimes/prime.py:150`,
  `interception/tunnel/prime.py:36`), which the stand-in turns into an exit.
- m1 closed (container): the builder's `/proc/<pid>/cmdline` and environ hold the path of the 0600 file, not the
  value; the script gets it in memory; `--theta` on the command line, mode 0644 and a link are refused.
- m5 closed (container, real exit statuses): SIGKILL of vf-eval by itself, from outside, and in the command
  form: status 98 and the "may be left" line. Minor gap: a vf-eval that ends with 130 after a SIGTERM that did
  not come from the tool counts as a normal exit (`tools/vfrun.py:304`); prove.py then stops for lack of an
  episode, check_probe's `may_fail` rollouts would go on. Off the runbook's path (it signals the TOOL first).
- D1 closed (container): refusal before a start (97, nothing created); a trip sends one SIGTERM, status 97, a
  record, no file removed (tree compared before and after); SIGKILL only after the grace period. Minor: a stop
  of the tool during that grace sends vf-eval a second SIGTERM and loses the record (`vfrun.py:255-257`); the
  disk message lacks the "may be left" line after a SIGKILL (`vfrun.py:307-310`); a failing statvfs stops the
  run with status 1 and no record. Step 1 (uv, docker build) has the check before, not during.
- Whole diff: no new path that kills, deletes, moves or re-owns beyond `run_helper` (SIGTERM, then SIGKILL after
  20 s, to the tool's own helper). `rehearsal/issue3.py` (outside the pin, cloud only, refuses off Linux and
  without the marker file): `--env HOME=...` or `--inherit HOME` would aim the runbook's rm -rf of the two pilot
  folders at another home (lines 238-245); refuse those two names.
- Tests rerun by me from this worktree: `tools/check_round3.py` 48 of 48, `tools/check_interrupt.py` 8 of 8,
  `tools/check_runbook.py` 46 of 46 (its temp folder in my scratch), `pin.py --check` 0 differences. Not rerun:
  `tools/check_safety.py` (its diff read only), any rollout.
- Left on the machine by this role: nothing (no container, no process). Scratch `vfr3code1` deleted; worktree
  `wt-vfr3code1` removed after the push. The Docker daemon was running before and was not touched.
- Next step (exact), for the coordinator: the verdict of round 3 from the two re-audits. The minor items above
  change pinned files; none is needed for steps 0 to 2.

## HOST-SAFETY FIXER, round 3 pass 1 (after the Mac session's read-only review of af767adb) -- 10 Nov 2026, finished
- Role: the Mac review's findings M1 to M3 and m1 to m11 and the coordinator's disk requirement D1.
  `RUNBOOK_MAC.md` is ON HOLD (first act of this role, commit fb54884bc; a suspension note stands above the first
  line of `HOST_SAFETY_AUDIT.md`, whose own text was not touched). Round 3 is NOT re-audited.
- Index: `results/host_safety_round3.json` (one entry per finding: status, where confirmed, what changed with
  file and lines, test, result, record). README sections 8.9 to 8.11. `results/summary.json`:
  `host_safety.round_3_of_fixes`, `.rehearsal_round_3`, `.re_audit_round_2`.
- Status: M1, M2, M3, m1 to m6, m8 to m11, D1 closed; m7 as a rule in the runbook, its bearer deferred to before
  step 3 (said in the runbook, step 3). No finding was rejected. One thing the review did not have was found and
  closed: the prime-runs SDK reads `~/.prime/config.json` and its key for every run, uploads off or not.
- Pinned code changed: 14 files changed, 4 added (`physim2_env/_nokey.py`, `tools/vfeval.py`,
  `tools/build_reference.py`, `tools/check_round3.py`), 91 of 109 unchanged (the driver, its guard, grading,
  taskset, access, store, the scripted harness, round 5, vw: byte for byte the round-2 pin). `PIN.sha256`: 109
  files, sha256 cd67eb4b8d706acf44c23dce72efd087532b422a5b66179c1cdc92561ffd03e4.
- Checks on the new code (none kills or deletes on a host): `tools/check_round3.py` 48 of 48 (22 under tripwires,
  8 traces of a made-up credential file, 18 with real signals in one throwaway container without a mount);
  `tools/check_safety.py` 36 of 36 (65 tripwires); `tools/check_interrupt.py` 8 of 8 (containers);
  `tools/check_runbook.py` 46 of 46 on the final text; `tools/pin.py --check` 0 differences.
- Rehearsal: fresh sparse clone of 00947b226 (same pin), 20:01 to 20:37 UTC, 65 commands each as one `sh -c`,
  `$HOME` given as a variable (commands byte for byte but for the study path, pid/name and, on this 1.8 GiB
  machine, the disk floor). Steps 0, 1 (no image build), 2a, 2b (37 rollouts: 32 of 34, 66 of 66), 2c, 4; a stop
  by the stop command, a hard kill with the label-checked removal, a watchdog refusal at the runbook's own 8 GiB
  and a watchdog stop during a rollout. The kernel's record of every open of a made-up credential file in the
  rehearsal's home: 0 events in 45 rollouts; 3 for the stock import as a control. Three prose mismatches,
  corrected; the 33 fenced commands of the final runbook equal the rehearsed ones. `results/rehearsal_round3.json`.
- Not done, and why: nothing on macOS (inferred only); the image build (the shared image exists); step 3 (never
  run; its two start commands are new); point 4 of the interruption section on a live case (Linux kills the
  laboratory with its parent); `tools/check_units.py`, `tools/check_driver.py`, `prove.py --worlds 4`, gliders,
  the red team's attacks were not run again (their code did not change).
- Left on the machine by this role: nothing of the pilot (no container, no process); the Docker daemon, which I
  started after a restart of the container and did not stop; the three images untouched; files `/tmp/vf-port-*`
  that verifiers never removes (one per rollout, as the runbook says: not deleted by pattern). Scratch `vfr3fix1`
  deleted except `dockerd.log`, the log of the running daemon (1.2 MB); worktree `wt-vfr3fix1` removed after the
  last push. Final commit of the role's work: 63abe1fd0 (this note is one commit later).
- Next step (exact), for the coordinator: a re-audit of round 3. To read: `git diff af767adbd..HEAD --
  research/alife/vecworld/program/round6/vfport` (the pinned diff is in the 18 files named above),
  `RUNBOOK_MAC.md`, `results/host_safety_round3.json`. To repeat the checks in the cloud container, from this
  folder, with `V=/home/user/evalwork/vfport/.venv/bin/python` and
  `D="env -i PATH=$PATH HOME=$HOME PHYSIM2_DEV_MACHINE=cloud-container"`:
  `$D $V -B tools/check_round3.py --scratch <a fresh scratch folder> --out <scratch>/r3.json` (host under tripwires
  and one container named vfr3fix1-check-round3, removed by --rm), `$D $V -B tools/check_safety.py --out ...`,
  `$D $V -B tools/check_interrupt.py --out ...`, `$V -B tools/check_runbook.py --out ...`, `$V -B tools/pin.py --check`.
  The pilot's tools now start only from a clean environment: `env -i PATH=$PATH HOME=$HOME VF_RUN_ID=<label>`.
- If the container restarted after this note: nothing of this role is running; recreate nothing.

## VERDICT, round 2 (of the branch head after the two round-2 re-audits) -- 10 Nov 2026, finished
- Role: issue the round-2 verdict from the fixer's report and the two re-audits (code, runbook), checking what
  I rely on at the branch head. The verdict follows in the NEXT commit and changes two files only:
  `HOST_SAFETY_AUDIT.md` (first line, and a section "Re-audit, round 2") and the notice between HOLD-BEGIN and
  HOLD-END of `RUNBOOK_MAC.md`. This note is the only other thing this role changed.
- Verdict: GO for the scripted smoke test on the lead's Mac (steps 0 to 2, "If a run was interrupted", step 4),
  for ONE commit: the one that holds the GO notice (the pushed head after the verdict commit; the coordinator's
  message gives its 40-character hash). Step 3 is not released: it may be offered to the lead after the smoke
  test has passed on the Mac and been reported. Judged: code and commands of 40c697e54.
- Checked by me at the head, nothing of the port executed on the host:
  run: `sha256sum -c PIN.sha256` 105 of 105 (7aa9bbfc...f64c19); 30 fenced commands, all begin with the guard,
  equal at be2c17ae6, 40c697e54 and the head; 23 of them are in the rehearsal record byte for byte (never
  issued: the image build and its status, the five of step 3); only `$HOME` and `$?` as variables, four delete
  or signal targets, all literal; the guard with `echo` for 9 wrong targets from 4 start folders prints once,
  for an empty path started inside the folder itself; the 2a start, the status and the stop (aimed at the
  waiting shell, with the placeholder left in, then at the tool) through my own command tool on a sleeping
  stand-in: one process line, nothing signalled twice, then `EXIT 143`, nothing left.
  read: `_item.py` in full, the three gates, `grading.py:49-87`, verifiers' Docker runtime (no mount option on
  a box), vf-eval's dry run (returns before any rollout), `physim2_env/lab_tools.py` (validate and submit run in
  the box, never on the host), `tools/run_report.py`, both configs, `rehearsal/issue.py` (refuses off Linux).
  run (pure functions only, cut out by ast): the code re-audit's wider N5 holds (`--ipc=host` and
  `-v /dev:/dev` shaped tables pass); a Mac share is refused wherever it is mounted.
  container (mine, no mount, no network, removed): the driver check 27 + 4 = 31 of 31; 6 starts of the box
  scripts refused, canary alive.
- Open items of the two re-audits: the three that the runbook re-audit wanted in before the hold is lifted and
  that can be said in the notice are in the notice as rules (a time bound for the "must show" branch; the
  section used once also after a restart; step 4's image list); the rest is minor and listed as residual in
  the audit file.
- Not done by me: any rollout, anything on macOS, the red team's attacks, `prove.py --worlds 4`, gliders.
- State left: no container of mine (vfverdict2-driver-main, -extra, -gate-1..6 ran with --rm), the three
  images and the daemon untouched, scratch `vfverdict2` deleted, worktree and branch removed after the push.
- If the container restarted before the verdict commit: recreate the worktree as the role text says and look
  at `git log -3`; if the commit "round-2 verdict" is not there, the verdict was not issued.

## RE-AUDIT of the runbook, round 2 (independent; of commit 40c697e54) -- 10 Nov 2026, finished
- Role: re-audit of `RUNBOOK_MAC.md` only (sha256 b08fb77a...c059 at 40c697e54), read as the Mac session would
  follow it. Verdict returned to the coordinator: GO for steps 0 to 2 as far as the runbook goes, with prose
  replacements recommended before the hold notice is replaced; step 3 keeps its own hold. This section is the only
  thing this role changed. The hold notice was NOT touched: that is the verdict's act.
- Labels: read; run = stand-ins in scratch, no file of the port executed; container = two throwaway containers of
  mine without any mount, removed by exact name; inferred = everything about macOS. I ran no rollout.
- Pin: `sha256sum -c PIN.sha256` and `shasum -a 256 -c` on a clean archive of 40c697e54: 105 of 105; sha256 of
  `PIN.sha256` 7aa9bbfc...f64c19 = the runbook's line 17.
- Closed: A1 and change 1 (30 of 30 fenced commands and the inline one begin with the guard; the guard with `echo`
  prints nothing for the placeholder, another project's folder and an empty path: run); A2, changes 1 and 2 of the
  round-1 verdict (run through my own command tool against a stand-in folder: the status listed the tool and not the
  waiting shell; the stop command printed and signalled nothing for the waiting shell and for an unreplaced
  placeholder, and stopped the tool with `EXIT 143`); interpreter, step 1, pin handover, text (read).
  `docker info --format` returns 1 against a dead socket (run, client 29.9.2).
- Rehearsal record: 23 of the 30 fenced commands match its literal texts after undoing its two substitutions; the
  30 fenced commands are equal at be2c17ae6 and at 40c697e54 (run). Never run: the image build with its status, all
  of step 3. Not in its list of mismatches: step 4 printed three images, the text names four.
- New, all minor, none reaches beyond the pilot: (1) the failing branch of 2a's "must show" rule has no time bound
  (lines 310-312); (2) "use this section once" cannot be known by a restarted session (409); (3) step 4's image
  list (590-592) is probably false under BuildKit, where base images are not listed (inferred); (4) rule A.1 tests
  for ON HOLD, not for the GO notice (35); (5) what a stop in step 1 or 4 leaves is not listed for the lead;
  (6) hardening: `docker rm -f` (451) has no check of its own; a label-checked form was run in containers;
  (7) step 3 only: the dry run (494) is not behind the lead's file, and "writes it here" (507) contradicts line 2.
  Exact replacement texts: in the report to the coordinator.
- State left: no container of mine, images untouched, daemon untouched, scratch `vfreaud2b` and my worktree removed.

## RE-AUDIT of the code, round 2 (independent; of commit 40c697e54) -- 10 Nov 2026, finished
- Role: re-audit of the CODE only (A3, A4, A5; required changes 3, 4, 5; the whole diff since 997005f56; the
  required tests). Verdict returned to the coordinator: GO on the code, for the pinned hash only. This section is
  the only thing this role changed.
- No pinned file changed in round 2 (my own `sha256sum -c PIN.sha256` at the head: 105 of 105; sha256
  7aa9bbfc...f64c19; since 73829e5c6 only texts, `rehearsal/` and `results/` differ).
- A3, A4 (4c, 5), A5 (4a, 4b): closed as specified. Read: `_item.py`, `grading.py`, `taskset.py`, `access.py`,
  `validate.py`, `physim2_script/__init__.py`, the three box scripts, every tool of the diff, verifiers' Docker,
  subprocess and base runtime.
- Reruns, each equal to its recorded file: `tools/check_safety.py` 36 of 36 (host, under its 65 tripwires; only
  the name of the temporary folder differs); the in-container script of `tools/check_driver.py` 31 of 31 (two
  `docker run --rm --network none` containers with names of my own; the tool's host part was not executed, its
  script text was taken from the source). Not rerun: `check_interrupt.py`, `check_units.py`, the probe rollouts.
- My own attacks. Host, pure functions under tripwires: 33 crafted mount tables. Throwaway containers without any
  host path, removed: a missing, an empty and a garbage mount table with every other layer present (all five
  functions refuse, canaries alive); nine shapes of trees for the wipe (files, directories and link targets of
  other owners all survive); the three box scripts without the marker (7 starts refused).
- New, minor, Linux only, for the later pass that already holds N5 and N6: a container started by hand with
  `--ipc=host` has a mount table of the stock shape (captured from a container that only ran `cat`; only the
  source name of `/dev/shm` differs, `tmpfs` instead of `shm`), so the guard's mount condition passes and the
  cleanup would walk the host's `/dev/shm` for the one uid. `-v /dev:/dev` passes for the same reason (devtmpfs
  is an accepted type). The fix proposed for N5 ("stock mount points only") does not cover either: it has to be
  an exact list of (mount point, type), with source `shm` for `/dev/shm`.
- Also seen: with a hand-made marker in a container the environment did not prepare, `redteam/agent_rt.py hostile
  killall` does issue `kill -9 -1` (the processes of that container only): the gate is the two files, as change 3
  specifies; N7 stands. `rehearsal/issue.py` acts for real on the cloud host by design (the runbook's own `rm -rf`,
  `docker rm -f`, `kill`); its folder check rests on `--inside`, which the caller chooses.
- Could not do: anything on macOS (inferred only: the gate and the guard pass in a stock Docker Desktop box, and
  refuse without damage if its mount table differs).
- Left on the machine by this role: nothing. Scratch deleted, no container, the three images untouched, the
  daemon untouched, worktree and branch removed.

## HOST-SAFETY FIXER, round 2 (after the round-1 verdict, NO-GO narrow) -- 10 Nov 2026, finished
- Role: the seven remaining changes of "Re-audit, round 1" (HOST_SAFETY_AUDIT.md): runbook text and one rehearsal
  in session mode. No file listed in PIN.sha256 changed (sha256 7aa9bbfc...f64c19; `tools/pin.py --check`: 105
  files, 0 differences). RUNBOOK_MAC.md is rewritten and STILL ON HOLD: round 2 has not been re-audited.
- Index: `results/host_safety_round2.json` (one entry per change: lines, the verdict's test, result, record file).
  README section 8.5 to 8.8 and `results/summary.json` (host_safety.round_2_of_fixes) describe the state.
- Done: 1 the process listing anchored on the pid and the interpreter path (`ps axww -o pid= -o command= | grep -E
  "^ *[0-9]+ <path>/\.venv/bin/python"`; two -o options instead of the verdict's `pid=,command=`, which a BSD ps
  may misread) and a by-hand check that the path is plain; 2 a stop command that looks at the pid's command line
  before it signals; 3 `--managed-python` on both uv commands, an interpreter check in step 1, the "must show"
  rule after each detached start; 4 `uv sync` detached with a log, and the new head of "If a run was interrupted"
  (step 2 only, once, stop on a Docker error); 5 the pin handover (no commit in the file; the hash of the GO
  message; a marked hold notice; what a failed comparison prints); 6 the three log endings and the other text;
  7 the rehearsal. Same pass, not gating: no `docker run` by hand at all; a file gate LEAD-GO-STEP3 on the paid
  command; a command for the lead that copies the step-3 trace out before step 4.
- Tests: `rehearsal/check_round2.py` 47 of 47 (text, and the runbook's own commands as `sh -c` / `bash -c` against
  stand-ins): `results/session_mode_round2.json`. Pinned `tools/check_runbook.py`: 32 of 33; the one failure asks
  for the round-1 `[p]ython` pattern (`results/safety_runbook_round2.json`).
- Rehearsal (16:47 to 17:27 UTC; fresh sparse clone of the pushed commit be2c17ae6, its own .venv on uv's Python
  3.12.13; every command as ONE `sh -c '<text>'` by `rehearsal/issue.py`; 81 commands, 40 of them statuses, literal
  text and complete output in `results/rehearsal_round2.json`): steps 0, 1 (no image build), 2a (7.5 min, all
  graded), 2b (37 rollouts, 1,264 s: 32 of 34 and 65 of 65), 2c, 4; five interruptions cleared by the runbook's
  own points (the stop aimed at the waiting shell: nothing printed, nothing signalled; a tool inside a rollout:
  EXIT 130 with a traceback; a tool before its first rollout: EXIT 143; SIGKILL of vf-eval twice: container
  removed by name, the laboratory once gone by itself and once stopped by the stop command; the vf-eval of 2c:
  EXIT 130 without a traceback). The 2a start and one status also through this session's own Bash tool: one
  process line, the tool. Six places of prose differed and were corrected; the 30 commands did not change.
- Regression on the pinned code, from the clone: check_safety.py 36 of 36 (host, tripwires), check_driver.py 31 of
  31 and check_interrupt.py 8 of 8 (throwaway containers), each equal to the recorded file. NOT rerun:
  check_units.py (nothing pinned changed; part of it runs outside its tripwires, which this role may not do on
  this host), prove.py --worlds 4, gliders, the red team's attacks.
- Could not do: anything on macOS (zsh, BSD ps, uv's Python there: inferred); the image build in the runbook's
  form; step 3; the rule "use the section once" as a rule. Not touched: the four minor code gaps the re-audit
  deferred (they need a change of pinned files).
- Next step (exact): a re-audit of RUNBOOK_MAC.md at the head of the branch (this commit), reading
  `results/host_safety_round2.json` first, then a round-2 verdict. A GO edits the hold notice only, and the
  coordinator's message names the commit that holds that edit.
- Left on the machine by this role: nothing but 39 more `/tmp/vf-port-*` files, which verifiers never removes
  (scratch deleted, the four leftovers of the two hard kills removed by exact name, worktree removed, no container,
  the three images unchanged, the Docker daemon not touched).

## VERDICT, round 1 (of the branch at 73829e5c6, after the two re-audits) -- 10 Nov 2026, finished
- Verdict: NO-GO for the smoke test on the Mac, NO-GO for the model rollout. RUNBOOK_MAC.md stays ON HOLD and was
  not changed. The verdict, its table, the seven remaining changes and the residual risks are the section
  "Re-audit, round 1" of HOST_SAFETY_AUDIT.md, in the commit after this one (that commit changes that file only).
- Why: the code is GO (A1, A3, A4, A5 closed; code = PIN.sha256 7aa9bbfc..., 105 of 105 files at the head). A2 is
  open, narrowed: issued as a session issues commands, the status command lists the waiting wrapper shell next to
  the tool, and SIGTERM to it stops nothing and loses the `EXIT` line (run here with a sleeping stand-in). Also
  open: the interpreter's process line on a Mac with a framework Python (inferred), no branch for a cut in step 1,
  the handover of the pin, and a rehearsal in session mode.
- Own runs: the pin at the head; the script of tools/check_driver.py in two named throwaway containers, 31 of 31,
  plus a guard-only probe with `--tmpfs /dev/extra` (the guard passes: the code re-auditor's minor gap); the three
  box scripts started in a container without the marker (all refused); the folder guard with `echo` from wrong
  folders (nothing printed). Nothing of the driver or of the box scripts ran on the host itself; no vf-eval, no
  model, no upload.
- Next step (exact): a fixer makes the seven changes of "What remains before GO for the smoke test" (runbook text
  and one rehearsal in session mode; no file listed in PIN.sha256 changes), then a re-audit of the runbook and a
  round-2 verdict.
- Left on the machine by this role: nothing (scratch deleted, worktree removed, no container, images unchanged,
  the Docker daemon not touched).

## RE-AUDIT of the code, round 1 (independent; of commit 73829e5c6) -- 10 Nov 2026, finished
- Role: re-auditor of findings A3, A4, A5 and required changes 3, 4, 5. The numbered verdict went to the
  coordinator; nothing of the port was changed by this role. Code at the head = PIN.sha256 (105 files, 0 differences).
- Reruns from a clean archive of the head, all equal to the recorded files: tools/check_safety.py 36/36 (host, under
  tripwires), tools/check_driver.py 31/31 and tools/check_interrupt.py 8/8 (throwaway containers, no host path).
  Not rerun: tools/check_units.py (part of it runs outside its tripwires), tools/check_probe.py (37 rollouts).
- Own runs: wipe edge cases in a stock container (only paths of the uid removed; links unlinked, not followed);
  two rollouts through vf-eval (probe-grading graded, 8 item boxes cleaned; harness-killall ended with status 137).
- Two new minor gaps, both off the runbook and Linux-only, neither run destructively:
  (1) the mount allow-list accepts any memory or kernel file system below /dev, /proc, /sys (`--tmpfs /dev/extra`:
  the guard passes and the cleanup walks it); (2) the guard does not look at namespaces (`--pid=host`: the guard
  passes with the host's processes visible; read of the guard only, under tripwires).
- Left on the machine by this role: nothing (scratch, worktree, containers and two /tmp/vf-port-* files removed).

## RE-AUDIT of the runbook, round 1 (independent; of commit 73829e5c6) -- 10 Nov 2026, finished
- Role: re-auditor of RUNBOOK_MAC.md as the Mac operator reads it (findings A1, A2, B1 to B15; required changes
  1, 2, 6, 7, 8, 9). The verdict and the replacement texts were returned to the coordinator, not written here.
  Nothing of the port was changed or executed by this role.
- Recomputed: sha256 of PIN.sha256 equals the runbook's; 105 of 105 listed files match, at 454812a2b and at the
  head. The 27 fenced commands are byte-identical at cac38e324 (rehearsed), 454812a2b (pinned) and the head.
- Run here (scratch only, stand-ins `echo` and `sleep`, no file of the port executed): the folder guard from 8
  wrong folders x 2 start points prints nothing; `docker info --format` against a socket that does not exist exits
  1; the detached command shape as a Claude session issues it (`sh -c <text>`) leaves a waiting wrapper shell
  whose command line holds the command text, so the status command's pattern lists it next to the real process
  (the rehearsal ran the commands from files and did not see this); SIGTERM to that wrapper leaves the child
  running and no `EXIT` line; a pattern anchored on the pid and the interpreter path lists the real process only.
- Open at the end of this role (text of the runbook; no path found that deletes or kills outside the pilot):
  the process listing and the stop command of "If a run was interrupted"; no branch for a cut in step 1; no limit
  on repeats; the copy inside the pinned commit does not name the commit step 0 compares; small text mismatches
  with the rehearsal record, which holds command labels and truncated output; step 3 is gated by text only.
- Left on the machine by this role: nothing (scratch deleted, worktree removed, no container, no image, no
  process; the Docker daemon was not touched).

## HOST-SAFETY FIXER, round 1 (after the audit's NO-GO, HOST_SAFETY_AUDIT.md) -- 10 Nov 2026

Worktree `/home/user/wt/vfsafe1` (branch wt-vfsafe1, pushes to `claude/fisim-agent-world-research-hepmlz`).
Scratch `/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vfsafe1/`. Venv for development
runs: the builder's `/home/user/evalwork/vfport/.venv` (nothing installed into it). The rehearsal gets its own.
Rule of this role: nothing of the driver, its cleanup or the hostile scripts runs on this host; host tests run
under tripwires, real cleanups only in throwaway containers without a host mount.

### State (final for this role, 10 Nov 2026, 16:00 UTC)
- All nine required changes and S1, S2 are in the code; every test the audit named passes
  (`results/host_safety_round1.json`). RUNBOOK_MAC.md is rewritten, pinned and STILL ON HOLD: these changes have not
  been re-audited. The rehearsal of steps 0, 1, 2 and 4 is done (`results/rehearsal_round1.json`).
- Commits: cac38e324 = the commit that was rehearsed. The runbook's text was then corrected in five places;
  454812a2b = the commit the runbook pins (its pin block at the head of the branch names it). Both have the same
  `PIN.sha256` (7aa9bbfc79e7...), i.e. the same package, tools, agents and configs byte for byte. The commit after
  454812a2b changes the pin block of the runbook, results and this file only. A re-audit reads the head.
- Nothing is running. Docker daemon up, the three images unchanged, no container. Scratch `vfsafe1` deleted, the
  worktree removed. Left on the machine by this role: nothing besides 60-odd `/tmp/vf-port-*` files that verifiers
  never removes and uv's cache entry of one wheel.

### Rehearsal (15:12 to 15:50 UTC; fresh sparse, shallow clone of cac38e324 in scratch, its own .venv)
- As written: step 0; `uv sync` (dry run named the clone's .venv by its absolute path; 6.7 s); step 2a (7.5 min: all
  graded, 0 failed, 2.68 s per item box); step 2b (37 rollouts, 1,291 s: 32 of 34, 65 of 65); step 2c (3.5 min);
  step 4.
- Interruption 1: `kill -TERM` of the tool by the runbook's procedure: the real vf-eval removed its container and
  its laboratory; nothing listed 4 s later. Interruption 2: SIGKILL of vf-eval: one container and the laboratory
  stayed, the status command listed exactly those, removed by exact name and pid, folders reset, step run again.
- Deviations (machine): sparse clone; `$HOME` replaced by a scratch folder; image build NOT run (shared image,
  proxy, disk); IPv6 shim on PATH for the one direct vf-eval.
- Five mismatches of text and behaviour, all corrected in the runbook (listed in the record).

### Could not do
- A run on macOS or Docker Desktop (everything about them is inferred). The image build in the runbook's form.
  Step 3. A rerun of `prove.py --worlds 4`, of the gliders rollout and of the red team's attacks on the new code.
- round5/agentenv/mac (finding B12) is outside this folder and was not touched; the runbook's "never" table names it.

### Next step (exact)
- Coordinator: a re-audit of the diff of changes 3 to 5 (the audit asks for it) and of the runbook, reading the
  head of the branch; `results/host_safety_round1.json` is the index. Until it says GO, nothing runs on the Mac.

### Done (code)
- 1 (A1): runbook guard on every command, uv with --project and a dry run first. 2 (A2): `tools/vfrun.py` needs
  VF_RUN_ID, stops vf-eval with SIGTERM first, checks Docker; runbook: detached commands, status command, "If a run
  was interrupted". 3 (A3): box gate at the top of the three box scripts and before each `kill -9 -1`. 4 (A4, A5):
  `_item.py` mount allow-list in the guard, unreadable mount table raises, wipe by unlink/rmdir only, no rmtree.
  5 (A4): `grading.container_gate` (the real verifiers runtime object, not borrowed). 6, 7, 9: RUNBOOK_MAC.md
  rewritten, `PIN.sha256` + `tools/pin.py`, `tools/run_report.py`. S1: uid range 20000-59999, --uid required, root
  caller, identity verified before kill(-1), nothing runs outside a box without --no-box, agent box marker from the
  range. S2: `check_units.py` never starts the driver as root; red-team tools delete nothing they did not make.

### Results so far (all on the code of this commit; `results/host_safety_round1.json` names every test)
- `tools/check_safety.py` (host, 65 tripwires installed before the package is imported): 36 of 36.
- `tools/check_driver.py` (two throwaway containers, one with `--tmpfs /extra`): 31 of 31 (the 19 earlier ones among them).
- `tools/check_interrupt.py` (a throwaway container; two containers of its own for the label listing): 8 of 8.
- `tools/check_runbook.py` (text; the guard with echo): 33 of 33.
- `tools/check_units.py` (host, tripwires): 66 of 66; the driver is not started as a program (this process is root).
- `tools/check_probe.py` through vf-eval (14:49-15:07 UTC, 37 rollouts, 1,072 s): round 5's checks 32 of 34 reproduced,
  0 failed, 2 changed by design; 65 of 65 new checks (two new: the kill is issued inside the box; box scripts pass
  their gate there).
- NOT rerun: `tools/prove.py --worlds 4` (results/proof_ring.json stays from commit 743f6b75e), gliders, red team.

### If the container restarted
- `S=/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vfsafe1; mkdir -p $S;
  pgrep -x dockerd >/dev/null || (nohup dockerd --feature containerd-snapshotter=false > $S/dockerd.log 2>&1 &)`
- scratch (`$S/dev`: the probe's store and runs; `$S/rehearsal`: the clone, its .venv and its pilot folders) does not
  survive; the committed results do. A cut rehearsal: `docker ps -a --filter label=verifiers.run=physim2-pilot-20261110`
  lists its containers (remove by exact name), then start the rehearsal again from the clone.

---

# (record of the first fixer, kept)

## FIXER (role after the builder, the specification review and the red team) -- 10 Nov 2026

Worktree `/home/user/wt/vfportfix` (branch wt-vfportfix, pushes to `claude/fisim-agent-world-research-hepmlz`).
Scratch `/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vfport/fix/`. Venv: the builder's
`/home/user/evalwork/vfport/.venv`. Docker daemon was found running (classic image store), images kept.

### INCIDENT (10 Nov 2026, about 04:31-04:34 UTC) -- read this first
- What ran: the first version of my `tools/check_units.py` started `physim2_env/public/_item.py` (the one-request
  driver) as root ON THE HOST of this cloud container, outside any container.
- What it did: the driver's cleanup did there what it does in a box: SIGKILL to every process of uid 1000 and deletion
  of every file owned by uid 1000 on the writable file systems (/ and /var/lib/docker).
- Known loss: `/home/ubuntu` (home of the unused default account; recreated from /etc/skel, earlier content unknown).
  Coordinator's check: no tracked file missing in the checkouts and worktrees, the Python environments import.
- Reported on the coordinator's channel at 04:34:53. Fix (commit 7e034be18): `require_box(uid)` in the driver
  (marker /etc/physim2/predictor_uid + container evidence + PHYSIM2_BOX_CLEANUP=disposable-box + the box's own uid,
  never 0); `require_container(runtime)` before every runtime command; the real cleanup is tested only inside a
  throwaway container (`tools/check_driver.py`); on the host only refusals are tested, under tripwires
  (`tools/check_units.py`, checks `guard_*`). RUNBOOK_MAC.md is on HOLD until the coordinator's independent audit.

### Done (code; package final at commit 743f6b75e)
- S1: `_rules.freeze` refuses duplicate members, file/directory collisions, paths over 1024 bytes, more than 20,000
  members; skips names with control characters or undecodable bytes; `finalize` runs verifiers' `_validate_restore`
  inside its try. Hostile agents tar_duplicate, tar_collision, tar_longpath.
- S2 = R2: `item_isolation = "box"` (default): one fresh container per exam item through verifiers'
  `provision_runtime` with the verifier box's config (`grading.fresh_box`); `"shared"` = one box, pilot mode, marked
  in the trace. Probe (a2) measures four channels in both modes.
- S3: `grading.validate` (round 5's three example calls) in the verifier box before item 1, invalid = K on every
  item; tool ops validate/submit run the public validator in the agent's box through the controller
  (`access.BoxAccess.check`), a failed submit freezes nothing.
- R1, R5: `_rules.read_reply` strict (float32, level<l> members only, at most 16, bounded numbers, no allocation from
  a declared size); a non-finite score is a failed item; the reward is always a finite number.
- R3: the driver reads reply and error text through a directory handle, O_NOFOLLOW | O_NONBLOCK, regular files only;
  worker-side timeout per request.
- R4: `single_use` on by default, keyed by `agent_key` (default "<model>|<harness id>"); `tools/settle.py`.
- R6: random predictor uid per rollout (20000-59999). R9: malformed inputs are format rejections, a rejected
  experiment charges nothing; the final collection respects the submission cap.
- S4: `results/proof_ring_items.npz` + `tools/recompute_table.py`. S6: single_use default. S7: the agent box CPU
  counter is renamed `agent_box_cpu_s_unverified`. S8: allow-list for variables entering a box. S9: runbook.

### Results (all on the package code of commit 743f6b75e; `results/summary.json` names every source)
- `tools/check_units.py`: 67 of 67 (the builder's code: 25 of 46). `tools/check_driver.py` (in a container): 19 of 19.
- `tools/check_probe.py` (05:07-05:22, one more rollout at 06:03): round 5's 34 checks: 32 reproduced, 0 failed, 2
  changed by design; 63 of 63 new checks; 37 rollouts, 963 s.
- `tools/prove.py --worlds 4` (05:22-05:54, aggregation at 06:10): 24 rollouts graded, 0 failed items of 1,536;
  S 0.984, P0 0.930, PM 0.916, D 0.210, null -0.046, O 1.096 (of C); sigma 0.070, rho 0.776; C through round 5's
  grader identical in 4 of 4 worlds; C and D with one box per item identical to one box (2.6 s per item box).
  The tool was started three times: the first run ended in an exception in its aggregation step after every
  rollout was done (a key I had renamed); no rollout was repeated; wall time added from the logs (1,973 s).
- `tools/recompute_table.py`: 26 numbers, maximum difference 0. Gliders smoke (D, one box per item): graded, 0 of 8
  failed. Red team's attacks again: overflow and fifo graded as K in 24 s and 23 s; hostile-exit1 still without a
  reward on the trace (open hole 2; `tools/settle.py`).

### Running
- nothing. Docker daemon up (classic image store), images kept for the host-safety audit: physim2-ring:1,
  localhost/verifiers-network:1, python:3.12-slim (573 MB in all). No container. Scratch stores with the hidden pilot
  instances deleted; only logs are left in `<scratch>/`.

### Next step (exact)
- Coordinator: the independent host-safety audit (task 35) of this folder, then release RUNBOOK_MAC.md to the Mac.
  The audit can repeat the checks with: `V=/home/user/evalwork/vfport/.venv/bin/python; cd` to this folder;
  `PYTHONPATH=$PWD $V -B tools/check_driver.py --out /tmp/claude-0/.../driver.json` (container only) and
  `PYTHONPATH=$PWD PHYSIM2_DEV_MACHINE=cloud-container $V -B tools/check_units.py --out /tmp/claude-0/.../units.json`
  (host: refusals under tripwires; it starts test predictors, never the cleanup).
- Open holes and decisions for the lead: README section 6.

---

# (builder's record, kept)


Study: PhySim v2 exam as a verifiers environment (round 6). Worktree `/home/user/wt/vfport`, branch pushes to
`claude/fisim-agent-world-research-hepmlz`. Scratch: `/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vfport/`.
Venv: `/home/user/evalwork/vfport/.venv` (python 3.12, verifiers 0.3.2.dev163 wheel as v1 pins).

## Done
- Read: the memo, agentenv (evaluator/, physim2/, agents/, run_rollout, prove, check_probe), v1 (taskset.py,
  runtime_sandbox.py, container_worker.py, runtime_access.py), verifiers (isolated_verifier/env.py, task.py,
  rollout.py, mcp/*, runtimes/docker/*, utils/artifacts.py, harness.py, agent.py).
- Docker works here: `dockerd --feature containerd-snapshotter=false` (classic image store: no compressed copy of
  every layer, needed for the 600 MB budget). Images built: `physim2-ring:1` (513 MB incl. the 119 MB base;
  numpy+scipy+jax, jaxlib stripped), `localhost/verifiers-network:1` (+12 MB). `docker system df`: 524 MB.
- Found: verifiers' restricted Docker runtime passes `--sysctl net.ipv6.conf.all.disable_ipv6=1`
  (runtimes/docker/__init__.py:221-222); this kernel has no IPv6, so `docker run` fails with
  "open sysctl net.ipv6.conf.all.disable_ipv6 file: unsafe procfs detected ... no such file or directory".
  Workaround planned: a `docker` shim on PATH (tools/docker_shim) that drops that one option when
  /proc/sys/net/ipv6 is absent. The iptables cut itself was run by hand in a container here and works.
- Venv /home/user/evalwork/vfport/.venv: verifiers 0.3.2.dev163 wheel + numpy 2.5.4, scipy 1.18.1, jax 0.12.0.1.

- Built and working (commit 25b083f30 and later): physim2_env/ (taskset.py, lab_tools.py, access.py, bundle.py,
  grading.py, store.py, public/{labclient,validate,_item,_rules}.py), physim2_script/ (scripted harness),
  agents/ (install_prebuilt, probe_grading, hostile_submission), tools/ (make_instances, vfrun, prove, docker_shim).
- First rollouts through `vf-eval physim2-env --env.id isolated-verifier` on Docker here: D, C, P0 on one world
  graded with 0 failed items; about 75 s wall per rollout (57 s of it the 64-item verifier phase).
- Found: `docker exec` runs with umask 0000 in this container, so files written by verifiers' Runtime.write were
  world-writable; staging now chmods explicitly and the driver's --scan fixes any leftover.

- tools/check_probe.py RUN (02:47-02:52 UTC): results/probe_ring.json. Round 5's 34 checks: 32 reproduced, 0 failed,
  2 changed by design (agent is root in its own container). 33 of 33 new checks pass (probes a-d, with controls).
  Fixed on the way: zombies of killed predictor processes (driver is now subreaper and reaps), System V shared
  memory (removed as the predictor's user), umask 0 under docker exec.
- Written: README.md (two placeholders left: line counts and the proof numbers), RUNBOOK_MAC.md, configs/, uv.lock,
  tools/make_summary.py.

- tools/prove.py RUN (02:52-03:16 UTC): results/proof_ring.json. 24 rollouts, all graded, 0 failed items; table within
  noise of round 5's; the same C submission through round 5's grader gives identical per-item scores (4 worlds).
- tools/check_probe.py RUN again on the final code (03:16-03:22): results/probe_ring.json, 32 of 34 + 37 of 37.
- Gliders smoke: one instance and one D rollout through the route, graded (results/gliders_smoke_D.json).
- tools/make_summary.py -> results/summary.json (hidden-value scan: 6 instances, 192 files, 0 hits).
- README.md, RUNBOOK_MAC.md, uv.lock complete. Scratch stores and run outputs deleted (hidden instances).

## Running
- nothing. The Docker daemon is up (classic image store); images kept for the next role: physim2-ring:1 (562 MB
  with its 119 MB base), localhost/verifiers-network:1 (+12 MB). `docker system df`: 573 MB.

## Next step (exact)
- For another role: `S=<scratch>; V=/home/user/evalwork/vfport/.venv/bin/python; cd` to this folder, then
  `$V -B tools/prove.py --store $S/store --scratch $S/proof --worlds 1 --prefix check-ring --policies D,P0,C --out $S/check.json`
  (about 4 minutes, $0) and `$V -B tools/check_probe.py --store $S/store --scratch $S/probe --out $S/probe.json`
  (about 6 minutes). Delete $S/store afterwards.
- Not done: any model rollout, anything on macOS, the sealer and private store, compute metering (README section 6).

## If the container restarted
- `S=/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vfport; mkdir -p $S;
  pgrep -x dockerd >/dev/null || (nohup dockerd --feature containerd-snapshotter=false > $S/dockerd.log 2>&1 &)`
- images survive in /var/lib/docker only if the disk survives; rebuild with docker/Dockerfile.ring (see its header).
- the instance store under $S/store does NOT survive a scratch wipe: re-run tools/make_instances.py.
