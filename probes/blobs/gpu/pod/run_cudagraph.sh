#!/bin/bash
cd ~/physim/probes/blobs/gpu
PY=.venv/bin/python
unset XLA_FLAGS
$PY bench/bench_cudagraph.py baseline        2>&1 | tee -a results/cudagraph.log
export XLA_FLAGS="--xla_gpu_enable_command_buffer=FUSION,CUBLAS,CUSTOM_CALL"
$PY bench/bench_cudagraph.py cmdbuf_full     2>&1 | tee -a results/cudagraph.log
export XLA_FLAGS="--xla_gpu_enable_command_buffer="
$PY bench/bench_cudagraph.py cmdbuf_off      2>&1 | tee -a results/cudagraph.log
