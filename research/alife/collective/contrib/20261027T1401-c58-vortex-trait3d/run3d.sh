#!/bin/bash
# 3-component trait, kind-specific waste (sw 0.4) vs kind-blind waste twin (sw 0), seeds 1 2, T=6000
cd "$(dirname "$0")"; export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
for sd in 1 2; do
  WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50}' python trait3.py d3_s${sd}_spec $sd 6000 > d3_${sd}_spec.log 2>&1 &
  WORLD_P='{"ew":0.25,"sw":0,"mut_dt":50}' python trait3.py d3_s${sd}_blind $sd 6000 > d3_${sd}_blind.log 2>&1 &
done
wait; echo ALLDONE
