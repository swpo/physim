# blobkit 0.3.0

The certified physim blob core as an installable package. No more sys.path /
tree-layout archaeology on GPU pods, CPU fleets, or laptops.

0.2 added backend injection (`assay_v2b.run_assay_b(backend=...)`), the
shared L2 sim driver, and the fleet bundle generator (`deploy_tools`).
0.3 adds the BATCHED-LADDER assay driver — "a generation is one tensor":

```python
from blobkit.assay_batch import run_assay_batch
outs = run_assay_batch([(g1, 1), (g2, 1), ...])   # B lanes, ONE device tensor
# same per-world out dicts as run_assay_b; LOCKED criteria decide per lane
# at each rung (2500 -> x2 -> cap); exited lanes leave, survivors repack.
```

Fleet mode: `python -m blobkit.deploy_tools <dir> --backend gpu_batch` emits
`pod_worker_batch.py` (whole-shard batched sweeps), `pod_gen_batch.py`
(async confirms `confirms:"async"`, donor-archive start `g0:"import"`) and
`pod_run_batch.sh`. V1 gates: batch == singles bitwise (VERIFY_V03.md).

```bash
pip install ./blobkit                # CPU (numpy + scipy)
pip install './blobkit[gpu]'         # + jax[cuda12]==0.4.38 for the GPU backend
```

```python
import blobkit                        # SHA256 lock self-check on import
blobkit.verify_locks()                # explicit check -> dict
from blobkit.worlds import load, GT_SET, KICKS
g = load("m0")                        # packaged genome, no source tree needed

from blobkit import assay_v2
out = assay_v2.run_assay(g, seed=1, results_path=None)

from blobkit.soup import get_backend
be = get_backend("cpu")               # or "gpu" (needs the [gpu] extra)
S = be.init_soup(g, L=128.0, seed=1, workers=2)
be.advance(S, 2500.0)
rec = be.snapshot_rec(S)
```

CLI (same as the old complexity/assay_v2.py, minus the tree):

```bash
python -m blobkit.assay_v2 m0 --seed 7 --results ./results.json
```

Provenance, locked hashes, and the promotion rule: `MANIFEST.md`.
Verification transcript: `VERIFY.md`.

Env knobs: `BLOBKIT_SKIP_LOCK=1` (skip import lock check),
`BLOBKIT_DATA=<dir>` (override packaged worlds), `BLOBKIT_RESULTS=<path>`
(assay_v2 CLI default results path).
