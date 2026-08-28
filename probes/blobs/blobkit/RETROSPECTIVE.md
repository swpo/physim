
=============================================================================
RETROSPECTIVE: research-code -> deployable-software transition (2026-08-28)
=============================================================================
The five avoidable losses, each with its root cause and its SOFTWARE fix
(not another patch):

L1 CPU-vs-GPU run-time estimate miss (~$150 of slow CPU fleet)
   root: no cost model existed before launch; per-gen wall was discovered live.
   fix: PREFLIGHT COST REPORT as a make_bundle artifact — every bundle ships a
   measured worlds/hour x plan table (bench on 20 candidates locally/1 pod
   BEFORE fleet commit). A run that starts without a cost sheet is a bug.

L2 GPU deploy shim war (5 failed launches)
   root: name-based imports + in-place module swapping (research-era pattern).
   fix: SHIPPED — blobkit packaging + backend injection (0.2). Lesson kept:
   deployment path == import path == the certified artifact. No shims, ever.

L3 Throughput 10x below our own published best practice
   root: knowledge lived in docs (accelerating-blobs.html) but NOT in the code
   path that deploys (make_bundle wrapped the single-world entry; nothing
   machine-checked that 'gpu deploy' uses 'the batched mode the post proved').
   fix: (a) v03 makes batched the ONLY gpu deploy mode; (b) PERF ASSERTIONS in
   deploy smoke: generated bundle's pod_smoke measures worlds/hour and FAILS
   below a floor written next to the certified reference. Published claims
   become executable checks.

L4 Sanity checks accreted from past failures (gate theater)
   root: certification (one-time) conflated with deploy checks (every time)
   because software was being built mid-campaign.
   fix: SHIPPED — taxonomy A/B/C in MANIFEST (CI locks / one-time certs /
   2-min deploy smoke). Future runs: certified wheel + smoke, nothing more.

L5 Estimates and lessons scattered (context, docs, memories) not executable
   root: agent-memory as the storage medium for engineering constraints.
   fix: constraints move INTO the package: cost model in deploy_tools, perf
   floors in smoke, dtype/env requirements as install-time asserts
   (e.g. OOM env vars are already baked into generated pod_run.sh — extend
   the pattern).

MATURATION BACKLOG (blobkit 0.3->0.4, in priority order):
 1. v03 batched ladder + V1 identity (in flight) — closes L3(a).
 2. pytest suite: unit tests for genome ops/vacuum math/criteria (pure,
    fast, no sim); decision-identity as a marked slow test. CI = pytest +
    verify_locks, runnable via `pip install -e .[dev] && pytest`.
 3. make_bundle perf floor + preflight cost sheet — closes L1+L3(b).
 4. Version stamping end-to-end: every results row already carries backend;
    add blobkit.__version__ + lock-table hash to every row + archive header
    (provenance = which certified stack produced this number).
 5. README quickstart for external users (install, load world, run assay,
    verify locks) — the 'others can use it' bar.
 6. RETIRE remaining bundle-era scripts from probes/ deploy paths (single
    source: make_bundle).
=============================================================================

## Run-plan efficiency changes (adopted pre-relaunch)

REMAINING INEFFICIENCY AUDIT (plan-of-record, stage by stage):

S1 GENERATION STRUCTURE — the confirm serialization survives batching UNLESS
   confirms ride the same batch. In the CPU era: screen 96 -> confirm elites
   seed2 -> confirm seed3 (SEQUENTIAL phases; s3 tails idled islands for hours).
   The batched ladder fixes WITHIN-phase walls, but if pod_gen still emits
   screen/confirm as separate synchronous phases, we serialize 3 batch rounds
   per gen with the s2/s3 rounds mostly-empty (few elites).
   CHANGE: fold confirms into the NEXT gen's batch (async confirms): gen N+1's
   batch = 96 new candidates + gen N's pending s2/s3 confirm jobs. Zero idle
   lanes, no extra phase walls. Cost: elites enter the archive one gen later
   (negligible science impact; MAP-Elites is order-tolerant).
   -> implement in pod_gen driver flags, not in the assay (small change).

S2 ISLAND TOPOLOGY AT 6 PODS — 6 pods x 1 island x 20 gens with unions every
   2 gens = 60 union events touching my session (pull 6, merge, push 6, x10).
   CHANGE: unions become POD-LOCAL cadence-free: since each pod has 1 island,
   do 3 unions TOTAL (after gens 7, 14, final) — immigration pressure stays
   (mix has immigrate=20 vs archive), and the measured v1/v2 benefit of unions
   was concentrated in 2-3 merge events, not continuous mixing. 60 -> 18
   controller-touch events. Alternatively pods rsync archives peer-to-peer via
   a tiny cron — but keep it simple: 3 scheduled unions.

S3 MEASURE-POINT PROTOCOL — currently 'first 2 gens on pod1 then fan out' =
   serial: ~1-2h of single-pod time before parallelism starts.
   CHANGE: fan out ALL 6 pods immediately; the measure point is READ from pod1
   at gen-2 WITHOUT blocking the others (they're all running the same certified
   engine; if the number is bad we stop 6 pods instead of 1 — the downside is
   ~$20 of pod-hours, the upside is 1-2h earlier completion for the 5 others).
   Given user's parallelize-max + single-digit-hours policy: fan out day one.

S4 GEN-0 RE-CONFIRM TOLL — every island re-confirms the 190-cell union5 seed
   at g0 (we watched isl6 pay ~65 min for this in single mode). 6 islands
   re-confirming the SAME 190 incumbents = 5x wasted duplicate work.
   CHANGE: pre-confirm ONCE during the measure point (pod1 g0), then ship the
   confirmed archive (with fresh T_used stamps) to the other 5 pods as their
   g0-complete state; they start breeding at g1 directly. Saves ~5 pod-hours
   and removes the biggest cold-start wall.

S5 RESULT ROW PROVENANCE — already scoped into v03 (version+locks+engine per
   row). No further change.

S6 FILM/AUTOPSY PIPELINE — post-run analysis (l0-evolve-v2 wake + films) is
   still manual-ish; fine for now, not worth pre-engineering.

NET: 4 changes, all small, all in the DRIVER layer (pod_gen/runner scripts),
none touching certified code: async confirms, 3-union schedule, immediate
fan-out, seed-once-share-confirms. Est. combined effect: removes ~30-40% of
projected wall beyond what batching gives, and cuts controller babysitting by
~3x.
