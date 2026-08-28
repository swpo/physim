
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
