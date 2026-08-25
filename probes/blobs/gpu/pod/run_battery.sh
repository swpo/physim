#!/bin/bash
# pod/run_battery.sh — full pod battery in gate-locked order. SAVE-AS-YOU-GO:
# every stage appends to results/*.json; rsync back after each stage.
set -e
cd ~/physim/probes/blobs/gpu
PY=.venv/bin/python
echo "=== gates first (locked before benchmarks) ==="
$PY tests/test_padding.py               2>&1 | tee results/pod_padding.log
$PY tests/test_chunking.py              2>&1 | tee results/pod_chunking.log
$PY tests/gate_f64.py                   2>&1 | tee results/pod_gate_f64.log
$PY tests/gate_anchor.py                2>&1 | tee results/pod_gate_anchor.log
echo "=== parity runs (GPU soup, scored locally later) ==="
$PY tests/gate_parity.py run            2>&1 | tee results/pod_parity_run.log
echo "=== benchmarks ==="
$PY bench/bench_step.py full            2>&1 | tee results/pod_bench_step.log
echo "=== headline ==="
$PY bench/bench_headline.py steponly    2>&1 | tee results/pod_head_step.log
$PY bench/bench_headline.py pop96       2>&1 | tee results/pod_head_pop96.log
$PY bench/bench_headline.py big512      2>&1 | tee results/pod_head_512.log
$PY bench/bench_headline.py big1024     2>&1 | tee results/pod_head_1024.log
echo "=== done ==="
