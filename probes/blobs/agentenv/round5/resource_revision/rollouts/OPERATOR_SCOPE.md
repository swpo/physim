# Operator scope reduction — 2026-09-06

User requested no more seeds/worlds start; retain work already in flight.
At request: E1#928 completed, E1#929 and E2#942 active, E1#930/E2#943/#944 queued.
Native runner has no admission-only signal and releases its semaphore before
persistence. Root installed exact-parent PID/birth/command-hash startup fences
at03:28Z and tested native module boot rejection before port/server/model work.
Existing tool servers stay unchanged. Event-driven kqueue watchers terminate
only after the named current terminal trace is saved; no wall-time deadline.

E2#942 finished03:21:52Z, before the fence was armed. E2#943 therefore slipped
into startup03:21:52Z and toolserver03:22:18Z; it was stopped03:33:11Z by the
completion watcher. This unintended~11-minute admission is NOT hidden or
scored. No complete trace/usage total exists for that canceled task. E2#944
was never admitted. E2 process exited130 after the saved#942 result.
E1#929 remains active; exact startup fence blocks future#930. Its watcher will
stop the evaluator after#929's terminal record is saved. No queued task may be
resumed later without explicit approval. Original configs remain as launch
evidence; this file records the later operator-authorized scope change.

Retained report scope: E1#928/#929 and E2#942, with canceled tasks separate.
Scores/experiment accounting are provisional because the completed-run audit
found repeated fork IDs under distinct parallel requests and lost-counter
symptoms. Raw data must not be edited. Cheap concurrency/transport regression
is needed before another benchmark, not further paid model probes.

Final03:40Z update: E1#929 terminated naturally with a provider/server-mid-response
HarnessError and no score. Its watcher stopped evaluator27324 only after this
terminal trace was saved. E1#930 had a scheduler-start log at03:39:57 but was
canceled during setup before any observed container/tool/model stage. E2#944
was not admitted. Both evaluators and completion watchers have exited, and
both exact-parent startup fence files were removed. No further benchmark
model work is authorized.
