#!/bin/bash
# usage: run_arms.sh SEED  (runs every arm from /tmp/claude-0/sSEED.npz, one after another)
export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
cd "$(dirname "$0")"
for arm in ctrl kdlocal kdzero kdlocal_chiF0 k2zero kdzero_chiF0; do
  python kdarms.py /tmp/claude-0/s$1.npz $1 $arm arms/${arm}_s$1.json
done
