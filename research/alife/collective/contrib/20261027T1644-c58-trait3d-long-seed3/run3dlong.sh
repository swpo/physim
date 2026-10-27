#!/bin/bash
# fresh seed 3, T=10000: 3-component trait, kind-specific waste vs kind-blind waste twin (2 threads each)
cd "$(dirname "$0")"; export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=2
WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50}' python trait3.py d3L_s3_spec 3 10000 > d3L_3_spec.log 2>&1 &
WORLD_P='{"ew":0.25,"sw":0,"mut_dt":50}' python trait3.py d3L_s3_blind 3 10000 > d3L_3_blind.log 2>&1 &
wait; echo ALLDONE
