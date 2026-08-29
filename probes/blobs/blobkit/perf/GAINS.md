# GAINS.md — record-path fix: evidence + expected-gain table

Anchor: frozen T2 prod workload `697bcb716916` (16 lanes, H100 PCIe,
blobkit 0.3.2). Headline row 42.3 w/h (1361 s); instrumented row 38.3 w/h
(1505 s) with seam totals:

    record  2299 s cumulative   (18,516 record points, ~124 ms/point-batch)
    dispatch 493 s              battery 356 s     pull 40 s
    => record cum / wall = x1.53 "effective threads" at BLOBGPU_REC_THREADS=8
    => record tracking is the binding constraint (~60%+ of wall);
       sim ceiling from T1 gpu cells ~369 w/h vs 42 achieved.

## Diagnosis (t2record microbench, rows in results/rows.jsonl)

`bench.py t2record --device cpu` (laptop, 16 lanes m0/pred, real advanced
states; identity gate extract+apply vs stock _record: PASS):

    scaling   serial 3.13 ms/record | threads2 x1.69 | threads4 x2.47 |
              threads8 x2.36 (SATURATES) | procs2 x1.85 | procs4 x3.13 |
              procs8 x4.01 (KEEPS SCALING)
    GIL probe (2 threads, independent arrays): blob_list_fast x1.79,
              ndimage_label x1.50, periodic_label x1.18 (union-find is
              pure Python), np.dot control x1.38
    components (pred, N=128, ms): blob_list_fast 3.98 ≈ record_REC_total
              3.96 (mass 0.05) — blob lists ARE the REC record; CREC adds
              patches 1.37 + orgs 0.90 every 5th point (~10% of cum)

Conclusion: the record path is GIL-BOUND in the thread pool (numpy/scipy
release the GIL only partially; periodic_label's union-find not at all).
Threads saturate at ~x2.4 alone — and on the pod the record threads also
fight the dispatch thread + battery pool, giving the measured x1.5.
Processes keep scaling (payloads are small: acts (na,256,256) f32 ≈ 1.6 MB,
pickle ~0.1 ms — negligible vs 33 ms/record for pred-class worlds).

## Fix candidates, ranked (all bench-provable on workload 697bcb716916)

(a) record tracking in a SPAWN PROCESS pool (the battery pattern).
    Prototype SHIPPED here: proto_procrec.py (runtime driver wrap, no
    locked-file edits) + `bench.py t2 --procrec`. Identity: recbench
    identity_gate PASS (extract+apply == stock _record, m0+pred, snaps
    incl.) and proto_procrec.gate_batch PASS (gpu-backend batch, record
    streams + statuses + snaps + t_step bitwise equal, 4 lanes T=500).
    0.4 engineering: same split inside sim_gpu._record_host/_driver_kw
    (extract = jax-free picklable worker a la _batteryproc; apply = host).

(b) coarser CREC cadence flag (25 -> 50 tu): saves only ~5% of record cum
    (CREC share ~10%, halved) AND is a SCIENCE change (patches/orgs/memf
    streams thin out; decisions/metrics windows shift) -> needs its own
    validation campaign. NOT worth it alone; bundle only if (a) lands and
    CREC extraction shows up in the post-(a) instrumented row.

(c) H-C2 device-side records (0.4+): blob lists are ~90% of record cum and
    need periodic labeling on device (jnp connected components) — the big
    lift. Post-(a) the record path should no longer bind at B=16; re-rank
    with the post-(a) instrumented row before investing.

(d) micro: patches sizes via one bincount instead of per-label .sum()
    (locked sim_cpu._record does O(k) full-mask passes on the CREC grid).
    Identical outputs, locked-file edit -> 0.4 relock item, small (~5% of
    record cum).

## Expected-gain table (model: instrumented wall 1505 s; record effective
## wall = 2299/1.5 = 1533 -> replaced by 2299/x_new; other seams unchanged)

| scenario                     | record x | wall (s) | w/h  | speedup vs 38.3 |
|------------------------------|----------|----------|------|-----------------|
| 0.3.2 threads8 (measured)    | x1.5     | 1505     | 38.3 | 1.00x           |
| (a) procs @ x4 (laptop-meas) | x4.0     |  546     | 105  | 2.75x           |
| (a) procs @ x6 (26-vcpu pod) | x6.0     |  355     | 162  | 4.24x           |
| (a) ideal x8                 | x8.0     |  259     | 222  | 5.81x           |
| (c) device records (~x20)    | ~x20     |  ~90+    | ~300+| bounded by sim  |

Caveats: model assumes dispatch/battery/pull stay constant (battery pool
and record pool will share cores — cap total procs at cpu_count; the pod
has 26 vcpus, 8+8 is fine); overlap=True already hides part of dispatch,
so headline (non-instrumented) gains will be somewhat smaller than the
instrumented model; the x4 row is the only locally MEASURED scaling point.

## The claim procedure (one compare command)

On the pod, blobkit 0.3.2, after this thread's bench update:

    python bench.py t2 --config t2 --device gpu                # baseline row
    python bench.py t2 --config t2 --device gpu --procrec      # fix row
    python bench.py compare --tier t2 --config t2 --device gpu

Same tier/config/device/workload hash `697bcb716916` -> the ratio column IS
the claim. For 0.4 (fix built into sim_gpu, no flag): install 0.4, rerun
row 1, compare joins on the workload hash across versions.

Local rows (this laptop, for the record): t2smoke stock 102.3 s vs
--procrec 102.1 s (null as expected: CPU-JAX t2 wall is 97% dispatch —
the record fix is a GPU-host phenomenon, exactly what the ledger says).
