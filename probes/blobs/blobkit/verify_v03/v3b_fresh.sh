#!/bin/bash
# verify_v03/v3b_fresh.sh — fresh-venv install + import + entry smoke.
set -e
PYBIN=${PYBIN:-python3.11}
rm -rf /tmp/bk03fresh
$PYBIN -m venv /tmp/bk03fresh
/tmp/bk03fresh/bin/pip -q install --upgrade pip >/dev/null
cd "$(dirname "$0")/.."
/tmp/bk03fresh/bin/pip -q install . >/dev/null
/tmp/bk03fresh/bin/python - <<'EOF'
import json
import blobkit
lk = blobkit.verify_locks()
assert lk["ok"], lk
from blobkit import assay_batch, deploy_tools
from blobkit.assay_batch import run_assay_batch, _norm_jobs, _pad_B
assert callable(run_assay_batch)
assert _pad_B(5, (4, 8, 16, 32)) == 8
ij, t0s, caps, tm = _norm_jobs(
    [dict(genome={"id": "x"}, seed=3, t0=5000.0, cap=20000.0)],
    2500.0, 20000.0)
assert (t0s, caps, tm) == ([5000.0], [20000.0], 5000.0)
# jax must NOT be required for import (lazy)
import sys
assert "jax" not in sys.modules, "jax leaked into plain import"
print(json.dumps(dict(gate="V3b", version=blobkit.__version__,
                      locks_ok=lk["ok"], n_checked=lk["n_checked"],
                      entry="run_assay_batch", jax_lazy=True, pass_=True)))
EOF
