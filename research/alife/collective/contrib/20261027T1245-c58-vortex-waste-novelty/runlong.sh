#!/bin/bash
# long runs to T=12000: kind-specific waste (sw 0.4) and kind-blind waste (sw 0, the matched neutral twin: gain independent of theta), seeds 1 2
cd "$(dirname "$0")"; export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
for sd in 1 2; do
  WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50}' python trait.py L_s${sd}_spec $sd 12000 > L_${sd}_spec.log 2>&1 &
  WORLD_P='{"ew":0.25,"sw":0,"mut_dt":50}' python trait.py L_s${sd}_blind $sd 12000 > L_${sd}_blind.log 2>&1 &
done
wait; echo ALLDONE
