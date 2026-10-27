#!/bin/bash
# fresh seed 5 (mutation draws mut_seed 5), T=10000: kind-specific waste vs kind-blind twin, 1 thread each
cd "$(dirname "$0")"; export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50,"mut_seed":5}' python trait3c.py s5_spec 5 10000 > s5_spec.log 2>&1 &
WORLD_P='{"ew":0.25,"sw":0,"mut_dt":50,"mut_seed":5}' python trait3c.py s5_blind 5 10000 > s5_blind.log 2>&1 &
wait; echo ALLDONE
