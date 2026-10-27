#!/bin/bash
# fresh seeds 3 4, T=6000: kind-specific waste vs kind-blind waste twin (trait.py with merge and fade rows)
cd "$(dirname "$0")"; export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
for sd in 3 4; do
  WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50}' python trait.py w_s${sd}_spec $sd 6000 > w_${sd}_spec.log 2>&1 &
  WORLD_P='{"ew":0.25,"sw":0,"mut_dt":50}' python trait.py w_s${sd}_blind $sd 6000 > w_${sd}_blind.log 2>&1 &
done
wait; echo ALLDONE
