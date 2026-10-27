#!/bin/bash
# fresh seed 4 (mutation draws mut_seed 4), T=10000: 3-component trait, kind-specific waste vs kind-blind waste twin, 1 thread each
cd "$(dirname "$0")"; export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50,"mut_seed":4}' python trait3.py s4_spec 4 10000 > s4_spec.log 2>&1 &
WORLD_P='{"ew":0.25,"sw":0,"mut_dt":50,"mut_seed":4}' python trait3.py s4_blind 4 10000 > s4_blind.log 2>&1 &
wait; echo ALLDONE
